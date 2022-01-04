import logging

import argh

from builders.html5_builder import HTML5Builder
from builders.bootstrap_builder import BootstrapBuilder

import os
import sys

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml", "generators"))

builders = (HTML5Builder, BootstrapBuilder)


@argh.arg("--output_dir", default="dataset/generated", help="Output directory")
@argh.arg("--num_of_pages", default=10, help="Number of pages to generate")
@argh.arg("--elements_on_page", default=40, help="Num of elements per page")
def all(
    output_dir: str = "dataset/generated",
    num_of_pages: int = 10,
    elements_on_page: int = 40,
):
    """Generate html pages using all available frameworks"""
    for HTMLBuilderClass in builders:
        html_builder = HTMLBuilderClass(
            num_of_pages=num_of_pages,
            elements_on_page=elements_on_page,
            output_path=output_dir,
        )
        html_builder.generate()


@argh.arg("--output_dir", default="dataset/generated", help="Output directory")
@argh.arg("--num_of_pages", default=10, help="Number of pages to generate")
@argh.arg("--elements_on_page", default=40, help="Num of elements per page")
def html5(
    output_dir: str = "dataset/generated",
    num_of_pages: int = 10,
    elements_on_page: int = 40,
):
    """Generate HTML-5 html pages"""
    HTML5Builder(
        num_of_pages=num_of_pages,
        elements_on_page=elements_on_page,
        output_path=output_dir,
    ).generate()


@argh.arg(
    "--output_dir", default="dataset/generated", help="Output directory"
)
@argh.arg("--num_of_pages", default=10, help="Number of pages to generate")
@argh.arg("--elements_on_page", default=40, help="Num of elements per page")
def bootstrap(
    output_dir: str = "dataset/generated",
    num_of_pages: int = 10,
    elements_on_page: int = 40,
):
    """Generate BOOTSTRAP html pages"""
    BootstrapBuilder(
        num_of_pages=num_of_pages,
        elements_on_page=elements_on_page,
        output_path=output_dir,
    ).generate()


parser = argh.ArghParser()
parser.add_commands([html5, bootstrap, all])

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S",
        level=logging.INFO,
    )
    parser.dispatch()
