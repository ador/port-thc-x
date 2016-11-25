import json
import numpy as np


class RateConverter (object):

    def __init__(self):
        self.settings = dict()
        self.currencies = []

    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_currencies(self.settings['currency_list_file'])
            f.close()

    def read_currencies(self, currencies_json):
        pass

    def get_available_currencies(self):
        pass

    def refresh_rate_values(self):
        pass

    def convert_to_usd(self, from_currency, value):
        return 100.0

 