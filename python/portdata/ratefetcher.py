import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler


class RateFetcher (object):

    def __init__(self):
        self.settings = None
        self.scheduler = BackgroundScheduler()
        self.full_url = ""
        self.rates_file_name = ""
        self.rates = None
        self.update_iterval_sec = 86400  # don't lower it

    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            subsettings = self.settings['fetch_rates']
            if 'refresh_seconds' in self.settings:
                self.update_iterval_sec = max(subsettings['refresh_seconds'],
                                              self.update_iterval_sec)
            self.full_url = (subsettings['base_url'] + "?app_id=" +
                             subsettings['app_id'])
        self.rates = self.load_rates()
        if self.settings['test_mode']:
            pass
        else:
            self.start_scheduler()

    def get_rates(self):
        return self.rates

    def load_rates(self):
        if self.settings['test_mode']:  # load from fallback file
            rates_file_name = str(self.settings['common_path'] +
                                  self.settings['fallback_currency_file'])
            rates_file = open(rates_file_name, 'r')
            data = json.loads(rates_file.read())
            return data['rates']
        else:
            rates_file_name = str(self.settings['common_path'] +
                                  self.settings['refreshed_currency_file'])
            self.rates_file_name = rates_file_name
            rates_file = open(rates_file_name, 'w') # to write!
            newrates = self.download_and_save_rates(rates_file)
            return newrates

    def start_scheduler(self):
        self.scheduler.add_job(self.update_rates, 'interval',
                               seconds=self.update_iterval_sec)
        self.scheduler.start()

    def update_rates(self):
        rates_file = open(self.rates_file_name, 'w')
        new_rates = self.download_and_save_rates(rates_file)
        self.rates = new_rates

    def download_and_save_rates(self, outfile):
        r = requests.get(self.full_url)
        if 200 != r.status_code:
            print("There was a problem with downloading the conversion rates")
            outfile.close()
            return None
        else:
            data = r.json()
            json.dump(data, outfile)
            outfile.close()
            return data['rates']

    def __del__(self):
        self.scheduler.shutdown()
