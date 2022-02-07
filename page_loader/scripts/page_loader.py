"""Page-loader script."""

from page_loader import cli, page_loader


def main():
    url = cli.args.url
    output = cli.args.output
    file_path = page_loader.download(url, output)
    print(file_path)


if __name__ == '__main__':
    main()
