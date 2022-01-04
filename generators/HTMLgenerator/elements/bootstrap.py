import random
import string

import faker

from base_classes import BaseElement
from elements.html5 import Button as HTML5Button, Span, Form, Input, HorizontalLine, Header, Option
from elements.html5 import Paragraph, Label, Link, OrderedList, ListItem, Div, UnorderedList
from service import generate_uuid, border_properties, bootstrap_button_styles

fake = faker.Faker()

bg_colors = ['bg-primary', 'bg-secondary', 'bg-success', 'bg-danger',
             'bg-warning', 'bg-info', 'bg-light', 'bg-dark', 'bg-white', 'bg-transparent']


class BootstrapBaseElement(BaseElement):
    """Represents base bootstrap elements class will be constructed from
    main class and randomly chosen classes from each category of available classes.
    Tag also is chosen randomly from list of available tags"""
    available_tags = []
    available_classes = {}
    main_class = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_tag()
        self.html_attributes['class'] = self.generate_class_name()
        self.html_attributes['name'] = generate_uuid()
        self.label_first = False
        self.label_margin = None

        self.add_specific_attributes()
        self.html_attributes.update(kwargs)

    @property
    def label(self):
        return 'n/a'

    def markup(self):
        return super().markup(self.label_margin)

    def add_specific_attributes(self):
        self.add_unnecessary_html_attribute('disabled', True, 30)

    def randomize_styling(self):
        self.style_attributes.update({
            'color': fake.color(hue=random.choice(['blue', 'monochrome', 'red', 'green']),
                                luminosity='dark'),
            'font-size': f"{random.randint(14, 28)}px",
        })

    def generate_class_name(self):
        """Generates class name using main_class and available_classes"""
        classes = [self.main_class, generate_uuid()]

        for k, v in self.available_classes.items():
            if random.randint(0, 100) < k[1]:
                classes.append(random.choice(v))
        return ' '.join(classes)

    def generate_tag(self):
        """Chooses between available tags for this element"""
        if self.tag == '' and self.available_tags:
            self.tag = random.choice(self.available_tags)


class BootstrapBaseControlDiv(BootstrapBaseElement):
    available_tags = ['div']
    inline_class_name = ''
    elements_collection = []

    def __init__(self, input_element_class=None, is_inline=None, **kwargs):
        self.is_inline = is_inline
        super().__init__(**kwargs)
        if input_element_class is None:
            input_element_class = random.choice(self.elements_collection)
        self.nested_elements.append(input_element_class(**kwargs))

    def generate_class_name(self):
        classes = [self.main_class, generate_uuid()]
        if self.is_inline is None:
            for k, v in self.available_classes.items():
                if random.randint(0, 100) < k[1]:
                    classes.append(random.choice(v))
        else:
            if self.is_inline:
                classes.append(self.inline_class_name)
        return ' '.join(classes)


class Badge(BootstrapBaseElement):
    available_tags = ['span', 'a']
    available_classes = {
        ('style', 100): ['badge-primary', 'badge-secondary', 'badge-success',
                         'badge-danger', 'badge-warning', 'badge-warning',
                         'badge-light', 'badge-dark'],
        ('modifiers', 50): ['badge-pill']
    }
    main_class = 'badge'

    @property
    def label(self):
        if self.tag == 'a':
            return 'link'
        else:
            return 'n/a'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        if self.tag == 'a':
            self.html_attributes['href'] = '#'


