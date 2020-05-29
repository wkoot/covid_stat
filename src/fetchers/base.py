import json
import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, date
from typing import List


@dataclass
class DataEntry(json.JSONEncoder):
    country_code: str  # ISO 3166-1 alpha-2
    first_day: date
    last_day: date
    deaths: int


class DataEntryEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DataEntry):
            return o.__dict__

        if isinstance(o, (date, datetime)):
            return o.isoformat()

        return super().default(self, o)


class BaseFetcher(ABC):
    raw_data = []  # type: list
    output_data = []  # type: List[DataEntry]

    @property
    @abstractmethod
    def country_code(self) -> str:
        pass  # ISO 3166-1 alpha-2

    def __init__(self) -> None:
        self.output_file = 'data/{}_{:%Y-%m-%d}.json'.format(self.country_code, datetime.today())
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'curl/7.58.0 (+https://doemee.codefor.nl/)',
        })

    def prepare(self) -> None:
        pass

    @abstractmethod
    def fetch(self) -> None:
        pass

    @abstractmethod
    def process_entry(self, entry) -> DataEntry:
        pass

    def data_entry(self, first_day: date, last_day: date, deaths: int) -> DataEntry:
        return DataEntry(country_code=self.country_code, first_day=first_day, last_day=last_day, deaths=deaths)

    def process(self) -> None:
        for entry in self.raw_data:
            processed_entry = self.process_entry(entry)
            if not processed_entry:
                continue

            self.output_data.append(processed_entry)

    def store(self) -> None:
        with open(self.output_file, 'w') as json_outfile:
            json.dump(self.output_data, json_outfile, cls=DataEntryEncoder)

    def run(self) -> None:
        self.prepare()
        self.fetch()
        self.process()
        self.store()
