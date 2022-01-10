import random

from base_classes import BaseHTMLBuilder
import elements.html5 as html5_elements


class HTML5Builder(BaseHTMLBuilder):

    elements = html5_elements.elements[:]

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
                                {element_class().markup()}</div>'''
            else:
                body += element_class().markup()
        output_text = html_text.replace("%BODY%", body)
        return output_text
