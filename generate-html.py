import argh

from HTMLgenerator.HTMLbuilders.html5_builder import HTML5Builder

builders = (HTML5Builder, )


def html5(output='output', num_of_pages=10, elements_on_page=40):
    for HTMLBuilderClass in builders:
        html_builder = HTMLBuilderClass(num_of_pages=num_of_pages,
                                        elements_on_page=elements_on_page,
                                        output_path=output)
        html_builder.generate()


if __name__ == '__main__':
    argh.dispatch_command(html5)
