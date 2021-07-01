import random
from abc import abstractmethod, ABC
from os import path
from pathlib import Path

import faker

fake = faker.Faker()

attributes_without_value = ('disabled', 'multiple', 'required',
                            'checked')


class BaseHTMLBuilder(ABC):
    """Class responsible for file generation.
    elements attribute contains all available for certain framework
    class types. All of these classes should be inherited from BaseElement"""
    elements = []

    def __init__(self, num_of_pages: int, elements_on_page: int,
                 output_path: str):
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
        output_file_path = path.join(self._output_path, self.framework_name)
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        if path.exists(f'HTMLgenerator/templates/{self.framework_name}.html'):
            template_file_path = f'HTMLgenerator/templates/{self.framework_name}.html'
        else:
            template_file_path = f'templates/{self.framework_name}.html'

        with open(template_file_path, "r") as template:
            html_text = template.read()
        for i in range(self._num_of_pages):
            output_text = self._generate_text(html_text)
            with open(path.join(output_file_path, f"{i}.html"), "w") as output:
                output.write(output_text)

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
            body += element_class().element_markup()
        output_text = html_text.replace("%BODY%", body)
        return output_text


class BaseElement(ABC):
    """Represents HTML element. List of available HTML attributes
    is stored in instance's attribute html_attributes and can be modified in inherited classes"""
    self_closing_tag = False
    label_needed = False
    nested_elements = []

    def __init__(self):
        self.style_attributes = {}
        self.html_attributes = {}
        self.tag = ''

    @abstractmethod
    def element_markup(self):
        """Defines full element markup with all specified attributes"""
        pass

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
        attrs = ''
        self.html_attributes['style'] = self.generate_style_string()
        self.html_attributes['data-label'] = self.label
        for k in random.sample(self.html_attributes.keys(), len(self.html_attributes.keys())):
            if k in attributes_without_value:
                if self.html_attributes[k]:
                    attrs += ' ' + k
            elif k == 'inner_value':  # value between opening and closing tag
                continue
            else:
                attrs += f' {k}="{self.html_attributes[k]}"'
        return attrs.strip()

    def generate_style_string(self):
        """Generates string using specified CSS properties"""
        self.randomize_styling()
        style = ''
        for k, v in self.style_attributes.items():
            style += f'{k}:{v}; '
        return style.strip()
