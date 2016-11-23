import json
import outlierdetect.gen_esd as esd
import numpy as np


class PortData (object):

    def __init__(self):
        self.settings = dict()
        self.countrycodes = set([])
        self.last_rates_timestamp = 0  # todo
        self.orig_data = dict()
        # the following dictionaries' key is countrycode
        # and the value is a sorted list (by usd_value) of data items
        self.data_by_country = dict()
        self.labeled_data = dict()
        # computed histogram data with outliers separated
        self.histograms = dict()
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
        if cc not in self.labeled_data:
            self.labeled_data[cc] = self.label_data(cc)
        return self.labeled_data[cc]

    def label_data(self, countrycode):
        # reset previous
        self.labeled_data[countrycode] = []
        # data to be labeled
        datalist = self.get_orig_data_for_country(countrycode)
        labeled_data = []
        # default: OK
        for data in datalist:
            data['label'] = 'OK'
            data['usd_val'] = self.compute_usd_value(data['currency'],
                                                     data['value'])
            labeled_data.append(data)
        # reorder labeled_data list based on usd_value
        labeled_data = sorted(labeled_data, key=lambda data: data['usd_val'])
        usd_values = [d['usd_val'] for d in labeled_data]
        outlier_indices = self.compute_outliers(usd_values)
        # re-label outliers:
        for i in outlier_indices:
            labeled_data[i]['label'] = 'OUTLIER'
        return labeled_data

    def compute_outliers(self, usd_values):
        # how many outliers are we searching (maximum)
        max_outlier_percent = self.settings["max_outlier_percent"]
        max_outlier_num = int(len(usd_values) * (max_outlier_percent / 100.0))
        (num_ols, index_list) = esd.generalizedESD(usd_values, max_outlier_num)
        return index_list

    def get_labeled_histogram_for_country(self, countrycode, bins):
        cc = countrycode
        if cc not in self.histograms:
            self.histograms[cc] = self.create_labeled_histogram(cc, bins)
        return self.histograms[cc]

    def create_labeled_histogram(self, countrycode, num_bins):
        data = self.get_labeled_data_for_country(countrycode)
        # note: we expect this to be sorted!
        usd_values = [d['usd_val'] for d in data]
        assert(usd_values == sorted(usd_values))
        # outlier_idx_list = self.compute_outliers(usd_values)
        (hist_vals, hist_borders) = np.histogram(usd_values, num_bins)
        # TODO compute the histogram 
        return None

    def compute_usd_value(self, from_currency, value):
        # TODO use a separate currency handler class
        return value
