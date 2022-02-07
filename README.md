[![Maintainability](https://api.codeclimate.com/v1/badges/5fe3e24fd57b9b508963/maintainability)](https://codeclimate.com/github/shitcoding/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5fe3e24fd57b9b508963/test_coverage)](https://codeclimate.com/github/shitcoding/python-project-lvl3/test_coverage)
[![Python CI](https://github.com/shitcoding/python-project-lvl3/actions/workflows/pyci.yml/badge.svg)](https://github.com/shitcoding/python-project-lvl3/actions/workflows/pyci.yml)
[![Actions Status](https://github.com/shitcoding/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/shitcoding/python-project-lvl3/actions)
---
# `page-downloader` script
Downloads a target web page with all its resourses and saves it to specified directory (default: current directory).

## Installation
```sh
cd ~/Downloads
git clone https://github.com/shitcoding/python-project-lvl3
cd python-project-lvl3
make package-install
```
[![asciicast](https://asciinema.org/a/VFvA2C8SzU8cTGalZbWbGe8HS.svg)](https://asciinema.org/a/VFvA2C8SzU8cTGalZbWbGe8HS)


## Usage
```sh
$ page-loader --help
usage: page_loader [-h] [-o OUTPUT] url

Downloads a web page

positional arguments:
  url                   URL of the web page you want to download

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to output directory (Default: current directory)
```

[![asciicast](https://asciinema.org/a/pwcyRLWNjKLVEDCeejndKMFdZ.svg)](https://asciinema.org/a/pwcyRLWNjKLVEDCeejndKMFdZ)
