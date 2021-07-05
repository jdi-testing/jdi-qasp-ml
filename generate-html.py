import argh

from HTMLgenerator.builders.html5_builder import HTML5Builder
from HTMLgenerator.builders.bootstrap_builder import BootstrapBuilder

builders = (HTML5Builder, )


@argh.arg('--output_dir', default="dataset/generated", help='Output directory')
@argh.arg('--num_of_pages', default=10, help="Number of pages to generate")
@argh.arg('--elements_on_page', default=40, help="Num of elements per page")
def html5(output_dir: str = 'dataset/generated', num_of_pages: int = 10, elements_on_page: int = 40):
    """Generate HTML-5 html pages"""
    HTML5Builder(num_of_pages=num_of_pages,
                 elements_on_page=elements_on_page,
                 output_path=output_dir).generate()


@argh.arg('--output_dir', default="dataset/generated", help='Output directory')
@argh.arg('--num_of_pages', default=10, help="Number of pages to generate")
@argh.arg('--elements_on_page', default=40, help="Num of elements per page")
def bootstrap(output_dir: str = 'dataset/generated', num_of_pages: int = 10, elements_on_page: int = 40):
    """Generate BOOTSTRAP html pages"""
    BootstrapBuilder(num_of_pages=num_of_pages,
                     elements_on_page=elements_on_page,
                     output_path=output_dir).generate()


parser = argh.ArghParser()
parser.add_commands([html5, bootstrap])

if __name__ == '__main__':
    parser.dispatch()
