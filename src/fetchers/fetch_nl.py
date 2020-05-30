from time import sleep

from util import iter_chunks, week_to_first_last_dates
from .base import BaseFetcher


class FetcherNL(BaseFetcher):
    """
    Source data - https://data.overheid.nl/dataset/309-overledenen--geslacht-en-leeftijd--per-week
    """
    country_code = 'NL'  # Netherlands
    intervals = {}

    def prepare(self):
        time_interval_options_api = 'https://opendata.cbs.nl/ODataApi/odata/70895ned/Perioden'
        intervals = self.session.get(time_interval_options_api).json()['value']
        self.intervals = {period['Key']: period['Title'] for period in intervals if period['Key'].startswith('20')}

    def fetch(self):
        data_api_baseurl = 'https://opendata.cbs.nl/ODataApi/odata/70895ned/TypedDataSet'
        crap_fields = "((Geslacht eq '1100')) and ((LeeftijdOp31December eq '10000')) and "
        recent_interval_keys = list(self.intervals.keys())

        for interval_batch in iter_chunks(recent_interval_keys, 100):
            sleep(1)  # Enhance your calm

            recent_intervals_filter_set = [f"(Perioden eq '{interval}')" for interval in interval_batch]
            recent_intervals_filter_str = crap_fields + '(' + " or ".join(recent_intervals_filter_set) + ')'

            data_api_params = [("$select", "Perioden, Overledenen_1"), ("$filter", recent_intervals_filter_str)]

            api_results = self.session.get(data_api_baseurl, params=data_api_params)
            self.raw_data.extend(api_results.json()['value'])

    def process_entry(self, entry):
        """
        Sample entry:
            { "Perioden": "2000X000", "Overledenen_1": 956.0 }
        """
        if "JJ" in entry["Perioden"]:
            return None  # period "2019JJ00" indicates data for that entire year

        first_day, last_day = week_to_first_last_dates(year=entry["Perioden"][0:4], week=entry["Perioden"][6:])
        return self.data_entry(first_day=first_day, last_day=last_day, deaths=int(entry["Overledenen_1"]))
