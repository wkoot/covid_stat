import argparse

import fetchers

known_fetchers = ", ".join(fetchers.__all__)
arg_parser = argparse.ArgumentParser(description=f"Run a fetcher from the set of fetchers classes: {known_fetchers}")
arg_parser.add_argument('fetcher', type=str, help='fetcher class name')


# noinspection PyUnusedLocal
def run_fetcher(*args, **kwargs):
    args = arg_parser.parse_args()
    fetcher_class = getattr(fetchers, args.fetcher, None)
    if not fetcher_class:
        raise arg_parser.error(f"Unknown fetcher class: {args.fetcher}")

    fetcher = fetcher_class()
    fetcher.run()


if __name__ == "__main__":
    run_fetcher()
