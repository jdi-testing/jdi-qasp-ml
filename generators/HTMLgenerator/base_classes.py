import logging
import os
import random
from abc import abstractmethod, ABC
from os import path
from pathlib import Path

import faker

from HTMLgenerator.service import generate_uuid

prefix = os.getcwd().split("jdi-qasp-ml")[0]
project_path = os.path.join(prefix, "jdi-qasp-ml")
generators_path = os.path.join(prefix, "jdi-qasp-ml", "generators")

fake = faker.Faker()

attributes_without_value = ("disabled", "multiple", "required", "checked", "readonly")


class BaseHTMLBuilder(ABC):
    """Class responsible for file generation.
    elements attribute contains all available for certain framework
    class types. All of these classes should be inherited from BaseElement"""

    elements = []

    def __init__(self, num_of_pages: int, elements_on_page: int, output_path: str):
        self._num_of_pages = num_of_pages
        self._elements_on_page = elements_on_page
        self._output_path = output_path

    @property
    @abstractmethod
    def framework_name(self):
        """Defines name of framework. It uses for output catalog generation
        and template identification"""
        pass

    def generate(self):
        """Generation of .html file based on template from /templates folder"""
        logging.info(
            f"Started generation of HTML files using {self.framework_name} framework."
        )
        output_file_path = path.join(self._output_path, self.framework_name)
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        if path.exists(f"HTMLgenerator/templates/{self.framework_name}.html"):
            template_file_path = f"HTMLgenerator/templates/{self.framework_name}.html"
        else:
            template_file_path = f"templates/{self.framework_name}.html"

        with open(template_file_path, "r") as template:
            html_text = template.read()
        for i in range(self._num_of_pages):
            output_text = self._generate_text(html_text)
            file_name = path.join(output_file_path, f"{i}.html")
            with open(file_name, "w") as output:
                output.write(output_text)
            logging.info(f"File {file_name} generated.")
        full_path = path.join(os.getcwd(), output_file_path)
        logging.info(
            f"Generation of {self.framework_name} finished. "
            f"{self._num_of_pages} files generated at {full_path}."
        )

    def _generate_text(self, html_text):
        """
        Iterates over available elements classes and fill in
        body of template
        :param html_text: string with html template
        :return:
        """
        body = ""
        for i in range(self._elements_on_page):
            element_class = random.choice(self.__class__.elements)
            body += element_class().markup()
        output_text = html_text.replace("%BODY%", body)
        return output_text


class BaseElement(ABC):
    """Represents HTML element. List of available HTML attributes
    is stored in instance's attribute html_attributes and can be modified in inherited classes"""

    self_closing_tag = False
    label_needed = False

    def __init__(self, **kwargs):
        self.style_attributes = {}
        self.html_attributes = {}
        self.tag = ""
        self._label = None
        self.nested_elements = []

        self.html_attributes["id"] = generate_uuid()
        self.html_attributes["name"] = generate_uuid()
        self.html_attributes["class"] = generate_uuid()
        self.html_attributes["name"] = generate_uuid()

        if "label" in kwargs:
            self._label = kwargs["label"]

        # Names 'for' and 'class' are forbidden for parameter
        if "attr_for" in kwargs:
            kwargs["for"] = kwargs["attr_for"]
            del kwargs["attr_for"]
        if "attr_class" in kwargs:
            kwargs["class"] = kwargs["attr_class"]
            del kwargs["attr_class"]
        self.html_attributes.update(kwargs)

        self.label_element = None
        self.label_first = False

        self.randomize_styling()

    @abstractmethod
    def randomize_styling(self):
        """Generates default CSS properties"""
        pass

    @abstractmethod
    def add_specific_attributes(self):
        """Adds element specific HTML attributes"""
        pass

    @property
    @abstractmethod
    def label(self):
        """Returns a label according to dataset/classes.txt"""
        pass

    def add_unnecessary_html_attribute(self, name: str, value, chance: int):
        """
        Adds unnecessary attribute to attributes dict with specified chance of appearance
        :param name: Name of a tag
        :param value: Value of a tag
        :param chance: Integer value from 0 to 100 represents chance of tag appear in element
        """
        if random.randint(0, 100) < chance:
            self.html_attributes[name] = value

    def generate_html_attributes_string(self):
        """Generates string that can be pasted in element markup with specified HTML attributes"""
        attrs = ""
        self.html_attributes["style"] = self.generate_style_string()
        self.html_attributes["data-label"] = self.label
        for k in random.sample(
            self.html_attributes.keys(), len(self.html_attributes.keys())
        ):
            if k in attributes_without_value:
                if self.html_attributes[k]:
                    attrs += " " + k
            elif k == "inner_value":  # value between opening and closing tag
                continue
            else:
                attrs += f' {k}="{self.html_attributes[k]}"'
        return attrs.strip()

    def generate_style_string(self):
        """Generates string using specified CSS properties"""
        self.randomize_styling()
        style = ""
        for k, v in self.style_attributes.items():
            style += f"{k}:{v}; "
        return style.strip()

    def markup(self, label_margin=None):
        """Defines full element markup with all specified attributes and nested elements"""
        if self.nested_elements:
            nested_markup_list = []
            for element in self.nested_elements:
                if isinstance(element, BaseElement):
                    nested_markup_list.append(element.markup())
                elif isinstance(element, str):
                    nested_markup_list.append(element)
            inner_value = "\n".join(nested_markup_list)
            inner_value = f"\n{inner_value}\n"
        else:
            try:
                inner_value = f"\n{self.html_attributes['inner_value']}\n"
            except KeyError:
                inner_value = ""
        tag_ending = (
            "/>\n" if self.self_closing_tag else f">\t{inner_value}</{self.tag}>\n"
        )
        label_text = ""
        if self.label_element is not None:
            if self.label_first and label_margin:
                self.style_attributes["margin-left"] = label_margin
            label_text = self.label_element.markup()
        element_markup = (
            f"""<{self.tag} {self.generate_html_attributes_string()} {tag_ending}"""
        )

        if self.label_first:
            return "".join([label_text, element_markup])
        else:
            return "".join([element_markup, label_text])
