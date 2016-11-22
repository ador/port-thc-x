import json

class PortData (object):


    def __init__(self):
        self.settings = dict()
        self.countrycodes = set([])
        self.last_rates_timestamp = 0 # todo
        self.data = dict()
        self.data_by_country = dict() # todo


    def apply_settings(self, settingsfile):
        with open(settingsfile, 'r') as f:
            self.settings = json.loads(f.read())
            self.read_data(self.settings["datafile"])
            f.close()


    def read_data(self, filename):
        with open(filename, 'r') as f:
            self.data = json.loads(f.read())
            for elem in self.data:
                ccode = elem["port"][0:2]
                if ccode in self.countrycodes:
                    pass
                else:
                    self.countrycodes.add(ccode)

            print("all codes found: " + str(self.countrycodes))
            f.close()
        return self.countrycodes


    def get_countrycodes(self):
        return sorted(list(self.countrycodes))

# todo
    # def get_all_data_for_country(self, countrycode):
    #     print("looking for data file in " + str(self.data["datafile"]))
    #     return self.data[]