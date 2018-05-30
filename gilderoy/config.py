import toml


def get_config():
    with open('config.toml') as f:
        config = toml.loads(f.read())

    return config


def process_config(config, assets):
    if 'additional' in config:
        config['additional'] = process_value(config['additional'], assets)

    return config


def process_value(value, assets):
    if isinstance(value, list):
        ret = []
        for item in value:
            ret.append(process_value(item, assets))
        return ret
    elif isinstance(value, dict):
        ret = {}
        for key, val in value.items():
            ret[key] = process_value(val, assets)
        return ret
    elif isinstance(value, str) and value[:9] == "assets://":
        asset_name = value[9:]

        return assets[asset_name]

    return value
