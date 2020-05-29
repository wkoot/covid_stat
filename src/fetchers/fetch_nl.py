from datetime import datetime, date
from time import sleep

from util import iter_chunks
from .base import BaseFetcher


class FetcherNL(BaseFetcher):
    """
    Source data - https://data.overheid.nl/dataset/309-overledenen--geslacht-en-leeftijd--per-week
    """
    country_code = 'nl'
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

        year = int(entry["Perioden"][0:4])  # int to compare later
        week_number = int(entry["Perioden"][6:])  # int to strip leading zeros
        year_week = f"{year}-W{week_number}"  # ISO 8601 Week date

        first_day = datetime.strptime(year_week + "-1", "%G-W%V-%u").date()
        last_day = datetime.strptime(year_week + "-7", "%G-W%V-%u").date()

        if first_day.year < year:
            first_day = date(year=year, month=1, day=1)
        if last_day.year > first_day.year:
            last_day = date(year=year, month=12, day=31)

        # TODO - create data model
        return dict(first_day=f"{first_day:%Y-%m-%d}", last_day=f"{last_day:%Y-%m-%d}", deaths=int(entry["Overledenen_1"]))
