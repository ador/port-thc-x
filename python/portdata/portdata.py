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
        if countrycode in self.labeled_data_by_country:
            return self.labeled_data_by_country[countrycode]
        else:
            self.label_data(countrycode)
            return self.labeled_data_by_country[countrycode]

    def label_data(self, countrycode):
        print(self.settings["max_outlier_percent"])
        datalist = self.data_by_country[countrycode]
        # reset
        self.labeled_data_by_country[countrycode] = []
        # TODO : call outlier detector code here and use labels accordingly
        for d in datalist:
            d['label'] = 'OK'
            self.labeled_data_by_country[countrycode].append(d)

