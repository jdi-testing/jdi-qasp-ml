import random
import string
from abc import ABC
from datetime import datetime

from base_classes import BaseElement
from faker import Faker
from service import border_properties, generate_uuid

fake = Faker()


class HTML5BaseElement(BaseElement, ABC):
    def __init__(self, randomize_styling=True, **kwargs):
        self._randomize_styling = randomize_styling
        super().__init__(**kwargs)
        self.add_specific_attributes()

    def randomize_styling(self):
        """Generates default CSS properties"""
        if self._randomize_styling:
            self.style_attributes = {
                'color': fake.color(hue=random.choice(['blue', 'monochrome', 'red', 'green']),
                                    luminosity='dark'),
                'font-size': f"{random.randint(14, 28)}px",
            }

    def add_specific_attributes(self):
        """Generates default HTML attributes"""
        self.add_unnecessary_html_attribute('disabled', True, 30)

    @staticmethod
    def generate_options():
        """Generates list of options with randomized value"""
        options_text = ''
        for i in range(random.randint(3, 10)):
            value = fake.word()
            options_text += f'''<option value="{value}">{value}</option>\n'''
        return options_text

    def add_label(self):
        self.label_first = random.randint(0, 10) > 5
        self.label_element = Label(attr_for=self.html_attributes['id'], label="label")


class Button(HTML5BaseElement):
    def __init__(self, **kwargs):
        if "type" not in kwargs:
            available_tags = ['button', 'input']
            self.tag = random.choice(available_tags)

        super().__init__(**kwargs)

    @property
    def label(self):
        return 'button'

    def randomize_styling(self):
        if self._randomize_styling:
            super().randomize_styling()
            specific_styling = {
                'background': fake.color(),
                'border-color': fake.color(),
                'padding': f'{random.randint(2, 30)}px {random.randint(2, 50)}px',
                'font-size': f"{random.randint(10, 56)}px",
                'border-radius': f"{random.randint(0, 50)}%",
            }
            self.style_attributes.update(specific_styling)

    def add_specific_attributes(self):
        super().add_specific_attributes()
        text_key = "inner_value" if self.tag == "button" else "value"
        specific_attributes = {
            text_key: fake.sentence(nb_words=1),
        }
        self.html_attributes.update(specific_attributes)
        if self.tag != "button":
            self.add_unnecessary_html_attribute("formaction", generate_uuid(), 50)
            self.add_button_type()
            self.add_formenctype()

    def add_formenctype(self):
        possible_values = [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
        self.add_unnecessary_html_attribute("formenctype", random.choice(possible_values), 50)

    def add_button_type(self):
        available_types = ["submit", "reset", "button"]
        self.html_attributes["type"] = random.choice(available_types)

    def markup(self, label_margin=None):
        markup = super().markup(label_margin=label_margin)
        if self.tag != "button":
            markup = f"<form>{markup}</form>"
        return markup


class Range(HTML5BaseElement):
    self_closing_tag = True

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    @property
    def label(self):
        return 'range'

    def add_specific_attributes(self):
        super(Range, self).add_specific_attributes()
        min_value = random.randint(0, 1000)
        max_value = random.randint(min_value + 1, 2000)
        specific_attributes = {
            'min': min_value,
            'max': max_value,
            'value': random.randint(min_value, max_value),
            'step': random.choice((1, 5, 10, 15, 20)),
            'inner_value': fake.sentence(nb_words=1),
        }
        self.html_attributes.update(specific_attributes)

    def markup(self):

        # data list creation
        options = ''
        if random.randint(0, 10) > 7:
            min_value = self.html_attributes['min']
            max_value = self.html_attributes['max']
            for i in range(min_value,
                           max_value,
                           random.randint(1, round((max_value - min_value) / 10) + 1)):
                options += f'<option value="{i}"></option>'
        data_list = f'''
            <datalist id="datalist-{self.html_attributes['id']}" style=>
                {options}
            </datalist>
        '''

        range_text = f'''<input
                  type="range"
                  {f'list="datalist-{self.html_attributes["id"]}"' if data_list else ''}
                  {self.generate_html_attributes_string()}>'''
        label_text = f'''<label for="{self.html_attributes['id']}"
                   style="{self.generate_style_string()}">
                    {self.html_attributes['inner_value']}
                  </label>'''
        elements = [range_text, label_text, data_list]
        random.shuffle(elements)
        return f'''
                <div>
                    {''.join(elements)}
                </div>
                '''


class RadioButtons(HTML5BaseElement):
    @property
    def label(self):
        return 'radiobutton'

    self_closing_tag = True

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'name': {generate_uuid()}
        }
        self.html_attributes.update(specific_attributes)

    def markup(self):
        question_text = fake.sentence(nb_words=10)
        num_of_choices = random.randint(1, 10)
        options_text = ""

        # options generation
        vertical_alignment = bool(random.randint(0, 1))
        active_element = random.randint(0, num_of_choices)
        for i in range(num_of_choices):
            element_id = generate_uuid()
            label_style_string = self.generate_style_string()
            label_style_string = f'style="{label_style_string}"'
            disabled = random.randint(0, 10) > 7
            radio_text = f'''<input type="radio"
                            {self.generate_html_attributes_string()}
                            {'checked' if i == active_element else ''}
                            {'disabled' if disabled else ''}
                            style={self.generate_style_string()}>'''
            label_text = f'''<label for="{element_id}" {label_style_string}>{fake.sentence(nb_words=1)}</label>'''

            elements = [label_text, radio_text]
            random.shuffle(elements)
            options_text += f'''
                            {''.join(elements)}
                            {'<br>' if vertical_alignment else ''}
                            '''

        return f"""
                    <p style=\"{self.generate_style_string()}\">{question_text}</p>
                    <div {'style="display:inline-block"' if vertical_alignment else ''}>
                        {options_text}
                    </div>
                """


