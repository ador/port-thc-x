from portdata.portdata import PortData
import os

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_port_data_1():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings1.json")
    return poda


def test_get_countrycodes():
    poda = setup_port_data_1()
    countrycodes = poda.get_countrycodes()
    assert(3 == len(countrycodes))
    assert(['CN', 'HU', 'US'] == countrycodes)


def test_get_labeled_data_for_country_OK():
    poda = setup_port_data_1()
    labeled = poda.get_labeled_data_for_country("CN")
    assert(7 == len(labeled))
    assert('USD' == labeled[0]['currency'])
    assert('OK' == labeled[1]['label'])


def test_get_labeled_data_for_country_OUTLIER():
    # Note: test data is prepared such that 'supplier_id' is 99 for outliers
    poda = setup_port_data_1()
    labeled = poda.get_labeled_data_for_country("CN")
    should_be_outliers = [d for d in labeled if d['supplier_id'] == 99]
    assert(2 == len(should_be_outliers))
    for ol in should_be_outliers:
        assert('OUTLIER' == ol['label'])
