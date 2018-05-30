from xml.etree.cElementTree import Element, ElementTree, SubElement
from .constants import PUBLIC_FOLDER
from os import path


def render_sitemap(config):
    root = Element(
        'urlset', {'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})

    for page in config['pages']:
        if not 'path' in page:
            continue

        url_element = SubElement(root, 'url')
        loc_element = SubElement(url_element, 'loc')

        loc_element.text = config['url_prefix'] + page['path']

    tree = ElementTree(root)

    tree.write(path.join(PUBLIC_FOLDER, 'sitemap.xml'),
               xml_declaration=True, encoding='utf-8')