class Table(HTML5BaseElement):

    @property
    def label(self):
        return 'table'

    def add_specific_attributes(self):
        self.html_attributes = {}

    def randomize_styling(self):
        self.style_attributes.update(border_properties())

    def markup(self):
        # remove table from available elements to avoid recursion
        available_elements = elements[:]
        available_elements.remove(self.__class__)
        elements_in_table = [random.choice(available_elements)().markup()
                             for _ in range(random.randint(1, random.randint(10, 20)))]
        num_of_columns = random.randint(1, 5)
        table_contents = ''
        while len(elements_in_table) > num_of_columns:
            table_row_string = '<tr>'
            for i in range(num_of_columns):
                table_row_string += f'<td style="{self.generate_style_string()}">{elements_in_table.pop()}</td>'
            table_row_string += '</tr>'
            table_contents += table_row_string

        return f'<table style="{self.generate_style_string()}" data-label="table">{table_contents}</table>'

    def __init__(self):
        super().__init__()
        self.tag = 'table'


class TextField(HTML5BaseElement):
    self_closing_tag = True

    @property
    def label(self):
        return 'textfield'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': 'text',
        }
        self.html_attributes.update(specific_attributes)
        self.add_unnecessary_html_attribute('minlength', random.randint(4, 150), 70)
        if 'minlength' in specific_attributes:  # if minlength exists maxlength cannot be greater
            maxlength = random.randint(int(specific_attributes['minlength']), 300)
        else:
            maxlength = random.randint(1, 150)
        self.add_unnecessary_html_attribute('maxlength', maxlength, 70)
        self.add_unnecessary_html_attribute('value', fake.sentence(nb_words=random.randint(1, 10)), 40)
        self.add_unnecessary_html_attribute('placeholder', fake.sentence(nb_words=random.randint(3, 8)), 90)


