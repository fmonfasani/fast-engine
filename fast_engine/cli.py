import argparse

from . import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(description="fast-engine CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
    return args

if __name__ == "__main__":
    main()
