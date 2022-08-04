from bs4 import BeautifulSoup
import os
import requests
from slugify import slugify
from urllib.parse import urlparse


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
    except AttributeError:
        print('Invalid url')
    # stripping the extension from page url using os.path.splitext()
    slug = slugify(u.netloc + os.path.splitext(u.path)[0])
    return slug


def save_img(url, dir_path):
    """Saves image to specified directory."""
    head, ext = os.path.splitext(url)
    img_path = os.path.join(dir_path, (make_slug(head) + ext))
    img_data = requests.get(url).content
    with open(img_path, "wb") as f:
        f.write(img_data)
    return img_path


def download(url, dir_path):
    """Downloads a web page by url and
    saves html file to specified directory.
    Returns full path to saved html file."""
    # Get scheme and host for downloading assets with relative url
    scheme, host = urlparse(url).scheme, urlparse(url).netloc
    page_path = os.path.join(dir_path, make_slug(url)) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    imgs = soup.find_all("img")  # find all `img` tags on the page
    if imgs:
        files_dir_name = f"{make_slug(url)}_files"  # create assets dir
        files_dir_path = os.path.join(dir_path, files_dir_name)
        os.makedirs(files_dir_path, exist_ok=True)
        for img in imgs:
            img_url = urlparse(img.attrs["src"])
            # Checking if image is local to the page's domain
            if not (img_url.scheme and img_url.netloc):
                img_full_url = img_url._replace(scheme=scheme, netloc=host).geturl()
                img_path = save_img(img_full_url, files_dir_path)
                # Replacing img url with saved img path in html
                img.attrs["src"] = f"{files_dir_name}/{os.path.basename(img_path)}"

    with open(page_path, "w") as f:
        f.write(soup.prettify())
    return page_path
