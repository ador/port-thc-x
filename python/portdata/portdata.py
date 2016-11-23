import json
import outlierdetect.gen_esd as esd


class PortData (object):

    def __init__(self):
        self.settings = dict()
        self.countrycodes = set([])
        self.last_rates_timestamp = 0  # todo
        self.orig_data = dict()
        self.data_by_country = dict()
        self.labeled_data_by_country = dict()
        # todo: a currency handler

    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_data(self.settings['datafile'])
            f.close()

    def read_data(self, filename):
        with open(filename, 'r') as f:
            self.orig_data = json.loads(f.read())
            for elem in self.orig_data:
                ccode = elem['port'][0:2]
                if ccode in self.countrycodes:
                    self.data_by_country[ccode].append(elem)
                else:
                    self.countrycodes.add(ccode)
                    self.data_by_country[ccode] = [elem]
            f.close()
        return self.countrycodes

    def get_countrycodes(self):
        return sorted(list(self.countrycodes))

    def get_orig_data_for_country(self, countrycode):
        return self.data_by_country[countrycode]

    def get_labeled_data_for_country(self, countrycode):
        cc = countrycode
        if cc not in self.labeled_data_by_country:
            self.label_data(cc)
        return self.labeled_data_by_country[cc]

    def label_data(self, countrycode):
        # reset previous
        self.labeled_data_by_country[countrycode] = []
        # data to be labeled
        datalist = self.get_orig_data_for_country(countrycode)
        # default: OK
        for data in datalist:
            data['label'] = 'OK'
            self.labeled_data_by_country[countrycode].append(data)
        # re-label outliers:
        # todo: convert currencies
        # ...tmp solution: assume USD
        usd_values = [d['value'] for d in datalist]
        outlier_indices = self.compute_outliers(usd_values)
        for i in outlier_indices:
            self.labeled_data_by_country[countrycode][i]['label'] = 'OUTLIER'

    def compute_outliers(self, usd_values):
        # how many outliers are we searching maximum
        max_outlier_percent = self.settings["max_outlier_percent"]
        max_outlier_num = int(len(usd_values) * (max_outlier_percent / 100.0))
        (num_ols, index_list) = esd.generalizedESD(usd_values, max_outlier_num)
        return index_list