class TextArea(HTML5BaseElement):

    @property
    def label(self):
        return 'textarea'

    def __init__(self):
        super().__init__()
        self.tag = 'textarea'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'rows': random.randint(4, 15),
            'cols': random.randint(10, 30)
        }

        self.add_unnecessary_html_attribute('inner_value', fake.paragraph(nb_sentences=random.randint(5, 15)), 50)
        self.add_unnecessary_html_attribute('placeholder', fake.paragraph(nb_sentences=random.randint(1, 3)), 50)
        self.html_attributes.update(specific_attributes)


class FileInput(HTML5BaseElement):

    @property
    def label(self):
        return 'fileinput'

    def __init__(self):
        super().__init__()
        self.tag = 'input'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        accept = ','.join([f"*.{fake.bothify(text='???', letters=string.ascii_lowercase)}"
                           for _ in range(random.randint(1, 3))])
        specific_attributes = {
            'type': 'file',
        }
        self.add_unnecessary_html_attribute('accept', accept, 60)
        self.add_unnecessary_html_attribute('capture', random.choice(["user", "environment"]), 15)
        self.add_unnecessary_html_attribute('multiple', True, 50)
        self.html_attributes.update(specific_attributes)

    def markup(self):
        label = f'<label for="{self.html_attributes.get("id")}">{fake.sentence(nb_words=random.randint(4, 15))}</label>'
        elements = [label, super().markup()]
        random.shuffle(elements)
        return ''.join(elements)


class Selector(HTML5BaseElement):

    @property
    def label(self):
        return 'selector'

    def __init__(self):
        super().__init__()
        self.tag = 'select'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.add_unnecessary_html_attribute('multiple', True, 40)
        self.add_unnecessary_html_attribute('required', True, 60)
        self.add_unnecessary_html_attribute('size', random.randint(3, 10), 80)

    def markup(self):
        options_text = self.generate_options()
        selector_text = f'''<select {self.generate_html_attributes_string()} style="{self.generate_style_string()}">
                            {options_text}
                        </select>'''
        return selector_text


class Datalist(HTML5BaseElement):

    @property
    def label(self):
        return 'dropdown'

    def __init__(self):
        super().__init__()
        self.tag = 'datalist'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'list': f'datalist-{self.html_attributes["id"]}',
        }
        self.html_attributes.update(specific_attributes)

    def markup(self):
        options = self.generate_options()
        input_markup = f'''<input {self.generate_html_attributes_string()} style="{self.generate_style_string()}"/>'''
        datalist = f'''
        <datalist id=datalist-{self.html_attributes["id"]}>
            {options}
        </datalist>'''
        return f'''<div>{''.join(random.sample([input_markup, datalist], 2))}</div>'''


class CheckList(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def markup(self):
        checklist_text = self.generate_checkbox_elements(input_class="checkbox")
        return f'''<div {self.generate_html_attributes_string()}>{checklist_text}</div>'''

    def generate_checkbox_elements(self, input_class="", label_class=""):
        """Generates markup of random checkboxes"""
        num_of_elements = random.randint(2, 12)
        checklist_text = ''
        for i in range(num_of_elements):
            checkbox = CheckBox()
            checklist_text += checkbox.markup()
        return checklist_text


class CheckBox(HTML5BaseElement):
    @property
    def label(self):
        return "checkbox"

    def __init__(self, randomize_styling=True, **kwargs):
        super().__init__(randomize_styling=randomize_styling, **kwargs)
        self.tag = "input"
        self.html_attributes["type"] = "checkbox"
        self.add_unnecessary_html_attribute("checked", True, 50)
        self.add_unnecessary_html_attribute("indeterminate", random.choice(["true", "false"]), 25)
        self.add_label()


class ColorPicker(HTML5BaseElement):
    @property
    def label(self):
        return 'colorpicker'

    def __init__(self):
        super().__init__()
        self.tag = 'input'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': 'color'
        }
        self.html_attributes.update(specific_attributes)
        self.add_unnecessary_html_attribute('value', fake.color(), 50)


