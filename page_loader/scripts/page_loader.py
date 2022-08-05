"""Page-loader script."""

import logging
import sys

from page_loader import cli, page_loader


def main():
    logging.basicConfig(filename='page_loader.log', level=logging.INFO)
    try:
        url = cli.args.url
        output = cli.args.output
        logging.info(f'Starting download of {url} page to {output}...')
        file_path = page_loader.download(url, output)
        logging.info(f'Page {url} succesfully saved to {file_path}')
        print(file_path)
    except page_loader.LoaderError:
        sys.exit(1)
    sys.exit()


if __name__ == '__main__':
    main()
