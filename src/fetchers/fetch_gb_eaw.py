import defusedxml
from bs4 import BeautifulSoup
from datetime import timedelta, date
from xlrd import open_workbook, xldate

from .base import BaseFetcher

defusedxml.defuse_stdlib()


class FetcherEAW(BaseFetcher):
    """
    Source data - https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales
    """
    country_code = 'GB-EAW'  # https://en.wikipedia.org/wiki/ISO_3166-2:GB

    def fetch(self):
        listing_url = 'https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales'
        listing_content_stream = self.session.get(listing_url)
        link_line = ''
        for line in listing_content_stream.iter_lines(decode_unicode=True):
            if line.startswith('<a href="/file?uri=%2fpeoplepopulationandcommunity%2fbirthsdeathsandmarriages%2fdeaths%2fdatasets%2fweeklyprovisionalfiguresondeathsregisteredinenglandandwales%2f2020/'):
                link_line = line
                break

        parsed_link = BeautifulSoup(link_line).find('a', href=True)
        if not parsed_link:
            raise SystemExit("Can't find datafile to parse")

        xlsx_content = self.session.get("https://www.ons.gov.uk" + parsed_link.attrs['href'])
        workbook = open_workbook(file_contents=xlsx_content.content)
        data_sheet = workbook.sheet_by_name('Weekly figures 2020')

        first_column = [data_sheet.cell_value(row_index, 0) for row_index in range(data_sheet.nrows)]
        week_number_row = first_column.index('Week number')
        week_end_date_row = first_column.index('Week ended')
        total_deaths_row = first_column.index('Total deaths, all ages')

        for column_index in range(data_sheet.ncols):
            week_number = data_sheet.cell_value(week_number_row, column_index)
            week_end_date = data_sheet.cell_value(week_end_date_row, column_index)
            total_deaths = data_sheet.cell_value(total_deaths_row, column_index)

            self.raw_data.append(dict(week_number=week_number, last_day=week_end_date, total_deaths=total_deaths))

    def process_entry(self, entry):
        """
        Sample entry:
            { "Perioden": "2000X000", "Overledenen_1": 956.0 }
        """
        if not entry['week_number']:
            return None
        if entry['week_number'] == 'Week number':
            return None

        week = int(entry['week_number'])
        last_day = xldate.xldate_as_datetime(entry['last_day'], None)

        first_day = last_day - timedelta(days=6)
        # TODO - datetime -> date && year iterator

        year = 2020
        if first_day.year < year:
            first_day = date(year=year, month=1, day=1)
        if last_day.year > first_day.year:
            last_day = date(year=year, month=12, day=31)

        return self.data_entry(first_day=first_day, last_day=last_day, deaths=int(entry['total_deaths']))
