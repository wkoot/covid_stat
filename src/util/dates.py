from datetime import datetime, date
from typing import Union


def week_to_first_last_dates(year: Union[str, int], week: Union[str, int]):
    year = int(year)  # retain int for comparison
    week = int(week)  # strip leading zeroes and spaces
    year_week = f"{year}-W{week}"  # ISO 8601 Week date

    first_day = datetime.strptime(year_week + "-1", "%G-W%V-%u").date()
    last_day = datetime.strptime(year_week + "-7", "%G-W%V-%u").date()

    if first_day.year < year:
        first_day = date(year=year, month=1, day=1)
    if last_day.year > first_day.year:
        last_day = date(year=year, month=12, day=31)

    return first_day, last_day
