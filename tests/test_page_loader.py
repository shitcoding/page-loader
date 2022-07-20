from pathlib import Path
import pytest
import requests_mock
import tempfile

from page_loader import download


def get_path(fixture_filename):
    current_dir = Path(__file__).parent.absolute()
    return current_dir / 'fixtures' / fixture_filename


def read_fixture(filename):
    fixture_path = get_path(filename)
    with open(fixture_path, 'r') as f:
        data = f.read()
        return data.rstrip()


@pytest.fixture
def realpython_page():
    return read_fixture('realpython-com.html').strip()


def test_download_page(realpython_page, requests_mock):
    # mocking the request to target page
    requests_mock.get('https://realpython.com', text=realpython_page)
    # saving target page html to temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = download('https://realpython.com', tmpdir)
        with open(output_path) as f:
            output = f.read().strip()
            # checking if saved html is the same as the html fixture
            assert output == realpython_page
        # checking that mock request has been called once
        assert requests_mock.called
        assert requests_mock.call_count == 1
