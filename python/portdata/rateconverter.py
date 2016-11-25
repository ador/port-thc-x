import json
import numpy as np


class RateConverter (object):
    """ Converts values from available currencies to USD.
        The returned values will be rounded to N decimal points (default: N=2).
        A configuration settings file can define N, among other parameters.
    """


    def __init__(self):
        self.settings = dict()
        self.currencies = []
        self.rates = dict()
        self.precision = 2

    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_currencies(self.settings['common_path'] +
                                 self.settings['currency_list_file'])
            if "currency_conversion_precision" in self.settings:
                self.precision = self.settings["currency_conversion_precision"]
            f.close()

    def read_currencies(self, filename):
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
        # TODO
        pass

    def convert_to_usd(self, from_currency, value):
        if from_currency == "USD":
            return round(value, self.precision)
        else:
            return round(1.0 * value / self.rates[from_currency], self.precision)

 