class Progress(HTML5BaseElement):

    @property
    def label(self):
        return 'progressbar'

    def __init__(self):
        super().__init__()
        self.tag = 'progress'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        max_value = random.randint(1, 1000)
        value = random.randint(0, max_value)
        specific_attributes = {
            'max': max_value,
            'value': value,
            'inner_value': f'{(value / max_value) * 100} %'
        }
        self.html_attributes.update(specific_attributes)


class DateTimeInput(HTML5BaseElement):

    @property
    def label(self):
        return 'datetimeselector'

    def __init__(self):
        super().__init__()
        self.tag = 'input'
        self.add_label()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': random.choice(['date', 'month', 'datetime-local', 'time', 'week'])
        }
        self.html_attributes.update(specific_attributes)
        self.generate_values()
        autocomplete_values = [
            "on", 
            "cc-exp", 
            "bday",
            "bday-day",
            "bday-month",
            "bday-year",
        ]
        self.add_unnecessary_html_attribute('required', True, 50)
        self.add_unnecessary_html_attribute('step', random.randint(1, 2000), 50)
        self.add_unnecessary_html_attribute('readonly', "readonly", 25)
        self.add_unnecessary_html_attribute('autocomplete', random.choice(autocomplete_values), 25)

    def generate_values(self):
        min_date = self.get_random_date()
        max_date = self.get_random_date(min_date)
        value = self.get_random_date(min_date, max_date)
        format_string = self.get_format_string()
        if self.html_attributes['type'] == 'time':
            min_time = self.get_random_time()
            max_time = self.get_random_time(min_time['hour'], min_time['minute'])
            value_time = self.get_random_time(min_time['hour'], min_time['minute'],
                                              max_time['hour'], max_time['minute'])
            min_date = datetime.now().replace(**min_time)
            max_date = datetime.now().replace(**max_time)
            value = datetime.now().replace(**value_time)

        self.add_unnecessary_html_attribute('min', min_date.strftime(format_string), 50)
        self.add_unnecessary_html_attribute('max', max_date.strftime(format_string), 50)
        self.add_unnecessary_html_attribute('value', value.strftime(format_string), 50)

    def get_format_string(self):
        format_string = '%Y-%m-%dT%H:%M'
        if self.html_attributes['type'] == 'date':
            format_string = '%Y-%m-%d'
        elif self.html_attributes['type'] == 'month':
            format_string = '%Y-%m'
        elif self.html_attributes['type'] == 'datetime-local':
            format_string = '%Y-%m-%dT%H:%M'
        elif self.html_attributes['type'] == 'time':
            format_string = '%H:%M'
        elif self.html_attributes['type'] == 'week':
            format_string = '%Y-W%W'

        return format_string

    @staticmethod
    def get_random_date(start=None, end=None):
        if start is None:
            start = datetime.now().replace(day=1, month=1, year=2000)
        if end is None:
            end = datetime.now().replace(day=1, month=1, year=2030)
        random_day = datetime.fromordinal(random.randint(start.toordinal(), end.toordinal())).replace(
            hour=random.randint(0, 23), minute=random.randint(0, 59))
        return random_day

    @staticmethod
    def get_random_time(min_hour=0, min_minute=0, max_hour=23, max_minute=59):
        return {'hour': random.randint(min_hour, max_hour), 'minute': random.randint(min_minute, max_minute)}


class NumberInput(HTML5BaseElement):
    label_needed = True

    @property
    def label(self):
        return 'numberselector'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': 'number'
        }
        self.html_attributes.update(specific_attributes)
        precision = random.randint(0, 5)
        min_value = round(random.random() * 1000, precision)
        max_value = random.randint(round(min_value * 100), 100000) / 100
        value = random.randint(round(min_value * 100), round(max_value * 100)) / 100
        step = random.randint(0, round(max_value) * 1000) / 1000
        self.add_unnecessary_html_attribute('min', min_value, 50)
        self.add_unnecessary_html_attribute('max', max_value, 50)
        self.add_unnecessary_html_attribute('value', value, 80)
        self.add_unnecessary_html_attribute('step', step, 80)


