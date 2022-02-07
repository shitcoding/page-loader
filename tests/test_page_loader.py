import os
from page_loader import download
import pytest
import requests_mock
import tempfile


def get_path(fixture_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', fixture_filename)


def read_fixture(filename):
    path = get_path(filename)
    with open(path, 'r') as f:
        data = f.read()
        return data.rstrip()

@pytest.fixture
def hexlet_courses_page():
    return read_fixture('ru-hexlet-io-courses.html').strip()


def test_download_page(hexlet_courses_page, requests_mock):
    requests_mock.get('https://ru.hexlet.io/courses', text=hexlet_courses_page)
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = download('https://ru.hexlet.io/courses', tmpdir)
        with open(output_path) as f:
            output = f.read().strip()
            assert output == hexlet_courses_page
        assert requests_mock.called
        assert requests_mock.call_count == 1
