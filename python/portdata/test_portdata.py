from portdata.portdata import PortData
import os

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setupPortData():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings.json")
    return poda


def test_get_countrycodes():
    poda = setupPortData()
    countrycodes = poda.get_countrycodes()
    assert(3 == len(countrycodes))
    assert(['CN', 'HU', 'US'] == countrycodes)


def test_get_labeled_data_for_country_OK():
    poda = setupPortData()
    labeled = poda.get_labeled_data_for_country("CN")
    assert(10 == len(labeled))
    assert('CNY' == labeled[0]['currency'])
    assert('OK' == labeled[0]['label'])


# def test_get_labeled_data_for_country_OUTLIER():
    # TODO 
    # test data is prepared such that 'supplier_id' is 99 for outliers
    # assert('OUTLIER' == labeled[x]['label'])


# TODO later
