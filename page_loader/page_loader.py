from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
import logging
import os
import requests
from slugify import slugify
from urllib.parse import urlparse

from requests.exceptions import MissingSchema, ConnectionError


class LoaderError(Exception):
    pass


def make_slug(url):
    """
    Returns filename slug string made from input url.

    Args:
        url (str):
            URL string.

    Returns:
        slug (str):
            Slug made from URL (lowercase letters, all symbols are
            replaced with dash).
    """
    try:
        u = urlparse(url)
    except AttributeError as e:
        logging.error(f'{url} is invalid url')
        raise LoaderError from e
    # stripping the extension from page url using os.path.splitext()
    slug = slugify(u.netloc + os.path.splitext(u.path)[0])
    return slug


def save_file(url, dir_path):
    """
    Downloads the file from target url to specified directory.

    Args:
        url: url of the target file.
        dir_path: path to the target directory to save the file.

    Returns:
        file_path: absolute path of the downloaded file.
    """
    head, ext = os.path.splitext(url)
    # if url have no extension, save file as .html
    if not ext:
        ext = '.html'
    file_path = os.path.join(dir_path, (make_slug(head) + ext))
    file_data = requests.get(url).content
    with open(file_path, "wb") as f:
        f.write(file_data)
    return file_path


def download_local_assets(soup, tag, attr, url, dir_path, page_slug):
    """
    Downloads the local assets from the BeautifulSoup object
    of the target html page.
    Saves assets to target directory and replaces `src`
    attribute with absolute path to downloaded files.

    Args:
        soup (BeautifulSoup):
            BeautifulSoup object of the target html page.
        tag (str):
            html tag of assets that need to be downloaded.
        attr (str):
            tag attribute with link to asset
            (`src` for <img> and <script>, `href` for <link>).
        url (str):
            URL of the target web page.
        dir_path (str):
            Path to the directory with target saved page.
        page_slug (str):
            Slug string made from target page url.

    Returns:
        new_soup (BeautifulSoup):
            BeautifulSoup object with `src` attribute replaced
            with absolute path to downloaded assets.
    """
    # Finding all elements with target tag and non-empty url attr
    assets = soup.find_all(tag, attrs={attr: True})
    # Creating a directory for assets if found assets with target tag
    if assets:
        assets_dir_name = f'{page_slug}_files'
        assets_dir_path = os.path.join(dir_path, assets_dir_name)
        os.makedirs(assets_dir_path, exist_ok=True)
    # Get scheme and host of the page to download assets with relative url
    scheme, host = urlparse(url).scheme, urlparse(url).netloc
    for a in assets:
        asset_url = urlparse(a.attrs.get(attr))
        # Downloading an asset it is local to the page's domain
        if (not asset_url.scheme and not asset_url.netloc) \
                or (scheme == asset_url.scheme and host == asset_url.netloc):
            # Modifying relative url to make it absolute
            asset_abs_url = asset_url._replace(
                scheme=scheme,
                netloc=host
            ).geturl()

            # save_file saves the asset and returns its' path
            asset_path = save_file(
                asset_abs_url.split('?')[0],  # remove url parameters
                assets_dir_path
            )
            # Replacing original asset url with path to downloaded file
            a.attrs[attr] = f'{assets_dir_name}/{os.path.basename(asset_path)}'
    return soup


def download(url, dir_path):
    """
    Downloads a web page and its' local assets, replaces assets URLs
    with absolute path to downloaded files in output HTML file and
    saves the resulting html file to specified directory.

    Args:
        url (str):
            URL of the target web page.
        dir_path (str):
            Path to the directory to save page.

    Returns:
        output_html_path (str):
            Absolute path to saved html file.
    """
    page_slug = make_slug(url)
    output_html_path = os.path.join(dir_path, page_slug) + ".html"
    try:
        r = requests.get(url)
    except MissingSchema as e:
        logging.error(f"Can't reach {url}: URL is incorrect")
        raise LoaderError from e
    except ConnectionError as e:
        logging.error(f"Can't reach {url}: URL is incorrect or website is down")
        raise LoaderError from e
    soup = BeautifulSoup(r.content, "html.parser")

    for tag, attr in (
            ('img', 'src'),
            ('script', 'src'),
            ('link', 'href'),
    ):
        soup = download_local_assets(soup, tag, attr, url, dir_path, page_slug)

    with open(output_html_path, "w") as f:
        formatter = HTMLFormatter(indent=4)
        f.write(soup.prettify(formatter=formatter))
    return output_html_path
