import csv
import json
import os
import sys

output_data = {}
invert_lookup = {}
with open('src_data/Gebieden_in_Nederland_2019.csv', 'r') as gebieden_csv:
    for row in csv.DictReader(gebieden_csv, delimiter=';'):
        if row['Naam'] == 'Bron: CBS':
            continue

        data_code = int(row['Code'].lstrip('GM'))
        data_row = dict(
            naam=row['Naam'],
            code=data_code,
            inwoners=int(row['Inwonertal']),
            adressendichtheid=int(row['Omgevingsadressendichtheid per km2'])
        )
        output_data[data_code] = data_row
        invert_lookup[row['Naam']] = data_code

with open('src_data/Regionale_kerncijfers_Nederland_2019.csv', 'r') as kerncijfers_csv:
    for row in csv.DictReader(kerncijfers_csv, delimiter=';'):
        if row['Naam'] == 'Bron: CBS':
            continue
        if row['Totale bevolking'] == '':
            continue

        data_row = dict(
            naam=row['Naam'],
            inwoners=int(row['Totale bevolking']),
            mannen=int(row['Mannen']),
            vrouwen=int(row['Vrouwen']),
            age_0_5=int(row['Jonger dan 5 jaar']),
            age_5_10=int(row['5 tot 10 jaar']),
            age_10_15=int(row['10 tot 15 jaar']),
            age_15_20=int(row['15 tot 20 jaar']),
            age_20_25=int(row['20 tot 25 jaar']),
            age_25_45=int(row['25 tot 45 jaar']),
            age_45_65=int(row['45 tot 65 jaar']),
            age_65_80=int(row['65 tot 80 jaar']),
            age_80_plus=int(row['80 jaar of ouder']),
            oppervlakte=float(row['Totale oppervlakte km2'].replace(',', '.')),
            land_oppervlak=float(row['Land oppervlakte km2'].replace(',', '.'))
        )

        data_row['bevolkinsdichtheid'] = data_row['inwoners'] / data_row['land_oppervlak']

        data_code = invert_lookup[row['Naam']]
        if output_data[data_code]['inwoners'] != data_row['inwoners']:
            sys.stdout.write('Gemeente {} population mismatch!\n'.format(data_code))

        output_data[data_code].update(data_row)

with open('src_data/gebieden_2019.json', 'w') as json_datafile:
    json.dump(output_data, json_datafile)

gemeente_geojson = 'docs/data/gemeentegrenzen_simplified.geojson'
if not os.path.isfile(gemeente_geojson):
    raise SystemExit

with open(gemeente_geojson, 'r') as geojson_datafile:
    geojson_data = json.load(geojson_datafile)

for feature in geojson_data['features']:
    code = feature['properties']['Code']

    feature['properties'].update(
        inwoners=output_data[code]['inwoners'],
        mannen=output_data[code]['mannen'],
        vrouwen=output_data[code]['vrouwen'],
        age_0_5=output_data[code]['age_0_5'],
        age_5_10=output_data[code]['age_5_10'],
        age_10_15=output_data[code]['age_10_15'],
        age_15_20=output_data[code]['age_15_20'],
        age_20_25=output_data[code]['age_20_25'],
        age_25_45=output_data[code]['age_25_45'],
        age_45_65=output_data[code]['age_45_65'],
        age_65_80=output_data[code]['age_65_80'],
        age_80_plus=output_data[code]['age_80_plus'],
        oppervlakte=output_data[code]['oppervlakte'],
        land_oppervlak=output_data[code]['land_oppervlak'],
        adressendichtheid=output_data[code]['adressendichtheid'],
        bevolkinsdichtheid=output_data[code]['bevolkinsdichtheid']
    )

with open(gemeente_geojson, 'w') as geojson_datafile:
    json.dump(geojson_data, geojson_datafile)
