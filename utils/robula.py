import datetime
import re
from copy import copy
from itertools import chain, combinations

from lxml import html, etree
from lxml.etree import XPathEvalError


class XPathEvaluationTimeExceeded(Exception):
    pass


class XPath:
    def __init__(self, value) -> None:
        self.value = value

    def get_value(self):
        return self.value

    def starts_with(self, value):
        return self.value.startswith(value)

    def substring(self, value):
        return self.value[value:]

    def head_has_any_predicates(self):
        return '[' in self.value.split('/')[2]

    def head_has_position_predicate(self):
        split_xpath = self.value.split('/')
        pattern = re.compile(r"[0-9]")
        return 'position()' in split_xpath[2] or 'last()' in split_xpath[2] or pattern.search(split_xpath[2])

    def head_has_text_predicate(self):
        return 'text()' in self.value.split('/')[2]

    def add_predicate_to_head(self, predicate):
        split_xpath = self.value.split('/')
        split_xpath[2] += predicate
        self.value = '/'.join(split_xpath)

    def __len__(self):
        length = 0
        for el in self.value.split('/'):
            if el:
                length += 1
        return length

    def __str__(self):
        return self.value

    def __repr__(self) -> str:
        return f'XPath({self.value})'


class RobulaPlus:
    def __init__(self, element, document):
        self.attribute_priorization_list = ['name', 'class', 'title', 'alt', 'value']
        self.attribute_black_list = [
            'href',
            'src',
            'onclick',
            'onload',
            'tabindex',
            'width',
            'height',
            'style',
            'size',
            'maxlength',
            'jdn-hash',
            'xml:space',
            'fill',
            'xmlns'
        ]

        self.forbidden_tags = ['svg', 'rect']
        self.maximum_evaluation_time_in_seconds = 5
        self.maximum_length_of_text = 1000

        self.element = element
        self.document = document

    def get_robust_xpath(self):
        start_time = datetime.datetime.now()
        x_path_list = [XPath('//*')]
        while len(x_path_list) > 0:
            x_path = x_path_list.pop(0)
            temp = []

            temp.extend(self.transf_convert_star(x_path))
            temp.extend(self.transf_add_id(x_path))
            temp.extend(self.transf_add_text(x_path))
            temp.extend(self.transf_add_attribute(x_path))
            temp.extend(self.transf_add_attribute_set(x_path))
            temp.extend(self.transf_add_position(x_path))
            temp.extend(self.transf_add_level(x_path))

            temp = remove_duplicates(temp)
            for el in temp:
                if (datetime.datetime.now() - start_time).total_seconds() > self.maximum_evaluation_time_in_seconds:
                    raise XPathEvaluationTimeExceeded

                try:
                    if self.uniquely_locate(el.get_value()):
                        return el.get_value()
                    x_path_list.append(el)
                except XPathEvalError:
                    pass

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

    @staticmethod
    def generate_power_set(attributes):
        s = [(key, value) for key, value in attributes.items()]
        powerset = [list(el) for el in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))]
        return powerset

    def uniquely_locate(self, xpath):
        elements = self.document.xpath(xpath)
        return len(elements) == 1 and elements[0] == self.element

    def transf_convert_star(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)
        if xpath.starts_with('//*') and ancestor.tag.lower() not in self.forbidden_tags:
            output.append(XPath('//' + ancestor.tag.lower() + xpath.substring(3)))
        return output

    def transf_add_id(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)
        try:
            ancestor_id = ancestor.id
        except AttributeError:
            ancestor_id = None
        if (ancestor_id is not None
                and not xpath.head_has_position_predicate()
                and not xpath.head_has_text_predicate()):
            new_xpath = XPath(xpath.get_value())
            new_xpath.add_predicate_to_head(f'[@id={ancestor_id}]')
            output.append(new_xpath)
        return output

    def transf_add_text(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)
        ancestor_text_content = str(ancestor.text_content()).replace("'", "&quot;")
        ancestor_text_content = str(ancestor.text_content()).replace(b'\xc2\xa0'.decode("utf-8"), " ")  # NBSP
        ancestor_text_content = str(ancestor.text_content()).replace(b'\xe2\x80\x89'.decode("utf-8"), " ")  # THSP

        if (not ancestor_text_content.isspace()
                and not xpath.head_has_position_predicate()
                and not xpath.head_has_text_predicate()
                and len(ancestor_text_content) < self.maximum_length_of_text):

            new_x_path = XPath(xpath.get_value())
            new_x_path.add_predicate_to_head(f"[contains(text(), '{ancestor_text_content}')]")
            output.append(new_x_path)
        return output

    def transf_add_attribute(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)
        if not xpath.head_has_any_predicates():
            # add priority attributes to output
            for priority_attribute in self.attribute_priorization_list:
                for attribute in ancestor.attrib.items():
                    if attribute[0] == priority_attribute:
                        new_xpath = XPath(xpath.get_value())
                        new_xpath.add_predicate_to_head(f"[@{attribute[0]}='{attribute[1]}']")
                        output.append(new_xpath)
                        break

        # append all other non-blacklist attributes to output
        for attribute in ancestor.attrib.items():
            if attribute[0] not in self.attribute_black_list and attribute[0] not in self.attribute_priorization_list:
                new_xpath = XPath(xpath.get_value())
                new_xpath.add_predicate_to_head(f"[@{attribute[0]}='{attribute[1]}']")
                output.append(new_xpath)
        return output

    def transf_add_attribute_set(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)

        if not xpath.head_has_any_predicates():
            self.attribute_priorization_list = ['id'] + self.attribute_priorization_list

            attributes = copy(ancestor.attrib)
            # remove black list attributes
            for attribute in self.attribute_black_list:
                if attribute in attributes:
                    del attributes[attribute]

            # generate power set
            attribute_power_set = self.generate_power_set(attributes)
            # remove sets with cardinality < 2
            attribute_power_set = [attribute for attribute in attribute_power_set if len(attribute) >= 2]
            # sort elements inside each powerset
            for attribute_set in attribute_power_set:
                attribute_set.sort(key=lambda el: el[0] in self.attribute_priorization_list, reverse=True)

            # sort powerset based on length of subset
            attribute_power_set.sort(key=len)
            # remove id
            self.attribute_priorization_list.pop(0)

            # convert to predicate
            for attr_set in attribute_power_set:
                predicate = f"[@{attr_set[0][0]}='{attr_set[0][1]}'"
                for i in range(1, len(attr_set)):
                    predicate += f" and @{attr_set[i][0]}='{attr_set[i][1]}'"
                predicate += ']'
                new_xpath = XPath(xpath.get_value())
                new_xpath.add_predicate_to_head(predicate)
                output.append(new_xpath)
        return output

    def transf_add_position(self, xpath):
        output = []
        ancestor = self.get_ancestor(len(xpath) - 1)

        if not xpath.head_has_position_predicate():
            position = 1
            if xpath.starts_with('//*'):
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
            output.append(XPath('//*' + xpath.substring(1)))
        return output


def path_list(xpath):
    temp = xpath.replace("//", "")
    elements = temp.split("/")
    if temp[-1] == "/":
        elements.pop()

    return elements


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def generate_xpath(xpath, page):
    document = html.fromstring(page)
    element = document.xpath(xpath)
    if element is None \
            or len(element) == 0:
        return "Document does not contain given element!"
    element = element[0]
    tree = etree.ElementTree(document)
    robula = RobulaPlus(element, document)

    try:
        robust_path = robula.get_robust_xpath()
    except XPathEvaluationTimeExceeded:
        pass
        return tree.getpath(element)

    return robust_path
