import csv
import json
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO
from urllib.request import urlopen, Request

today_dt = datetime.today()
data_url = 'https://www.rivm.nl/coronavirus-kaart-van-nederland'

rivm_request = Request(data_url)
rivm_request.add_header('Referer', 'https://www.rivm.nl/')
rivm_request.add_header('User-Agent', 'curl/7.58.0 (+https://doemee.codefor.nl/)')

with urlopen(rivm_request) as conn:
    rivm_html = BeautifulSoup(conn, 'html.parser')

rivm_csv = rivm_html.find('div', dict(id='csvData'))
csv_buffer = StringIO(rivm_csv.text)

first_line = csv_buffer.readline()  # pop the '\n' so DictReader grabs first line header
if first_line != '\n':
    csv_buffer.seek(0)  # reset buffer if the first line was not actually '\n'

csv_data_reader = csv.DictReader(csv_buffer, delimiter=';')
first_entry = True
json_filename = 'docs/data/{:%Y-%m-%d}.json'.format(today_dt)
with open(json_filename, 'w') as json_outfile:
    json_outfile.write('[')

    for row in csv_data_reader:
        if not first_entry:
            json_outfile.write(',')
        else:
            first_entry = False

        json.dump(row, json_outfile)

    json_outfile.write(']')
