import argparse

from util.countries import get_country_fetchers


# noinspection PyUnusedLocal
def run_fetcher(*args, **kwargs):
    country_fetchers = get_country_fetchers()
    fetcher_str_set = ", ".join(country_fetchers.keys())

    arg_parser = argparse.ArgumentParser(description=f"Run a fetcher from the set of fetchers: {fetcher_str_set}")
    arg_parser.add_argument('fetcher', type=str.upper, help='Fetcher ISO 3166-1 alpha-2 code')

    args = arg_parser.parse_args()
    if args.fetcher not in country_fetchers:
        raise arg_parser.error(f"Unknown fetcher class: {args.fetcher}")

    fetcher = country_fetchers[args.fetcher]()
    fetcher.run()


if __name__ == "__main__":
    run_fetcher()
