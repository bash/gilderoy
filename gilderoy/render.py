import pystache
import htmlmin
import getopt
import sys
from os import path
from datetime import date
from .constants import PAGES_FOLDER, PUBLIC_FOLDER, TEMPLATE_NAME


def render(config, assets):
    with open(TEMPLATE_NAME) as f:
        template = f.read()

    additional = {}
    if 'additional' in config:
        additional = config['additional']

    for page in config['pages']:
        page_file = path.join(PAGES_FOLDER, page['file'] + '.mustache')

        with open(page_file) as f:
            page_template = f.read()

        nav = []
        for nav_page in config['pages']:
            if 'path' in nav_page and 'title' in nav_page:
                is_active = False

                if 'path' in page:
                    is_active = (nav_page['path'] == page['path'])

                nav.append({
                    'path': nav_page['path'],
                    'title': nav_page['title'],
                    'is_active': is_active,
                })

        if 'title' in page:
            title = page['title'] + ' · ' + config['title']
        else:
            title = config['title']

        context = {
            'nav': nav,
            'config': config,
            'page': page,
            'page_file': page_file,
            'title': title,
            'year': date.today().year,
            'assets': assets,
            'additional': additional,
        }

        context['content'] = pystache.render(page_template, context)

        page_html = htmlmin.minify(
            pystache.render(template, context),
            remove_optional_attribute_quotes=False,
            remove_empty_space=True,
        )

        with open(path.join(PUBLIC_FOLDER, page['file'] + '.html'), 'w') as f:
            f.write(page_html)
