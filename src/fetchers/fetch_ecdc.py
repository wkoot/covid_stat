import json
import requests
from datetime import datetime

from util.countries import get_country_fetchers


def fetch_ecdc() -> None:
    # Source data - https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
    today_dt = datetime.today()
    country_fetchers = get_country_fetchers()

    ecdc_data_url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    data_json = requests.get(ecdc_data_url).json()

    output_data = {}
    for entry in data_json['records']:
        country_code = entry['geoId'].upper()

        if country_code not in country_fetchers:
            continue
        if country_code not in output_data:
            output_data[country_code] = {}

        month = int(entry['month'])
        day = int(entry['day'])

        date_str = f"{entry['year']}-{month:02}-{day:02}"
        output_data[country_code][date_str] = int(entry['deaths'])

    output_file = '../../data/{}_{:%Y-%m-%d}.json'.format('ecdc', today_dt)
    with open(output_file, 'w') as json_outfile:
        json.dump(output_data, json_outfile)


if __name__ == "__main__":
    fetch_ecdc()
