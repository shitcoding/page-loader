test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report=xml

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

install:
	poetry install

build: check
	-@rm ./dist/* 2> /dev/null
	poetry build

package-install: install build
	python3 -m pip install --user dist/*.whl

.PHONY:	test test-coverage lint selfcheck check install build package-install
