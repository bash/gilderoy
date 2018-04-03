import toml

from . import render, build_assets

def main():
    with open('config.toml') as f:
        config = toml.loads(f.read())

    render(config, build_assets(config))
