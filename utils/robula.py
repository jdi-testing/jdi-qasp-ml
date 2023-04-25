import datetime
import re
from copy import copy
from itertools import chain, combinations

from cachetools import LRUCache, cached
from cachetools.keys import hashkey
from lxml import etree, html
from lxml.etree import XPathEvalError

from app.logger import logger


class XPathEvaluationTimeExceeded(Exception):
    pass


class XPathCantFindPath(Exception):
    pass


class XPathDocumentDoesntContainElement(Exception):
    pass


class XPath:
    def __init__(self, value) -> None:
        self.value = value

    def get_value(self) -> str:
        return self.value

    def starts_with(self, value):
        return self.value.startswith(value)

    def substring(self, value):
        return self.value[value:]

    def head_has_any_predicates(self):
        return "[" in self.value.split("/")[2]

    def head_has_position_predicate(self):
        split_xpath = self.value.split("/")
        pattern = re.compile(r"[0-9]")
        return (
            "position()" in split_xpath[2]
            or "last()" in split_xpath[2]
            or pattern.search(split_xpath[2])
        )

    def head_has_text_predicate(self):
        return "text()" in self.value.split("/")[2]

    def add_predicate_to_head(self, predicate):
        split_xpath = self.value.split("/")
        split_xpath[2] += predicate
        self.value = "/".join(split_xpath)

    def first_not_a_star_level(self):
        levels = filter(None, self.get_value().split("/"))
        for index, level in enumerate(levels):
            if level and level != "*":
                return index

    def positions_with_index(self):
        """Returns positions with indexes"""
        positions = []
        levels = filter(None, self.get_value().split("/"))
        for index, level in enumerate(levels):
            pattern = re.compile(r"\[\d+\]")
            if pattern.search(level):
                positions.append(index)
        return positions

    def starts_with_index(self):
        """Checks whether xpath starts with index or not (stars in the beginning are ignored)"""
        if self.first_not_a_star_level() in self.positions_with_index():
            return True
        return False

    def contains_index_in_the_middle(self):
        """Checks whether xpath contains index in the middle"""
        positions = self.positions_with_index()
        if self.first_not_a_star_level() in positions:
            del positions[positions.index(self.first_not_a_star_level())]
        if len(self) - 1 in positions:
            del positions[positions.index(len(self) - 1)]

        return len(positions)

    def ends_with_index(self):
        """Checks whether xpath ends with index or not"""
        if len(self) - 1 in self.positions_with_index():
            return True
        return False

    def ends_with_star(self):
        """
        Check whether xpath ends with star or not.
        Xpaths based on element count can't be robust.
        """
        return self.get_value()[-1] == "*"

    def __len__(self):
        length = 0
        for el in self.value.split("/"):
            if el:
                length += 1
        return length

    def __str__(self):
        return self.value

    def __repr__(self) -> str:
        return f"XPath({self.value})"


