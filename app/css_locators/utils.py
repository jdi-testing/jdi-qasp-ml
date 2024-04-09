from bs4 import BeautifulSoup


def inject_css_selector_generator_scripts(document: str) -> str:
    doc_soup = BeautifulSoup(document, "html.parser")
    doc_soup.head.extend([
        BeautifulSoup().new_tag("script", attrs={"src": s})
        for s in (
            "finder.js",
            "index.js",
            "generate_css_selector.js",
        )
    ])

    return str(doc_soup)
