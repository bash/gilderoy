import hashlib
import sys
import shutil
import sass
import os
from os import path
from .constants import *

BUF_SIZE = 65536

def output_file_name(source, file_hash):
    filename, ext = path.splitext(source)
    
    return path.basename(filename) + '-' + file_hash + ext

def output_file_path(filename):
    return path.join(PUBLIC_FOLDER, STATIC_FOLDER, filename)

def hash_file(path):
    sha1 = hashlib.sha1()

    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)

            if not data:
                break

            sha1.update(data)
    
    return sha1.hexdigest()[:10]

def hash_string(input):
    sha1 = hashlib.sha1()
    sha1.update(input.encode('utf-8'))
    return sha1.hexdigest()[:10]

def process_sass(source):
    file_stem, _ = path.splitext(source)
    css = sass.compile(filename=source, output_style='compressed')
    filename = output_file_name(file_stem + '.css', hash_string(css))
    file_path = output_file_path(filename)

    with open(file_path, 'w') as f:
        f.write(css)
    
    return filename

def process_file(source):
    filename = output_file_name(source, hash_file(source))
    file_path = output_file_path(filename)

    shutil.copy(source, file_path)

    return filename

def build_assets(config):
    assets = {}

    if 'assets' not in config:
        return {}

    static_folder = path.join(PUBLIC_FOLDER, STATIC_FOLDER)

    if not path.isdir(static_folder):
        os.mkdir(static_folder)

    for name, asset in config['assets'].items():
        source = asset['source']
        _, ext = path.splitext(source)
        
        if ext == ".scss":
            filename = process_sass(source)
        else:
            filename = process_file(source)

        assets[name] = '/' + STATIC_FOLDER + '/' + filename

    return assets
