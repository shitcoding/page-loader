import os
import requests


def make_filename(url):
    """Returns filename string made from input url."""
    url_noschema = url.split('//')[-1]
    slug = url_noschema.replace('.', '-').replace('/', '-')
    return slug + '.html'


def download(url, dir_path):
    """Downloads a web page by url and
    saves html file to specified directory.
    Returns full path to saved html file."""
    r = requests.get(url)
    file_name = make_filename(url)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'w') as f:
        f.write(r.text)
    return file_path
