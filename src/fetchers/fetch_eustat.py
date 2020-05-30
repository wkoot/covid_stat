from csv import DictReader

from util import week_to_first_last_dates
from .base import BaseFetcher


class FetcherEUStat(BaseFetcher):
    """
    Source data - https://data.europa.eu/euodp/en/data/dataset/WHum2Ir8F4KYmrrkj1sRQ

    NUTS 1 correctly maps to ISO 3166-1 alpha-2 for current country_codes
    Dataset also contains 'UK', which is ignored because there is a better source
    """
    country_code = 'EU'  # dummy
    country_codes = [
        'AM',  # Armenia
        'AT',  # Austria
        'BE',  # Belgium
        'BG',  # Bulgaria
        'CH',  # Switzerland (Confoederatio Helvetica)
        'CZ',  # Czech Republic (Czechia)
        'DK',  # Denmark
        'EE',  # Estonia
        'ES',  # Spain
        'FI',  # Finland
        'FR',  # France
        'GE',  # Georgia
        'HU',  # Hungary
        'IS',  # Iceland
        'IT',  # Italy
        'LI',  # Liechtenstein
        'LT',  # Lithuania
        'LU',  # Luxembourg
        'LV',  # Latvia
        'ME',  # Montenegro
        'NO',  # Norway
        'PT',  # Portugal
        'RS',  # Serbia
        'SE',  # Sweden
        'SI',  # Slovenia
        'SK',  # Slovakia
    ]

    def fetch(self):
        tsv_url = 'http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/demo_r_mweek3.tsv.gz&unzip=true'
        tsv_file_contents = self.session.get(tsv_url).content.decode('utf-8')
        tsv_reader = DictReader(tsv_file_contents.splitlines(), delimiter='\t')

        for row in tsv_reader:
            row_title = row.pop('unit,sex,age,geo\\time')  # pop crappy field from entry
            if not row_title.startswith("NR,F,TOTAL,"):
                continue

            last_title_element = row_title.split(',')[-1]
            if last_title_element not in self.country_codes:
                continue

            for key, value in row.items():
                self.raw_data.append(dict(country=last_title_element, period=key, value=value))

    def process_entry(self, entry):
        """
        Sample entry:
            { "Perioden": "2000X000", "Overledenen_1": 956.0 }
        """

        if entry['value'] == ": ":
            return None

        year, week = entry["period"].split("W")
        first_day, last_day = week_to_first_last_dates(year=year, week=week)
        deaths = int(entry['value'].rstrip(' p'))

        return self.data_entry(first_day=first_day, last_day=last_day, deaths=deaths, country_code=entry["country"])
