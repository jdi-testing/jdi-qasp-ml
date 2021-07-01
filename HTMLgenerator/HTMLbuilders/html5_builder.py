import random
import string
from datetime import datetime

from faker import Faker

from HTMLgenerator.HTMLbuilders.base_classes import BaseHTMLBuilder, BaseElement
from HTMLgenerator.service import generate_uuid

fake = Faker()


class BaseHTML5Element(BaseElement):
    @property
    def label(self):
        return 'n/a'

    def __init__(self):
        super().__init__()
        self.add_specific_attributes()

    def element_markup(self):
        """Defines full element markup with all specified attributes"""
        if self.label_needed:
            return self.generate_markup_with_label()
        else:
            return self.generate_standard_markup()

    def generate_standard_markup(self):
        return f"""<{self.tag} 
            {self.generate_html_attributes_string()}
            {"/>" if self.self_closing_tag else
        f">{self.html_attributes['inner_value'] if 'inner_value' in self.html_attributes else ''}</{self.tag}>"}"""

    def generate_markup_with_label(self):
        if random.randint(0, 10) > 5:  # with or without label
            return self.generate_standard_markup()
        else:
            element_markup_text = self.generate_standard_markup()
            label_text = self.generate_label()
            return f'''<div>{''.join(random.sample([label_text, element_markup_text], 2))}</div>'''

    def randomize_styling(self):
        """Generates default CSS properties"""
        self.style_attributes = {
            'color': fake.color(hue=random.choice(['blue', 'monochrome', 'red', 'green']),
                                luminosity='dark'),
            'font-size': f"{random.randint(14, 28)}px",
        }

    def add_specific_attributes(self):
        """Generates default HTML attributes"""
        self.html_attributes = {
            'class': generate_uuid(),
            'id': generate_uuid(),
            'name': generate_uuid(),
        }
        self.add_unnecessary_html_attribute('disabled', True, 30)

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

    def generate_checkbox_elements(self, input_class="", label_class=""):
        """Generates markup of random checkboxes"""
        num_of_elements = random.randint(2, 12)
        checklist_text = ''
        for i in range(num_of_elements):
            value = fake.word()
            input_id = '-'.join([self.html_attributes['id'], value])
            checked = True if random.randint(0, 10) > 8 else False
            input_class_string = f'class="{input_class}"' if input_class else ''
            label_class_string = f'class="{label_class}"' if label_class else ''
            input_text = f'''<input type="checkbox" {input_class_string} data-label="checkbox" 
                             id={input_id} name="{self.html_attributes['name']}" 
                             {'checked' if checked else ''}>'''
            label_text = f'''<label for="{input_id}" {label_class_string} 
                             style="{self.generate_style_string()}">{value}</label>'''
            checklist_text += f'''{''.join(random.sample([input_text, label_text], 2))}<br>'''
        return checklist_text


class Button(BaseHTML5Element):
    def __init__(self):
        super().__init__()
        self.tag = 'button'

    @property
    def label(self):
        return 'button'

    def randomize_styling(self):
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
        specific_attributes = {
            'inner_value': fake.sentence(nb_words=1),
        }
        self.html_attributes.update(specific_attributes)


class Range(BaseHTML5Element):
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

    def element_markup(self):

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


class RadioButtons(BaseHTML5Element):
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

    def element_markup(self):
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


