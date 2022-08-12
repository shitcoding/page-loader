"""Page-loader script."""

import logging
from progress.bar import IncrementalBar
import sys

from page_loader import cli, page_loader


def main():
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler('page_loader.log'),
            logging.StreamHandler(sys.stdout),
        ],
    )
    try:
        url = cli.args.url
        output = cli.args.output
        logging.info(f'requested url: {url}')
        logging.info(f'output path: {output}')

        with IncrementalBar('Downloading:', max=4) as bar:
            file_path = page_loader.download(url, output)
            for i in range(4):
                bar.next()

        logging.info(f"Page was downloaded as '{file_path}'")
    except page_loader.LoaderError:
        sys.exit(1)
    sys.exit()


if __name__ == '__main__':
    main()
