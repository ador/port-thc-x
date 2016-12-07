import json
from portdata.ratefetcher import RateFetcher


class RateConverter (object):
    """ Converts values from available currencies to USD.
        The returned values will be rounded to N decimal points (default: N=2).
        A configuration settings file can define N, among other parameters.
    """

    def __init__(self):
        self.settings = None
        self.currencies = []
        self.rates = dict()
        self.precision = 2
        self.fetcher = RateFetcher()

    def apply_settings(self, settingsfile):
        self.fetcher.apply_settings(settingsfile)
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_currencies(self.settings['common_path'] +
                                 self.settings['fallback_currency_file'])
            if "currency_conversion_precision" in self.settings:
                self.precision = self.settings["currency_conversion_precision"]
            f.close()

    def read_currencies(self, filename):
        with open(filename, 'r') as f:
            currencies_json = json.loads(f.read())
            self.rates = currencies_json['rates']
            self.currencies = sorted(list(self.rates.keys()))
            f.close()
        return self.currencies

    def get_available_currencies(self):
        return self.currencies

    def refresh_rate_values(self):
        self.rates = self.fetcher.get_rates()

    def convert_to_usd(self, from_currency, value):
        self.refresh_rate_values()
        if from_currency == "USD":
            return round(value, self.precision)
        else:
            if from_currency in self.rates:
                return round(1.0 * value / self.rates[from_currency],
                             self.precision)
            else:
                # TODO : better error handling
                print("Could not convert from unknown currency: " +
                      from_currency)
                return round(value, self.precision)
