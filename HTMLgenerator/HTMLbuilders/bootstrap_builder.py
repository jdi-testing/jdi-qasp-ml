import random

import faker

from HTMLgenerator.HTMLbuilders.base_classes import BaseHTMLBuilder, BaseElement
from HTMLgenerator.service import generate_uuid

fake = faker.Faker()


class BootstrapBaseElement(BaseElement):
    available_tags = {}
    available_classes = {}
    main_class = ''

    def __init__(self, **kwargs):
        super().__init__()
        self.generate_tag()
        self.html_attributes['id'] = generate_uuid()
        self.html_attributes['name'] = generate_uuid()
        self.html_attributes['class'] = self.generate_class_name()
        self.html_attributes.update(kwargs)

        self.add_specific_attributes()
        self.randomize_styling()

    def add_specific_attributes(self):
        self.add_unnecessary_html_attribute('disabled', True, 30)

    def randomize_styling(self):
        """Generates default CSS properties"""
        self.style_attributes = {
            'color': fake.color(hue=random.choice(['blue', 'monochrome', 'red', 'green']),
                                luminosity='dark'),
            'font-size': f"{random.randint(14, 28)}px",
        }

    def element_markup(self):
        if self.nested_elements:
            inner_value = '\n'.join([element.element_markup() for element in self.nested_elements])
        else:
            try:
                inner_value = self.html_attributes['inner_value']
            except KeyError:
                inner_value = ''
        tag_ending = "/>" if self.self_closing_tag else f">{inner_value}</{self.tag}>"

        return f"""<{self.tag} 
                    {self.generate_html_attributes_string()}
                    {tag_ending}"""

    def generate_class_name(self):
        classes = [self.main_class, generate_uuid()]

        for k, v in self.available_classes.items():
            if random.randint(0, 100) < k[1]:
                classes.append(random.choice(v))
        return ' '.join(classes)

    def generate_tag(self):
        """Chooses between available tags for this element"""
        self.tag = random.choice(self.available_tags)


class Button(BootstrapBaseElement):
    available_tags = ['button', 'a', 'input']
    available_classes = {
        ('size', 50): ('btn-lg', 'btn-sm', ''),
        ('block', 15): ('btn-block',),
        ('style', 100): ('btn-primary', 'btn-secondary', 'btn-success',
                         'btn-danger', 'btn-warning', 'btn-warning',
                         'btn-light', 'btn-dark', 'btn-link',
                         'btn-outline-primary', 'btn-outline-secondary', 'btn-outline-success',
                         'btn-outline-danger', 'btn-outline-warning', 'btn-outline-warning',
                         'btn-outline-light', 'btn-outline-dark', 'btn-outline-link')
    }

    main_class = 'btn'

    def add_specific_attributes(self):
        super().add_specific_attributes()

        if self.tag != 'input':
            self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(1, 3))

        if self.tag == 'input':
            self.html_attributes['type'] = random.choice(['button', 'submit', 'reset'])
            if self.html_attributes['type'] == 'button':
                self.html_attributes['value'] = fake.word()
        elif self.tag == 'a':
            self.html_attributes['role'] = 'button'


class Checkbox(BootstrapBaseElement):
    available_classes = {
        ('control', 100): ('form-check-input',)
    }
    label_needed = True

    @property
    def tag(self):
        return 'input'

    def generate_html_attributes(self):
        super().generate_html_attributes()
        specific_attributes = {
            'type': 'checkbox'
        }
        self.html_attributes.update(specific_attributes)

    def generate_style_string(self):
        return ''
#
#
# class CheckList(BootstrapBaseElement):
#     available_classes = {
#         ('required', 100): ['form-check'],
#         ('alignment', 40): ['form-check-inline']
#     }
#
#     @property
#     def tag(self):
#         return 'input'
#
#     def element_markup(self):
#         checklist_text = self.generate_checkbox_elements("form-check-input", "form-check-label")
#         return f'''<div {self.generate_html_attributes_string()}>{checklist_text}</div>'''


class BootstrapBuilder(BaseHTMLBuilder):
    elements = [
        Button,
        # Checkbox,
        # CheckList
    ]

    @property
    def framework_name(self):
        return 'bootstrap'
