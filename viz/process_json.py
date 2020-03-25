import json
import os
import sys
from datetime import datetime, timedelta

today_dt = datetime.today()
json_filename = 'docs/data/{:%Y-%m-%d}.json'.format(today_dt)
with open(json_filename, 'r') as json_datafile:
    data_array = json.load(json_datafile)

if isinstance(data_array, dict):
    raise SystemExit('Already processed, skipping')

# prefill dataset
with open('src_data/gebieden_2019.json', 'r') as gebieden_datafile:
    gebieden_data = json.load(gebieden_datafile)

output_data = {}
for gemeente in gebieden_data.values():
    gemeente_nummer = gemeente['code']
    output_data[gemeente_nummer] = dict(count=0, increase=0, gemeente=gemeente_nummer)

# fill from fetched rivm data
peildatum = ''
for entry in data_array:
    entry_num = int(entry['Gemnr']) if entry['Gemnr'].lstrip('-').isdigit() else -5  # NB: -1, -2 are already taken
    entry_count = int(entry['Aantal']) if entry['Aantal'].isdigit() else 0

    if entry_num not in output_data:
        if entry['Gemeente'].startswith('peildatum'):
            peildatum = entry['Gemeente'].lstrip('peildatum ')

        output_data[entry_num] = dict(count=0, increase=0, gemeente=entry_num)
        if entry_num > 0:
            sys.stdout.write('Gemeente {} was not in output data!\n'.format(entry_num))

    output_data[entry_num].update(count=entry_count)

# TODO - parse peildatum could be done earlier
if peildatum:
    day_num, month_trailer = peildatum.lower().split(maxsplit=1)
    today_num, today_month = '{:%d %b}'.format(today_dt).lower().split()
    if not (day_num == today_num and month_trailer[0] == today_month[0]):  # first month letter is similar in NL locale
        os.remove(json_filename)
        raise SystemExit('Data is not new for today')

# comparison with yesterday
yesterday_json = 'docs/data/{:%Y-%m-%d}.json'.format(today_dt - timedelta(days=1))
if os.path.isfile(yesterday_json):
    with open(yesterday_json, 'r') as json_yesterday_file:
        data_yesterday = json.load(json_yesterday_file)

    for entry in output_data:
        data_key = str(entry)  # json stored k,v has stringy keys
        if data_key not in data_yesterday:
            sys.stdout.write('Gemeente {} was not in yesterday data!\n'.format(entry))
            output_data[entry]['increase'] = 0
            continue

        output_data[entry]['increase'] = output_data[entry]['count'] - data_yesterday[data_key]['count']

with open(json_filename, 'w') as json_datafile:
    json.dump(output_data, json_datafile)

os.remove('docs/data/today.json')
os.symlink(os.path.basename(json_filename), 'docs/data/today.json')