class Paragraph(HTML5BaseElement):

    def __init__(self):
        super().__init__()
        self.tag = 'p'

    @property
    def label(self):
        return 'n/a'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.paragraph(nb_sentences=random.randint(5, 15))


class Link(HTML5BaseElement):

    @property
    def label(self):
        return 'link'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'a'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes.update({
            'href': random.choice(["#", fake.url()]),
            'inner_value': fake.sentence(nb_words=random.randint(1, 3))
        })

        referrer_policies = [
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ]
        relationships = [
            "alternate",
            "author",
            "bookmark",
            "external",
            "help",
            "license",
            "next",
            "nofollow",
            "noopener",
            "noreferrer",
            "opener",
            "prev",
            "search",
            "tag",
        ]
        self.add_unnecessary_html_attribute("download", fake.url(), 30)
        self.add_unnecessary_html_attribute("ping", fake.url(), 30)
        self.add_unnecessary_html_attribute("referrerpolicy", random.choice(referrer_policies), 30)
        self.add_unnecessary_html_attribute("rel", random.choice(relationships), 30)
        self.add_unnecessary_html_attribute("target", random.choice(["_self", "_blank", "_parent", "_top"]), 30)
        self.add_unnecessary_html_attribute("rel", random.choice(relationships), 30)
        self.add_unnecessary_html_attribute("type", fake.mime_type(), 30)


class Label(HTML5BaseElement):
    @property
    def label(self):
        if self._label is None:
            return 'n/a'
        else:
            return self._label

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'label'

    def add_specific_attributes(self):
        self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(3, 8))


class OrderedList(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'ol'


class UnorderedList(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'ul'


class ListItem(HTML5BaseElement):

    @property
    def label(self):
        if self._label is None:
            return 'n/a'
        else:
            return self._label

    def __init__(self, generate_text=False, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'li'
        if generate_text:
            include_link = random.randint(0, 10) > 3
            if include_link:
                link = Link()
                self.nested_elements.append(link)

            for _ in range(random.randint(0, 2)):
                self.nested_elements.append(fake.sentence(nb_words=random.randint(1, 2)))

            random.shuffle(self.nested_elements)


class Div(HTML5BaseElement):

    @property
    def label(self):
        if self._label is None:
            return 'n/a'
        else:
            return self._label

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'div'


class Span(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'span'


class Form(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'form'


class Input(HTML5BaseElement):

    @property
    def label(self):
        if self._label is not None:
            return self._label
        else:
            return 'n/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.add_unnecessary_html_attribute('placeholder', fake.sentence(nb_words=random.randint(1, 4)), 70)


class HorizontalLine(HTML5BaseElement):
    self_closing_tag = True

    @property
    def label(self):
        return 'n/a'

    def __init__(self, randomize_styling=False, **kwargs):
        super().__init__(randomize_styling, **kwargs)
        self.tag = 'hr'


class Header(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, randomize_styling=True, **kwargs):
        super().__init__(randomize_styling, **kwargs)
        self.tag = f'h{random.randint(1, 6)}'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(5, 12))


class Option(HTML5BaseElement):

    @property
    def label(self):
        return 'n/a'

    def __init__(self, randomize_styling=True, **kwargs):
        super().__init__(randomize_styling, **kwargs)
        self.tag = 'option'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(1, 3))


elements = [
    Button,
    CheckList,
    ColorPicker,
    DateTimeInput,
    RadioButtons,
    Range,
    Table,
    Paragraph,
    Link,
    TextField,
    TextArea,
    FileInput,
    Selector,
    Datalist,
    Progress,
    NumberInput
]
