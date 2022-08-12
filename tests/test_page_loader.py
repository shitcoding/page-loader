from filecmp import dircmp
import os
from pathlib import Path
import pytest
import requests
import requests_mock
import tempfile

from page_loader import download, LoaderError


def get_path(fixture_filename):
    current_dir = Path(__file__).parent.absolute()
    return current_dir / 'fixtures' / fixture_filename


def read_fixture(filename):
    fixture_path = get_path(filename)
    with open(fixture_path, 'r') as f:
        data = f.read()
        return data


def read_bin_fixture(filename):
    fixture_path = get_path(filename)
    with open(fixture_path, 'rb') as f:
        data = f.read()
        return data


@pytest.fixture
def fixture_page():
    return read_fixture(
        'mocks/fixture_page.html'
    ).strip()


@pytest.fixture
def expected_saved_page():
    return read_fixture(
        'expected/page-loader-hexlet-repl-co.html'
    ).strip()


TARGET_URL = 'https://page-loader.hexlet.repl.co'
MOCK_ASSETS_DIR = get_path('mocks/assets')
MOCK_ASSETS_FILENAMES = (
    ('/assets/application.css', 'application.css'),
    ('/assets/professions/nodejs.png', 'nodejs.png'),
    ('/courses', 'courses.html'),
    ('/script.js', 'script.js'),
)


def test_download_page(fixture_page, expected_saved_page, requests_mock):
    # Mocking the request to target page
    requests_mock.get(
        TARGET_URL,
        text=fixture_page,
    )

    # Mocking the requests to target page assets
    for rel_url, filename in MOCK_ASSETS_FILENAMES:
        requests_mock.get(
            f'{TARGET_URL}{rel_url}',
            content=read_bin_fixture(MOCK_ASSETS_DIR / filename),
        )

    # Saving target page to temporary directory as html file
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = download(
            TARGET_URL,
            tmpdir
        )

        # Checking that saved html file is the same as expected html
        with open(output_path) as f:
            output = f.read().strip()
            # checking if saved html is the same as the html fixture
            assert output == expected_saved_page

        # Checking that directory with saved assets exists
        saved_assets_dir = f'{output_path.rstrip(".html")}_files'
        assert os.path.exists(saved_assets_dir)


        # Checking that saved assets are the same as expected
        cmp = dircmp(MOCK_ASSETS_DIR, saved_assets_dir)
        assert not cmp.diff_files


def test_download_incorrect_url():
    """
    Downloading from incorrect url should raise LoaderError exception.
    """
    with pytest.raises(LoaderError):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = download(
                'incorrect_url',
                tmpdir
            )


def test_download_site_unavailable(requests_mock):
    """
    Downloading from not responding website should raise an exception.
    """
    # Mocking the request to target page
    requests_mock.get(
        TARGET_URL,
        exc=requests.exceptions.ConnectTimeout,
    )
    with pytest.raises(LoaderError):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = download(
                TARGET_URL,
                tmpdir
            )


def test_download_non_existent_page(requests_mock):
    """
    Website returning 404 status code.
    """
    # Mocking the request to target page
    requests_mock.get(
        TARGET_URL,
        text='This page does not exist!',
        status_code=404,
    )

    with pytest.raises(LoaderError):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = download(
                TARGET_URL,
                tmpdir
            )
