import json
import numpy as np


class RateConverter (object):

    def __init__(self):
        self.settings = dict()
        self.currencies = []
        self.rates = dict()

    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_currencies(self.settings['common_path'] +
                                 self.settings['currency_list_file'])
            f.close()

    def read_currencies(self, filename):
        curr_list = []
        with open(filename, 'r') as f:
            currencies_json = json.loads(f.read())
            self.rates = currencies_json['rates']
            print("rates :  " + str(self.rates))
            self.currencies = sorted(list(self.rates.keys()))
            f.close()
        return self.currencies

    def get_available_currencies(self):
        return self.currencies

    def refresh_rate_values(self):
        pass

    def convert_to_usd(self, from_currency, value):
        return 100.0

 