class Spinner(BootstrapBaseElement):
    available_tags = ['div']
    available_classes = {
        ('type', 100): ['spinner-border', 'spinner-grow', ],
        ('style', 100): ['text-primary', 'text-secondary', 'text-success',
                         'text-danger', 'text-warning', 'text-warning',
                         'text-light', 'text-dark'],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        span = Span(attr_class='sr-only')
        span.html_attributes['inner_value'] = fake.word()
        self.nested_elements.append(span)


class Button(BootstrapBaseElement):
    available_tags = ['button', 'a', 'input']
    available_classes = {
        ('size', 50): ('btn-lg', 'btn-sm', ''),
        ('block', 15): ('btn-block',),
        ('style', 100): bootstrap_button_styles()
    }

    main_class = 'btn'

    @property
    def label(self):
        if self._label is not None:
            return self._label
        else:
            return 'button'

    def __init__(self, **kwargs):
        self.include_badge = random.randint(0, 10) < 4
        self.include_spinner = random.randint(0, 10) < 4
        super().__init__(**kwargs)

    def add_specific_attributes(self):
        super().add_specific_attributes()

        if self.tag != 'input':
            self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(1, 3))

        if self.tag == 'input':
            self.html_attributes['type'] = random.choice(['button', 'submit', 'reset'])
            if self.html_attributes['type'] == 'button':
                self.html_attributes['value'] = fake.word()
            elif self.html_attributes['type'] == 'submit':
                self._label = 'submit'
        elif self.tag == 'a':
            self.html_attributes['role'] = 'button'

        if self.tag != 'input' and self.include_badge:
            badge = Badge()
            if self.tag == 'a':
                badge.tag = 'span'
            badge.html_attributes['inner_value'] = random.choice([*list(range(10)), fake.word()])
            self.html_attributes['inner_value'] = ' '.join([self.html_attributes['inner_value'], badge.markup()])

        if self.tag != 'input' and self.include_spinner:
            spinner = Spinner()
            self.html_attributes['inner_value'] = ' '.join([spinner.markup(), self.html_attributes['inner_value']])


class FormCheckInput(BootstrapBaseElement):
    available_classes = {
        ('control', 100): ('form-check-input',),
        ('position', 60): ('pull-right',),
    }

    available_tags = ['input']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label_first = random.randint(0, 10) > 5
        if self.label_first:
            self.label_margin = '10px'
        self.label_element = Label(attr_for=self.html_attributes['id'], label=self.label)


class FormCheckbox(FormCheckInput):
    @property
    def label(self):
        return 'checkbox'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['type'] = 'checkbox'
        self.add_unnecessary_html_attribute('checked', True, 30)


class FormRadioButton(FormCheckInput):
    @property
    def label(self):
        return 'radiobutton'

    def add_specific_attributes(self):
        super(FormRadioButton, self).add_specific_attributes()
        self.html_attributes['type'] = 'radio'


def form_check_inputs():
    return FormCheckbox, FormRadioButton


class CheckList(BootstrapBaseElement):
    available_tags = ['div']
    available_classes = {
        ('required', 100): ['checklist']
    }

    def randomize_styling(self):
        super().randomize_styling()
        self.style_attributes.update(border_properties())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        inline_list = random.randint(0, 10) > 8
        # FormCheck contains 2 types of elements therefore i put it here twice to equal chance
        element_class = random.choice((FormCheck, FormCheck, CustomControlSwitch))
        if element_class == FormCheck:
            input_element_class = random.choice(form_check_inputs())
        else:
            input_element_class = Switch
        for i in range(random.randint(3, 10)):
            self.nested_elements.append(
                element_class(input_element_class, inline_list, name=self.html_attributes['name']))

    def add_specific_attributes(self):
        pass


class Switch(BootstrapBaseElement):
    available_classes = {
    }
    main_class = 'custom-control-input'
    available_tags = ['input']

    @property
    def label(self):
        return 'checkbox'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_element = Label(attr_for=self.html_attributes['id'],
                                   label=self.label, attr_class='custom-control-label')

    def add_specific_attributes(self):
        self.html_attributes['type'] = 'checkbox'
        self.add_unnecessary_html_attribute('disabled', True, 5)
        self.add_unnecessary_html_attribute('checked', True, 50)


class FormCheck(BootstrapBaseControlDiv):
    inline_class_name = 'form-check-inline'
    available_classes = {
        ('alignment', 50): [inline_class_name]
    }
    main_class = 'form-check'
    elements_collection = form_check_inputs()


class CustomControlSwitch(BootstrapBaseControlDiv):
    inline_class_name = 'custom-control-inline'
    available_classes = {
        ('alignment', 50): [inline_class_name]
    }
    elements_collection = (Switch,)
    main_class = 'custom-control custom-switch'

    def add_specific_attributes(self):
        pass


