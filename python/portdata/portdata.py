import json
import outlierdetect.gen_esd as esd
from portdata.rateconverter import RateConverter
import numpy as np


class PortData (object):

    def __init__(self):
        self.settings = None
        self.countrycodes = set([])
        self.last_rates_timestamp = 0  # todo
        self.orig_data = dict()
        self.min_datasize_for_OLdetection = 7
        # the following dictionaries' key is countrycode
        # and the value is a sorted list (by usd_value) of data items
        self.data_by_country = dict()
        self.labeled_data = dict()
        # computed histogram data with outliers separated
        self.histograms = dict()
        # to keep country codes which received new data but the outlier
        # labels were not yet recomputed
        self.dirty_ccodes_data = set()
        # a currency converter
        self.rate_converter = RateConverter()

    def apply_settings(self, settingsfile):
        self.rate_converter.apply_settings(settingsfile)
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_data(self.settings['common_path'] +
                           self.settings['datafile'])
            f.close()

    def read_data(self, filename):
        with open(filename, 'r') as f:
            self.orig_data = json.loads(f.read())
            for elem in self.orig_data:
                ccode = elem['port'][0:2]
                self.add_raw_data(ccode, elem)
            f.close()
        return self.countrycodes

    def add_raw_data(self, ccode, json_data):
        self.dirty_ccodes_data.add(ccode)
        if ccode in self.countrycodes:
            self.data_by_country[ccode].append(json_data)
        else:
            self.countrycodes.add(ccode)
            self.data_by_country[ccode] = [json_data]

    def get_countrycodes(self):
        return sorted(list(self.countrycodes))

    def get_orig_data_for_country(self, countrycode):
        if countrycode in self.data_by_country:
            return self.data_by_country[countrycode]
        else:
            return []

    def get_labeled_data_for_country(self, countrycode):
        cc = countrycode
        if cc not in self.labeled_data or cc in self.dirty_ccodes_data:
            self.label_data(cc)
        return self.labeled_data[cc]

    def label_data(self, countrycode):
        # data to be labeled
        datalist = self.get_orig_data_for_country(countrycode)
        labeled_data = []
        # default: OK
        for data in datalist:
            data['label'] = 'OK'
            data['usd_val'] = self.compute_usd_value(data['currency'],
                                                     data['value'])
            labeled_data.append(data)
        # only try to find outliers if we have a handful of datapoints at least
        if len(datalist) >= self.min_datasize_for_OLdetection:
            # reorder labeled_data list based on usd_value
            labeled_data_sorted = sorted(
                labeled_data, key=lambda data: data['usd_val'])
            usd_values = [data['usd_val'] for data in labeled_data_sorted]
            outlier_indices = self.compute_outliers(usd_values)
            # re-label outliers:
            for i in outlier_indices:
                labeled_data_sorted[i]['label'] = 'OUTLIER'
            self.labeled_data[countrycode] = labeled_data_sorted
        else:
            self.labeled_data[countrycode] = labeled_data
        self.dirty_ccodes_data.discard(countrycode)

    def compute_outliers(self, usd_values):
        # how many outliers are we searching (maximum)
        max_outlier_percent = self.settings["max_outlier_percent"]
        max_outlier_num = int(len(usd_values) * (max_outlier_percent / 100.0))
        (num_ols, index_list) = esd.generalizedESD(usd_values, max_outlier_num)
        return index_list

    def compute_histogram_for_country(self, countrycode, num_bins=-1):
        cc = countrycode
        if cc not in self.labeled_data or cc in self.dirty_ccodes_data:
            self.label_data(cc)
        if -1 == num_bins:
            datalen = len(self.data_by_country[countrycode])
            num_bins = min(
                max(datalen // 5, self.settings['min_histogram_bins']),
                self.settings['max_histogram_bins'])
        self.histograms[cc] = self.create_labeled_histogram(cc, num_bins)

    def get_labeled_histogram_for_country(self, countrycode, num_bins=-1):
        # TODO : optimize, cache somehow
        self.compute_histogram_for_country(countrycode, num_bins)
        return self.histograms[countrycode]

    def num_outliers_in_hist_col(self, minval, maxval, data):
        return len([x for x in data if (x['usd_val'] >= minval and
                                        x['usd_val'] < maxval and
                                        x['label'] == 'OUTLIER')])

    def num_outliers_in_last_hist_col(self, minval, maxval, data):
        return len([x for x in data if (x['usd_val'] >= minval and
                                        x['usd_val'] <= maxval and
                                        x['label'] == 'OUTLIER')])

    def num_normals_in_hist_col(self, minval, maxval, data):
        return len([x for x in data if (x['usd_val'] >= minval and
                                        x['usd_val'] < maxval and
                                        x['label'] == 'OK')])

    def num_normals_in_last_hist_col(self, minval, maxval, data):
        return len([x for x in data if (x['usd_val'] >= minval and
                                        x['usd_val'] <= maxval and
                                        x['label'] == 'OK')])

    def histo_column(self, minval, maxval, data):
        d = dict()
        d['label'] = '{:.2f}'.format(
            minval) + " - " + '{:.2f}'.format(maxval)
        d['outlier'] = self.num_outliers_in_hist_col(minval, maxval, data)
        d['normal'] = self.num_normals_in_hist_col(minval, maxval, data)
        return d

    def last_histo_column(self, minval, maxval, data):
        d = dict()
        d['label'] = '{:.2f}'.format(
            minval) + " - " + '{:.2f}'.format(maxval)
        d['outlier'] = self.num_outliers_in_last_hist_col(minval, maxval, data)
        d['normal'] = self.num_normals_in_last_hist_col(minval, maxval, data)
        return d

    def create_labeled_histogram(self, countrycode, num_bins):
        data = self.labeled_data[countrycode]
        # note: we expect this to be sorted!
        usd_values = sorted([d['usd_val'] for d in data])
        # outlier_idx_list = self.compute_outliers(usd_values)
        (hist_vals, hist_borders) = np.histogram(usd_values, num_bins)
        to_return = []
        for i in range(len(hist_borders) - 2):
            d = self.histo_column(hist_borders[i],
                                  hist_borders[i + 1],
                                  data)
            to_return.append(d)
        d = self.last_histo_column(hist_borders[-2],
                                   hist_borders[-1],
                                   data)
        to_return.append(d)
        return to_return

    def compute_usd_value(self, from_currency, value):
        usd_val = self.rate_converter.convert_to_usd(from_currency, value)
        return usd_val

    def add_dataitem(self, currency, supplier_id, value, port):
        ccode = port[0:2]
        data = dict(
            currency=currency, supplier_id=supplier_id,
            value=value, port=port
        )
        self.add_raw_data(ccode, data)

    def aggregate_country_labeled_data(self, countrycode):
        cc = countrycode
        datalist = self.labeled_data[cc]
        to_return = dict()
        to_return['ccode'] = cc
        to_return['outlier_num'] = 0
        to_return['normal_num'] = 0
        for d in datalist:
            if d['label'] == 'OK':
                to_return['normal_num'] += 1
            elif d['label'] == 'OUTLIER':
                to_return['outlier_num'] += 1
        return to_return

    def get_all_countries_summary_data(self):
        to_return = []
        for c in self.get_countrycodes():
            self.label_data(c)
            aggregated_countrydata = self.aggregate_country_labeled_data(c)
            to_return.append(aggregated_countrydata)
        return to_return
