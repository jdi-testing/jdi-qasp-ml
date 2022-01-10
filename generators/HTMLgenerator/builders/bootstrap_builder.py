from base_classes import BaseHTMLBuilder
import elements.bootstrap as bootstrap_elements


class BootstrapBuilder(BaseHTMLBuilder):
    elements = bootstrap_elements.elements[:]

    @property
    def framework_name(self):
        return 'bootstrap'
