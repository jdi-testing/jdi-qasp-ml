import sys

from html5_generator import HTML5Builder

if __name__ == '__main__':
    output_path = 'output'
    num_of_pages = 1
    elements_on_page = 50

    if len(sys.argv) > 1:
        output_path = sys.argv[1]

    if len(sys.argv) > 2:
        num_of_pages = int(sys.argv[2])

    if len(sys.argv) > 3:
        num_of_elements = int(sys.argv[3])

    for HTMLBuilderClass in (HTML5Builder, ):
        html_builder = HTMLBuilderClass(num_of_pages=num_of_pages,
                                        elements_on_page=elements_on_page,
                                        output_path=output_path)
        html_builder.generate()
