from bs4 import BeautifulSoup


def get_script_text(script_path: str) -> str:
    with open(script_path) as f:
        return "\n".join(f.readlines())


def inject_css_selector_generator_scripts(document: str) -> str:
    doc_soup = BeautifulSoup(document, "html.parser")
    script_files_base_dir = "app/css_locators/auxiliary"
    script_files = (
        f"{script_files_base_dir}/{filename}"
        for filename in (
            "lib-finder.js",
            "lib-css-selector-generator.js",
            "generate_css_selector.js",
        )
    )
    for script_path in script_files:
        script_tag = doc_soup.new_tag("script")
        script_tag.string = get_script_text(script_path)
        doc_soup.head.append(script_tag)

    return str(doc_soup)