class RobulaPlus:
    def __init__(self, element, document, config):
        self.attribute_priorization_list = [
            "name",
            "class",
            "title",
            "alt",
            "value",
        ]
        self.attribute_black_list = [
            "href",
            "src",
            "onclick",
            "onload",
            "tabindex",
            "width",
            "height",
            "style",
            "size",
            "maxlength",
            "jdn-hash",
            "xml:space",
            "fill",
            "xmlns",
            "data-label",
        ]
        self.forbidden_tags = ["svg", "rect"]

        self.maximum_generation_time_in_seconds = config[
            "maximum_generation_time"
        ]
        self.allow_indexes_at_the_beginning = config[
            "allow_indexes_at_the_beginning"
        ]
        self.allow_indexes_in_the_middle = config[
            "allow_indexes_in_the_middle"
        ]
        self.allow_indexes_at_the_end = config["allow_indexes_at_the_end"]
        self.maximum_length_of_text = 1000

        self.element = element
        self.document = document

    def check_for_time_limit(self, start_time):
        evaluation_time_in_seconds = (
            datetime.datetime.now() - start_time
        ).total_seconds()
        if (
            self.maximum_generation_time_in_seconds is not None
            and evaluation_time_in_seconds
            > self.maximum_generation_time_in_seconds
        ):
            raise XPathEvaluationTimeExceeded

    def get_robust_xpath(self):
        start_time = datetime.datetime.now()
        x_path_list = [XPath("//*")]
        while len(x_path_list) > 0:
            current_xpath = x_path_list.pop(0)
            temp = self.generate_xpaths_for_current_level(
                current_xpath, start_time
            )

            for el in temp:
                evaluation_time_in_seconds = (
                    datetime.datetime.now() - start_time
                ).total_seconds()
                if (
                    self.maximum_generation_time_in_seconds is not None
                    and evaluation_time_in_seconds
                    > self.maximum_generation_time_in_seconds
                ):
                    raise XPathEvaluationTimeExceeded

                try:
                    el = self.clean_xpath(el)
                    if self.xpath_is_valid(
                        el, current_xpath
                    ) and self.uniquely_locate(el.get_value()):
                        return el.get_value()
                    x_path_list.append(el)
                except XPathEvalError:
                    pass
        raise XPathCantFindPath

    def generate_xpaths_for_current_level(self, xpath, start_time):
        """Returns array of xpaths possible for current level"""
        temp = []
        temp.extend(self.transf_convert_star(xpath))
        temp.extend(self.transf_add_id(xpath))
        temp.extend(self.transf_add_text(xpath))
        temp.extend(self.transf_add_attribute(xpath))
        temp.extend(self.transf_add_attribute_set(xpath, start_time))
        temp.extend(self.transf_add_position(xpath))
        temp.extend(self.transf_add_level(xpath))
        temp = remove_duplicates(temp)
        return temp

    def clean_xpath(self, xpath: XPath):
        """Removes redundant symbols from xpath if it's possible"""
        value = xpath.get_value()
        cleaned_path = self.remove_redundant_levels(value)
        if self.uniquely_locate(cleaned_path):
            return XPath(cleaned_path)
        else:
            return xpath

    def get_ancestor(self, index):
        output = self.element
        for i in range(index):
            output = output.getparent()
        return output

    def get_ancestor_count(self):
        count = 0
        element = self.element
        while element.getparent() is not None:
            element = element.getparent()
            count += 1
        return count

    def generate_power_set(self, attributes, start_time):

        s = [(key, value) for key, value in attributes.items()]
        combinations_iterable = (combinations(s, r) for r in range(len(s) + 1))
        chain_from_iterable = chain.from_iterable(combinations_iterable)

        powerset = []
        for iteration, el in enumerate(chain_from_iterable):
            powerset.append(list(el))
            if iteration > 512:
                self.check_for_time_limit(start_time)

        return powerset

    def uniquely_locate(self, xpath):
        elements = self.document.xpath(xpath)
        return len(elements) == 1 and elements[0] == self.element

    def transf_convert_star(self, xpath):
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
        except AttributeError:
            return output

        if (
            xpath.starts_with("//*")
            and ancestor.tag.lower() not in self.forbidden_tags
        ):
            output.append(
                XPath("//" + ancestor.tag.lower() + xpath.substring(3))
            )
        return output

    def transf_add_id(self, xpath):
        """Generates xpath with id of element"""
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
            ancestor_id = ancestor.id
        except AttributeError:
            ancestor_id = None
        if (
            ancestor_id is not None
            and not xpath.head_has_position_predicate()
            and not xpath.head_has_text_predicate()
        ):
            new_xpath = XPath(xpath.get_value())
            new_xpath.add_predicate_to_head(f"[@id={ancestor_id}]")
            output.append(new_xpath)
        return output

    def transf_add_text(self, xpath):
        """Generates xpath with element's inner text (text of this element and all children)"""
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
        except AttributeError:
            return output
        ancestor_text_content = self.remove_invalid_characters(
            str(ancestor.text_content())
        )
        if "/" in ancestor_text_content:
            return output

        if (
            not ancestor_text_content.isspace()
            and not xpath.head_has_position_predicate()
            and not xpath.head_has_text_predicate()
            and len(ancestor_text_content) < self.maximum_length_of_text
        ):
            new_x_path = XPath(xpath.get_value())
            new_x_path.add_predicate_to_head(
                f"[contains(text(), '{ancestor_text_content}')]"
            )
            output.append(new_x_path)
        return output

    def transf_add_attribute(self, xpath):
        """Generates list of xpaths with all valid attributes"""
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
        except AttributeError:
            return output
        if not xpath.head_has_any_predicates():
            # add priority attributes to output
            for priority_attribute in self.attribute_priorization_list:
                for attribute in ancestor.attrib.items():
                    if attribute[0] == priority_attribute:
                        new_xpath = XPath(xpath.get_value())
                        attribute_value = self.remove_invalid_characters(
                            attribute[1]
                        )
                        new_xpath.add_predicate_to_head(
                            f"[@{attribute[0]}='{attribute_value}']"
                        )
                        output.append(new_xpath)
                        break

        # append all other non-blacklist attributes to output
        for attribute in ancestor.attrib.items():
            if (
                attribute[0] not in self.attribute_black_list
                and attribute[0] not in self.attribute_priorization_list
            ):
                new_xpath = XPath(xpath.get_value())
                attribute_value = self.remove_invalid_characters(attribute[1])
                new_xpath.add_predicate_to_head(
                    f"[@{attribute[0]}='{attribute_value}']"
                )
                output.append(new_xpath)
        return output

    def transf_add_attribute_set(self, xpath, start_time):
        """Generates xpaths with all possible permutations of attributes with len > 2"""
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
        except AttributeError:
            return output

        if not xpath.head_has_any_predicates():
            self.attribute_priorization_list = [
                "id"
            ] + self.attribute_priorization_list

            attributes = copy(ancestor.attrib)
            # remove black list attributes
            for attribute in self.attribute_black_list:
                if attribute in attributes:
                    del attributes[attribute]

            # generate power set
            attribute_power_set = self.generate_power_set(
                attributes, start_time
            )
            # remove sets with cardinality < 2
            attribute_power_set = [
                attribute
                for attribute in attribute_power_set
                if len(attribute) >= 2
            ]
            # sort elements inside each powerset
            for attribute_set in attribute_power_set:
                attribute_set.sort(
                    key=lambda el: el[0] in self.attribute_priorization_list,
                    reverse=True,
                )

            # sort powerset based on length of subset
            attribute_power_set.sort(key=len)
            # remove id
            self.attribute_priorization_list.pop(0)
            # convert to predicate
            for attr_set in attribute_power_set:
                predicate = f"[@{attr_set[0][0]}='{self.remove_invalid_characters(attr_set[0][1])}'"
                for i in range(1, len(attr_set)):
                    predicate += f" and @{attr_set[i][0]}='{self.remove_invalid_characters(attr_set[i][1])}'"
                predicate += "]"
                new_xpath = XPath(xpath.get_value())
                new_xpath.add_predicate_to_head(predicate)
                output.append(new_xpath)
                self.check_for_time_limit(start_time)

        return output

    def transf_add_position(self, xpath):
        """Generates xpath with attribute's position index"""
        output = []
        try:
            ancestor = self.get_ancestor(len(xpath) - 1)
        except AttributeError:
            return output

        if (
            not xpath.head_has_position_predicate()
            and ancestor.getparent() is not None
        ):
            position = 1
            if xpath.starts_with("//*"):
                position = ancestor.getparent().index(ancestor) + 1
            else:
                for child in ancestor.getparent():
                    if ancestor == child:
                        break
                    if ancestor.tag == child.tag:
                        position += 1
            new_xpath = XPath(xpath.get_value())
            new_xpath.add_predicate_to_head(f"[{position}]")
            output.append(new_xpath)

        return output

    def transf_add_level(self, xpath):
        output = []
        if len(xpath) - 1 < self.get_ancestor_count():
            output.append(XPath("//*" + xpath.substring(1)))
        return output

    @staticmethod
    def remove_invalid_characters(s: str):
        """Removes characters which can't be used in xpath"""
        valid_string = s[:]
        chars_to_remove = [
            "'",
            "\t",
            "\n",
            b"\xc2\xa0".decode("utf-8"),  # NBSP
            b"\xe2\x80\x89".decode("utf-8"),
        ]  # THSP

        valid_string = valid_string.translate(
            {ord(ch): "" for ch in chars_to_remove}
        )
        return valid_string

    @staticmethod
    def remove_redundant_levels(value):
        """Replaces repeating levels (\\*) in xpath with //*"""
        normalized_value = re.sub(r"(\/\*){2,}", "//*", value)
        return normalized_value

    def xpath_is_valid(self, xpath: XPath, parent_xpath: XPath):
        """Checks validity of xpath according to custom rules"""
        if self.xpath_contains_only_tag(xpath, parent_xpath):
            return False

        if (
            not self.allow_indexes_at_the_beginning
            and xpath.starts_with_index()
        ):
            return False

        if not self.allow_indexes_at_the_end and xpath.ends_with_index():
            return False

        if (
            not self.allow_indexes_in_the_middle
            and xpath.contains_index_in_the_middle()
        ):
            return False

        if xpath.ends_with_star():
            return False

        return True

    def xpath_contains_only_tag(self, xpath: XPath, parent_xpath: XPath):
        """Returns true if xpath consists only of a tag e.g. '//select'"""
        converted_star = self.transf_convert_star(parent_xpath)
        if (
            len(xpath) == 1
            and len(converted_star)
            and xpath.get_value() == converted_star[0].get_value()
        ):
            return True
        return False


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def split_full_path_to_current_and_parents_parts(full_path):
    full_path_split = full_path.split("/")
    current_level_locator = full_path_split[-1]
    parent_path = "/".join(full_path_split[:-1])
    return parent_path, current_level_locator


@cached(
    cache=LRUCache(maxsize=10 * 1024 * 1024),
    key=lambda xpath, page, document_uuid, config: hashkey(
        xpath, document_uuid
    ),
)
def generate_xpath(xpath, page, document_uuid, config):
    document = html.fromstring(page)
    element = document.xpath(xpath)
    if element is None or len(element) == 0:
        raise XPathDocumentDoesntContainElement(
            "Document does not contain given element {xpath}!"
        )
    element = element[0]
    tree = etree.ElementTree(document)
    robula = RobulaPlus(element, document, config)

    try:
        robust_path = robula.get_robust_xpath()
    except XPathEvaluationTimeExceeded:
        current_level_full_path = tree.getpath(element)
        logger.info(
            f"Time Exceeded on element {element.tag} - "
            f"using element's parent to generate locator"
        )
        (
            parent_path,
            current_level_locator,
        ) = split_full_path_to_current_and_parents_parts(
            current_level_full_path
        )
        parent_robust_locator = generate_xpath(
            parent_path, page, document_uuid, config
        )
        return f"{parent_robust_locator}//{current_level_locator}"

    except XPathCantFindPath:
        return tree.getpath(element)

    return robust_path
