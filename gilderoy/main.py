from . import render, render_sitemap, build_assets, get_config, process_config


def main():
    raw_config = get_config()
    assets = build_assets(raw_config)
    config = process_config(raw_config, assets)

    render(config, assets)
    render_sitemap(config)
