import fetchers

_country_fetchers = {}


def get_country_fetchers() -> dict:
    if _country_fetchers:
        return _country_fetchers

    for fetcher_name in fetchers.__all__:
        fetcher_class = getattr(fetchers, fetcher_name, None)
        if hasattr(fetcher_class, 'country_code'):
            _country_fetchers[fetcher_class.country_code] = fetcher_class

    return _country_fetchers
