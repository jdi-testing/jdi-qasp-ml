import argh

from HTMLbuilders.html5_builder import HTML5Builder
from HTMLbuilders.bootstrap_builder import BootstrapBuilder

builders = (HTML5Builder, )


def main(output='output', num_of_pages=1, elements_on_page=50):
    for HTMLBuilderClass in builders:
        html_builder = HTMLBuilderClass(num_of_pages=num_of_pages,
                                        elements_on_page=elements_on_page,
                                        output_path=output)
        html_builder.generate()


if __name__ == '__main__':
    argh.dispatch_command(main)

