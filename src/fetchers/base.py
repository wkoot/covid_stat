import json
import requests
from abc import ABC, abstractmethod
from datetime import datetime


class BaseFetcher(ABC):
    raw_data = []  # type: list
    output_data = {}  # type: dict

    @property
    @abstractmethod
    def country_code(self) -> str:
        pass  # ISO 3166-1 alpha-2

    def __init__(self) -> None:
        self.output_file = '../../data/{}_{:%Y-%m-%d}.json'.format(self.country_code, datetime.today())
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
    def process_entry(self, entry) -> dict:
        pass

    def process(self) -> None:
        for entry in self.raw_data:
            processed_entry = self.process_entry(entry)
            self.output_data.update(processed_entry)

    def store(self) -> None:
        with open(self.output_file, 'w') as json_outfile:
            json.dump(self.output_data, json_outfile)

    def run(self) -> None:
        self.prepare()
        self.fetch()
        self.process()
        self.store()