class Alert(BootstrapBaseElement):
    main_class = 'alert'
    available_tags = ['div']
    available_classes = {
        ('context', 100): ['alert-primary', 'alert-secondary', 'alert-success', 'alert-danger',
                           'alert-warning', 'alert-info', 'alert-light', 'alert-dark'],

    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        include_link = random.randint(0, 10) > 3
        if include_link:
            link = Link(attr_class='alert-link')
            self.nested_elements.append(link)

        for _ in range(random.randint(1, 2)):
            paragraph = Paragraph()
            self.nested_elements.append(paragraph)

        random.shuffle(self.nested_elements)

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['role'] = 'alert'


class Breadcrumb(BootstrapBaseElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = 'nav'
        link_list = OrderedList(attr_class='breadcrumb')
        self.nested_elements.append(link_list)

        for _ in range(random.randint(2, 7)):
            if random.randint(0, 10) > 7:
                li_classname = 'breadcrumb-item active'
            else:
                li_classname = 'breadcrumb-item'
            link_list.nested_elements.append(ListItem(attr_class=li_classname, generate_text=True))
        random.choice(link_list.nested_elements).html_attributes['aria-current'] = 'page'  # set current page

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['aria-label'] = 'breadcrumb'


class NavDropdown(BootstrapBaseElement):
    available_tags = ['li']
    main_class = 'nav-item dropdown'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        link = Link(label='dropdown', attr_class='nav-link dropdown-toggle')
        link.html_attributes['data-toggle'] = 'dropdown'
        link.html_attributes['href'] = '#'
        link.html_attributes['role'] = 'button'
        link.html_attributes['aria-haspopup'] = 'true'
        link.html_attributes['aria-expanded'] = 'false'
        self.nested_elements.append(link)

        dropdown_menu = Div(attr_class='dropdown-menu', label='dropdown')
        self.nested_elements.append(dropdown_menu)
        for _ in range(random.randint(1, 8)):
            generate_divider = random.randint(0, 10) < 3
            if generate_divider:
                divider = Div(attr_class='dropdown-divider')
                dropdown_menu.nested_elements.append(divider)
                continue

            item = Link(attr_class='dropdown-item', href='#')
            dropdown_menu.nested_elements.append(item)


class Navigation(BootstrapBaseElement):
    available_tags = ['nav', 'ul']
    main_class = 'nav'
    available_classes = {
        ('alignment', 60): ('justify-content-center', 'justify-content-end', 'flex-column',
                            'nav-fill', 'nav-justified'),
        ('type', 30): ('nav-tabs', 'nav-pills',)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        wrap_in_list_item = ((bool(random.randint(0, 1))
                              and self.tag == 'ul')
                             or 'nav-tabs' in self.html_attributes['class']
                             or 'nav-pills' in self.html_attributes['class'])

        is_tab = 'nav-tabs' in self.html_attributes['class']
        is_pill = 'nav-pills' in self.html_attributes['class']

        for _ in range(random.randint(2, 7)):
            if is_tab or is_pill:
                generate_dropdown = random.randint(0, 10) < 3
                if generate_dropdown:
                    dropdown = NavDropdown()
                    self.nested_elements.append(dropdown)
                    continue

            accessibility_class_name = ''
            if random.randint(0, 10) < 6:
                accessibility_class_name = random.choice(['active', 'disabled'])
            if is_tab:
                link = Link(label='tab', attr_class=' '.join(['nav-link', accessibility_class_name]))
            else:
                link = Link(attr_class=' '.join(['nav-link', accessibility_class_name]))
            link.nested_elements.clear()

            if wrap_in_list_item:
                if is_tab:
                    item = ListItem(label='tab', attr_class='nav-item')
                else:
                    item = ListItem(attr_class='nav-item')
                item.nested_elements.append(link)
                self.nested_elements.append(item)
            else:
                self.nested_elements.append(link)

    def randomize_styling(self):
        super().randomize_styling()
        self.style_attributes.update(border_properties())


class InputGroup(BootstrapBaseElement):
    available_tags = ['div']
    main_class = 'input-group'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        prepend = Div(attr_class='input-group-prepend', randomize_styling=False)
        span = Span(attr_class='input-group-text', randomize_styling=False)
        span.html_attributes['inner_value'] = random.choice(['@', fake.word()])
        prepend.nested_elements.append(span)

        input_elements = []
        for _ in range(1, 4):
            input_element = Input(attr_class='form-control', type='text', label='textfield', randomize_styling=False)
            input_element.html_attributes['aria-describedby'] = span.html_attributes['id']
            try:
                input_element.html_attributes['aria-label'] = input_element.html_attributes['placeholder']
            except KeyError:
                pass
            input_elements.append(input_element)

        prepend_first = random.randint(0, 10) < 5
        if prepend_first:
            self.nested_elements.append(prepend)
            self.nested_elements.extend(input_elements)
        else:
            self.nested_elements.extend(input_elements)
            self.nested_elements.append(prepend)


class SearchForm(Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_attributes['class'] = 'form-inline my-2 my-lg-0'
        search_input = Input(attr_class='form-control mr-sm-2', type='search')
        search_input.html_attributes['aria-label'] = 'Search'
        button = Button(type='submit', label='submit')
        self.nested_elements.append(search_input)
        self.nested_elements.append(button)


class NavBar(BootstrapBaseElement):
    available_tags = ['nav']
    main_class = 'navbar'
    available_classes = {
        ('expanding', 100): ['navbar-expand-sm', 'navbar-expand-md',
                             'navbar-expand-xl', 'navbar-expand-lg'],
        ('color', 100): ['navbar-light', 'navbar-dark'],
        ('background', 100): bg_colors,
        ('position', 30): ['fixed-top', 'fixed-bottom', 'sticky-top']
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_elements()

    def create_elements(self):
        link = Link(attr_class='navbar-brand')
        body = Div(attr_class='collapse navbar-collapse')
        toggler = HTML5Button(randomize_styling=False, attr_class='navbar-toggler', type='button')
        toggler.html_attributes['data-toggle'] = 'collapse'
        toggler.html_attributes['data-target'] = f'#{body.html_attributes["id"]}'
        toggler.html_attributes['aria-controls'] = body.html_attributes['id']
        toggler.html_attributes['aria-expanded'] = 'false'
        toggler.html_attributes['aria-label'] = 'Toggle navigation'
        span = Span(attr_class='navbar-toggler-icon')
        toggler.nested_elements.append(span)
        del toggler.html_attributes['inner_value']

        content_as_ul = bool(random.randint(0, 1))
        if content_as_ul:
            content = UnorderedList(attr_class='navbar-nav')
        else:
            content = Div(attr_class='navbar-nav')
        body.nested_elements.append(content)
        for _ in range(random.randint(2, 7)):

            link_class = 'nav-link' if content_as_ul else 'nav-item nav-link'
            accessibility_class_name = ''
            if random.randint(0, 10) < 6:
                accessibility_class_name = random.choice(['active', 'disabled'])

            generate_dropdown = random.randint(0, 10) < 3
            if generate_dropdown:
                link = NavDropdown()
            else:
                link = Link(attr_class=' '.join([link_class, accessibility_class_name]), randomize_styling=False)
            if content_as_ul:
                list_item = ListItem(attr_class=' '.join(['nav-item', accessibility_class_name]))
                list_item.nested_elements.append(link)
                content.nested_elements.append(list_item)
            else:
                content.nested_elements.append(link)
        shuffled_list = random.sample([link, toggler], 2)
        self.nested_elements.extend(shuffled_list)
        self.nested_elements.append(body)

        generate_search_field = random.randint(0, 10) < 2
        if generate_search_field:
            form = SearchForm()
            self.nested_elements.append(form)

        generate_input_group = random.randint(0, 10) < 2
        if generate_input_group:
            input_group = InputGroup()
            self.nested_elements.append(input_group)


class Pagination(BootstrapBaseElement):
    available_tags = ['ul']
    available_classes = {
        ('alignment', 40): ('justify-content-center', 'justify-content-end'),
        ('size', 40): ('pagination-lg', 'pagination-sm')
    }
    main_class = 'pagination'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(random.randint(2, 9)):
            accessibility_class_name = ''
            if random.randint(0, 10) < 6:
                accessibility_class_name = random.choice(['active', 'disabled'])
            item = ListItem(attr_class=' '.join(['page-item', accessibility_class_name]), randomize_styling=False)
            link = Link(attr_class='page-link', randomize_styling=False)
            link.html_attributes['inner_value'] = i
            item.nested_elements.append(link)
            self.nested_elements.append(item)

    def markup(self):
        return f'<nav aria-label="Pagination">{super().markup()}</nav>'


class Progress(BootstrapBaseElement):
    available_tags = ['div']
    main_class = 'progress'

    @property
    def label(self):
        return 'progressbar'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        is_multiple = random.randint(0, 10) < 3
        if is_multiple:
            for _ in range(random.randint(2, 5)):
                progressbar = ProgressBar()
                self.nested_elements.append(progressbar)
        else:
            self.nested_elements.append(ProgressBar())

    def randomize_styling(self):
        self.style_attributes['margin'] = '10px'
        if random.randint(0, 10) < 3:
            self.style_attributes['height'] = f'{random.randint(1, 25)}px'


class ProgressBar(BootstrapBaseElement):
    available_tags = ['div']
    available_classes = {
        ('background', 60): ['bg-success', 'bg-info', 'bg-warning', 'bg-danger'],
        ('stripped', 50): ['progress-bar-striped'],
        ('animated', 50): ['progress-bar-animated'],
    }
    main_class = 'progress-bar'

    @property
    def label(self):
        return 'progressbar'

    def __init__(self, **kwargs):
        self.min_value = random.randint(0, 99)
        self.max_value = random.randint(self.min_value + 1, 100)
        self.current_value = random.randint(self.min_value, self.max_value)
        self.percentage = round(((self.current_value - self.min_value) / (self.max_value - self.min_value)) * 100, 2)
        super().__init__(**kwargs)
        self.html_attributes['role'] = 'progressbar'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['aria-valuemin'] = self.min_value
        self.html_attributes['aria-valuemax'] = self.max_value
        self.html_attributes['aria-valuenow'] = self.current_value
        self.add_unnecessary_html_attribute('inner_value', f'{self.percentage} %', 60)

    def randomize_styling(self):
        self.style_attributes['width'] = f'{self.percentage}%'


class Jumbotron(BootstrapBaseElement):
    available_tags = ['div']
    available_classes = {
        ('fluid', 50): ['jumbotron-fluid']
    }
    main_class = 'jumbotron'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(2, 5):
            element_class = random.choice([Paragraph, Link, HorizontalLine, Button, Header])
            self.nested_elements.append(element_class())


class Collapse(BootstrapBaseElement):
    available_tags = ['a', 'button']
    available_classes = {
        ('style', 100): bootstrap_button_styles()
    }
    main_class = 'btn'

    @property
    def label(self):
        return 'button'

    def __init__(self, **kwargs):
        self.collapsable_element = Div(attr_class='collapse')
        # collapse with tag "button" doesn't expand elements with numbers in id
        self.collapsable_element.html_attributes['id'] = ''.join(random.sample(string.ascii_lowercase, 8))
        paragraph = Paragraph()
        self.collapsable_element.nested_elements.append(paragraph)

        super().__init__(**kwargs)

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.word()
        self.html_attributes['data-toggle'] = 'collapse'
        self.html_attributes['aria-expanded'] = 'false'
        self.html_attributes['aria-controls'] = self.collapsable_element.html_attributes['id']
        target = f'#{self.collapsable_element.html_attributes["id"]}'
        if self.tag == 'a':
            self.html_attributes['href'] = target
            self.html_attributes['role'] = 'button'
        elif self.tag == 'button':
            self.html_attributes['type'] = 'button'
            self.html_attributes['data-target'] = target

    def markup(self):
        return f'{super().markup()}\n{self.collapsable_element.markup()}'


class DropdownMenu(BootstrapBaseElement):
    available_tags = ['div']
    main_class = 'dropdown-menu'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(random.randint(2, 8)):
            generate_divider = random.randint(0, 10) < 2
            if generate_divider:
                self.nested_elements.append(Div(attr_class='dropdown-divider'))
            else:
                link_class = random.choice([Link, HTML5Button])
                accessibility_class_name = ''
                if random.randint(0, 10) < 3:
                    accessibility_class_name = random.choice(['active', 'disabled'])
                link = link_class(attr_class=' '.join(['dropdown-item', accessibility_class_name]), label='link',
                                  randomize_styling=False)
                self.nested_elements.append(link)


class DropdownButton(BootstrapBaseElement):
    available_tags = ['button', 'a']
    available_classes = {
        ('style', 100): bootstrap_button_styles(),
        ('split', 100): ['dropdown-toggle-split'],
        ('size', 80): ['btn-lg', 'btn-sm']
    }
    main_class = 'btn dropdown-toggle'

    @property
    def label(self):
        return 'dropdown'

    def __init__(self, **kwargs):
        self.splitted = random.randint(0, 10) < 4
        super().__init__(**kwargs)
        self.dropdown_menu = DropdownMenu(attr_class='dropdown-menu')
        self.dropdown_menu.html_attributes['aria-labelledby'] = self.html_attributes['id']
        if self.splitted:
            self.button = Button()

    def add_specific_attributes(self):
        super().add_specific_attributes()
        if not self.splitted:
            self.html_attributes['inner_value'] = fake.word()

        self.html_attributes['data-toggle'] = 'dropdown'
        self.html_attributes['aria-haspopup'] = 'true'
        self.html_attributes['aria-expanded'] = 'false'
        if self.tag == 'a':
            self.html_attributes['href'] = '#'
            self.html_attributes['role'] = 'button'
        elif self.tag == 'button':
            self.html_attributes['type'] = 'button'

    def markup(self):
        direction = random.choice(['dropup', 'dropright', 'dropleft', ''])
        if self.splitted:
            return f'<div class="btn-group {direction}">{self.button.markup()}\n{super().markup()}' \
                   f'\n{self.dropdown_menu.markup()}</div>'
        else:
            return f'<div class="dropdown {direction}">{super().markup()}\n{self.dropdown_menu.markup()}</div>'


class Range(BootstrapBaseElement):
    available_tags = ['input']

    main_class = 'custom-range'

    def __init__(self, **kwargs):
        self.min = random.randint(0, 90)
        self.max = random.randint(self.min + 1, 100)
        self.value = random.randint(self.min, self.max)
        super().__init__(**kwargs)
        self.label_element = Label(attr_for=self.html_attributes['id'], label=self.label)

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['type'] = 'range'
        self.add_unnecessary_html_attribute('min', self.min, 60)
        self.add_unnecessary_html_attribute('max', self.max, 60)
        self.add_unnecessary_html_attribute('value', self.value, 60)
        self.add_unnecessary_html_attribute('step', random.randint(1, 10) / 10, 50)


class ScrollSpy(BootstrapBaseElement):
    available_tags = ['div']

    main_class = 'scrollspy-example'

    def __init__(self, **kwargs):
        self.list_anchors = Div(attr_class='list-group')
        super().__init__(**kwargs)

        for i in range(random.randint(2, 8)):
            link = Link(attr_class='list-group-item list-group-item-action')
            link.html_attributes['href'] = f'#list-item-{link.html_attributes["id"]}'
            self.list_anchors.nested_elements.append(link)

        for link in self.list_anchors.nested_elements:
            header = Header()
            header.html_attributes['id'] = f'list-item-{link.html_attributes["id"]}'
            self.nested_elements.append(header)
            self.nested_elements.append(Paragraph())

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['data-spy'] = 'scroll'
        self.html_attributes['data-target'] = f'#{self.list_anchors.html_attributes["id"]}'
        self.html_attributes['data-offset'] = 0

    def randomize_styling(self):
        super().randomize_styling()
        self.style_attributes['position'] = 'relative'
        self.style_attributes['height'] = '200px'
        self.style_attributes['margin-top'] = '.5'
        self.style_attributes['margin-top'] = '.5 rem'
        self.style_attributes['overflow-x'] = 'auto'
        self.style_attributes['overflow-y'] = 'scroll'
        self.style_attributes['display'] = 'block'

    def markup(self):
        return f'{self.list_anchors.markup()}\n{super().markup()}'


class BootstrapForm(BootstrapBaseElement):
    available_tags = ['form']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(2, 7):
            self.nested_elements.append(FormGroup())

    def randomize_styling(self):
        self.style_attributes.update(border_properties())


class FormGroup(BootstrapBaseElement):
    available_tags = ['div']

    main_class = 'form-group'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        class_of_element = random.choice(form_controls)
        self.element = class_of_element()
        self.nested_elements.append(self.element)
        generate_tooltip = random.randint(0, 10) < 4
        if generate_tooltip:
            self.nested_elements.append(Small())

    def randomize_styling(self):
        super().randomize_styling()
        self.style_attributes.update(border_properties())


class FormControl(BootstrapBaseElement):
    main_class = 'form-control'
    available_classes = {
        ('sizing', 50): ['form-control-lg', 'form-control-sm']
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_element = Label(attr_for=self.html_attributes['id'])

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.add_unnecessary_html_attribute('readonly', True, 30)


class Small(BootstrapBaseElement):
    available_tags = ['small']
    main_class = 'form-text text-muted'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['inner_value'] = fake.sentence(nb_words=random.randint(3, 12))


class FormSelect(FormControl):
    available_tags = ['select']

    @property
    def label(self):
        return 'selector'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(random.randint(1, 5)):
            self.nested_elements.append(Option())

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.add_unnecessary_html_attribute('multiple', True, 40)


class FormTextfield(FormControl):
    available_tags = ['input']
    self_closing_tag = True

    @property
    def label(self):
        return 'textfield'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['type'] = random.choice(['email', 'password'])
        self.add_unnecessary_html_attribute('placeholder', fake.sentence(nb_words=random.randint(1, 3)), 60)


class FormTextArea(BootstrapBaseElement):
    available_tags = ['textarea']
    main_class = 'form-control'

    @property
    def label(self):
        return 'textarea'

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['rows'] = random.randint(1, 5)
        self.html_attributes['cols'] = random.randint(5, 20)


class FormRange(FormControl):
    main_class = 'form-control-range'
    available_tags = ['input']

    @property
    def label(self):
        return 'range'

    def __init__(self, **kwargs):
        self.min = random.randint(0, 90)
        self.max = random.randint(self.min + 1, 100)
        self.value = random.randint(self.min, self.max)
        super().__init__(**kwargs)

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['type'] = 'range'
        self.add_unnecessary_html_attribute('min', self.min, 60)
        self.add_unnecessary_html_attribute('max', self.max, 60)
        self.add_unnecessary_html_attribute('value', self.value, 60)
        self.add_unnecessary_html_attribute('step', random.randint(1, 10) / 10, 50)


class FileBrowser(BootstrapBaseElement):
    available_tags = ['input']
    main_class = 'custom-file-input'

    @property
    def label(self):
        return 'fileinput'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_element = Label(
            attr_for=self.html_attributes['id'],
            attr_class='custom-file-label',
            label=self.label,
        )

    def add_specific_attributes(self):
        super().add_specific_attributes()
        self.html_attributes['type'] = 'file'

    def markup(self):
        return f'<div class="custom-file">{super().markup()}</div>'


form_controls = [FormTextfield, FormCheck, FormSelect, FormTextArea, FormRange, FileBrowser]
elements = [
    Button,
    FormCheck,
    CheckList,
    CustomControlSwitch,
    Alert,
    Breadcrumb,
    Navigation,
    NavBar,
    Pagination,
    Progress,
    Jumbotron,
    Collapse,
    DropdownButton,
    Range,
    InputGroup,
    Spinner,
    ScrollSpy,
    BootstrapForm,
]
