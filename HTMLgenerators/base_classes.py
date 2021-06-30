import random
import string
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
        with open(f"templates/{self.framework_name}.html", "r") as template:
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
            break_line = random.randint(0, 10) > 8
            if break_line:
                body += f'''<div style="border: 2px solid black; display: block;">
                        {element_class().element_markup()}</div>'''
            else:
                body += element_class().element_markup()
        output_text = html_text.replace("%BODY%", body)
        return output_text


class BaseElement(ABC):
    """Represents HTML element. List of available HTML attributes
    is stored in instance's attribute html_attributes and can be modified in inherited classes"""
    self_closing_tag = False
    label_needed = False

    def __init__(self):
        self.style_attributes = {}
        self.html_attributes = {}
        self._tag = ''
        self.generate_html_attributes()

    @property
    @abstractmethod
    def tag(self):
        """Stores tag of element"""
        return self._tag

    def element_markup(self):
        """Defines full element markup with all specified attributes"""
        if self.label_needed:
            return self.generate_markup_with_label()
        else:
            return self.generate_standard_markup()

    def generate_standard_markup(self):
        return f"""<{self.tag} 
        {self.generate_html_attributes_string()}
        style="{self.generate_style_string()}"
        {"/>" if self.self_closing_tag else
        f">{self.html_attributes['inner_value'] if 'inner_value' in self.html_attributes else ''}</{self.tag}>"}"""

    def generate_markup_with_label(self):
        if random.randint(0, 10) > 5:  # with or without label
            return self.generate_standard_markup()
        else:
            element_markup_text = self.generate_standard_markup()
            label_text = self.generate_label()
            return f'''<div>{''.join(random.sample([label_text, element_markup_text], 2))}</div>'''

    def generate_style_attributes(self):
        """Generates default CSS properties"""
        self.style_attributes = {
            'color': fake.color(hue=random.choice(['blue', 'monochrome', 'red', 'green']),
                                luminosity='dark'),
            'font-size': f"{random.randint(14, 28)}px",
        }

    def generate_html_attributes(self):
        """Generates default HTML attributes"""
        self.html_attributes = {
            'class': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
            'id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
            'name': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        }
        self.add_unnecessary_html_attribute('disabled', True, 30)

    def generate_style_string(self):
        """Generates string using specified CSS properties"""
        self.generate_style_attributes()
        style = ''
        for k, v in self.style_attributes.items():
            style += f'{k}:{v}; '
        return style.strip()

    def generate_html_attributes_string(self):
        """Generates string that can be pasted in element markup with specified HTML attributes"""
        attrs = ''
        shuffled_keys = self.html_attributes.keys()
        for k in random.sample(self.html_attributes.keys(), len(self.html_attributes.keys())):
            if k in attributes_without_value:
                if self.html_attributes[k]:
                    attrs += ' ' + k
            elif k == 'inner_value':  # value between opening and closing tag
                continue
            else:
                attrs += f' {k}="{self.html_attributes[k]}"'
        return attrs.strip()

    def add_unnecessary_html_attribute(self, name: str, value, chance: int):
        """
        Adds unnecessary attribute to attributes dict with specified chance of appearance
        :param name: Name of a tag
        :param value: Value of a tag
        :param chance: Integer value from 0 to 100 represents chance of tag appear in element
        """
        if random.randint(0, 100) < chance:
            self.html_attributes[name] = value

    def generate_label(self):
        """Generates random label for element"""
        return f'''<label for="{self.html_attributes["id"]}">
                            {fake.sentence(nb_words=random.randint(5, 15))}
                         </label>'''

    @staticmethod
    def generate_options():
        """Generates list of options with randomized value"""
        options_text = ''
        for i in range(random.randint(3, 10)):
            value = fake.word()
            options_text += f'''<option value="{value}">{value}</option>\n'''
        return options_text