class Table(BaseHTML5Element):

    @property
    def label(self):
        return 'table'

    def add_specific_attributes(self):
        self.html_attributes = {}

    def randomize_styling(self):
        self.style_attributes = {
            'border-style': random.choice(('solid', 'none', 'dotted', 'inset',
                                           'dashed solid', 'hidden', 'double',
                                           'groove', 'ridge')),
            'border-width': f"{random.randint(1, 5)}px",
            'border-color': fake.color()
        }

    def element_markup(self):
        # remove table from available elements to avoid recursion
        available_elements = HTML5Builder.elements[:]
        available_elements.remove(self.__class__)
        elements_in_table = [random.choice(available_elements)().element_markup()
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


class Paragraph(BaseHTML5Element):

    def __init__(self):
        super().__init__()
        self.tag = 'p'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.paragraph(nb_sentences=random.randint(5, 15))


class Link(BaseHTML5Element):

    @property
    def label(self):
        return 'link'

    def __init__(self):
        super().__init__()
        self.tag = 'a'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes.update({
            'href': f"http://{fake.word()}.{fake.word()}",
            'inner_value': fake.sentence(nb_words=random.randint(3, 30))
        })


class TextField(BaseHTML5Element):
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


class TextArea(BaseHTML5Element):

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


class FileUpload(BaseHTML5Element):

    @property
    def label(self):
        return 'fileinput'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        accept = ','.join([f"*.{fake.bothify(text='???', letters=string.ascii_lowercase)}"
                           for _ in range(random.randint(1, 3))])
        specific_attributes = {
            'type': 'file',
            'accept': f".{fake.bothify(text='???', letters=string.ascii_lowercase)}"
        }
        self.add_unnecessary_html_attribute('accept', accept, 60)
        self.html_attributes.update(specific_attributes)

    def element_markup(self):
        label = f'<label for="{self.html_attributes.get("id")}">{fake.sentence(nb_words=random.randint(4, 15))}</label>'
        elements = [label, super().element_markup()]
        random.shuffle(elements)
        return ''.join(elements)


class Selector(BaseHTML5Element):

    @property
    def label(self):
        return 'selector'

    def __init__(self):
        super().__init__()
        self.tag = 'select'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.add_unnecessary_html_attribute('multiple', None, 40)
        self.add_unnecessary_html_attribute('required', True, 60)
        self.add_unnecessary_html_attribute('size', random.randint(3, 10), 80)

    def element_markup(self):
        label_text = self.generate_label()
        options_text = self.generate_options()
        selector_text = f'''<select {self.generate_html_attributes_string()} style="{self.generate_style_string()}">
                            {options_text}
                        </select>'''
        return ''.join(random.sample([label_text, selector_text], 2))  # randomize label position


class Datalist(BaseHTML5Element):

    @property
    def label(self):
        return 'dropdown'

    def __init__(self):
        super().__init__()
        self.tag = 'datalist'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'list': f'datalist-{self.html_attributes["id"]}',
        }
        self.html_attributes.update(specific_attributes)

    def element_markup(self):
        label = self.generate_label()
        options = self.generate_options()
        input_markup = f'''<input {self.generate_html_attributes_string()} style="{self.generate_style_string()}"/>'''
        datalist = f'''
        <datalist id=datalist-{self.html_attributes["id"]}>
            {options}
        </datalist>'''
        return f'''<div>{''.join(random.sample([label, input_markup, datalist], 3))}</div>'''


class CheckList(BaseHTML5Element):

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def element_markup(self):
        checklist_text = self.generate_checkbox_elements()
        return f'''<div {self.generate_html_attributes_string()}>{checklist_text}</div>'''


class ColorPicker(BaseHTML5Element):
    label_needed = True

    @property
    def label(self):
        return 'colorpicker'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': 'color'
        }
        self.html_attributes.update(specific_attributes)
        self.add_unnecessary_html_attribute('value', fake.color(), 50)


class Progress(BaseHTML5Element):
    label_needed = True

    @property
    def label(self):
        return 'progressbar'

    def __init__(self):
        super().__init__()
        self.tag = 'progress'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        max_value = random.randint(0, 1000)
        value = random.randint(0, max_value)
        specific_attributes = {
            'max': max_value,
            'value': value,
            'inner_value': f'{(value / max_value) * 100} %'
        }
        self.html_attributes.update(specific_attributes)


class DateTimeInput(BaseHTML5Element):
    label_needed = True

    @property
    def label(self):
        return 'datetimeselector'

    def __init__(self):
        super().__init__()
        self.tag = 'input'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        specific_attributes = {
            'type': random.choice(['date', 'month', 'datetime-local', 'time', 'week'])
        }
        self.html_attributes.update(specific_attributes)
        self.generate_values()
        self.add_unnecessary_html_attribute('required', None, 50)

    def generate_values(self):
        min_date = self.get_random_date()
        max_date = self.get_random_date(min_date)
        value = self.get_random_date(min_date, max_date)
        format_string = '%Y-%m-%dT%H:%M'
        if self.html_attributes['type'] == 'date':
            format_string = '%Y-%m-%d'
        elif self.html_attributes['type'] == 'month':
            format_string = '%Y-%m'
        elif self.html_attributes['type'] == 'datetime-local':
            format_string = '%Y-%m-%dT%H:%M'
        elif self.html_attributes['type'] == 'time':
            min_time = self.get_random_time()
            max_time = self.get_random_time(min_time['hour'], min_time['minute'])
            value_time = self.get_random_time(min_time['hour'], min_time['minute'],
                                              max_time['hour'], max_time['minute'])
            min_date = datetime.now().replace(**min_time)
            max_date = datetime.now().replace(**max_time)
            value = datetime.now().replace(**value_time)
            format_string = '%H:%M'
        elif self.html_attributes['type'] == 'week':
            format_string = '%Y-W%W'

        self.add_unnecessary_html_attribute('min', min_date.strftime(format_string), 50)
        self.add_unnecessary_html_attribute('max', max_date.strftime(format_string), 50)
        self.add_unnecessary_html_attribute('value', value.strftime(format_string), 50)

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


class NumberInput(BaseHTML5Element):
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


class HTML5Builder(BaseHTMLBuilder):
    elements = [
        RadioButtons,
        Button,
        Range,
        Table,
        Paragraph,
        Link,
        TextField,
        TextArea,
        FileUpload,
        Selector,
        Datalist,
        CheckList,
        ColorPicker,
        Progress,
        DateTimeInput,
        NumberInput
    ]

    @property
    def framework_name(self):
        return 'html5'

    def _generate_text(self, html_text):
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
