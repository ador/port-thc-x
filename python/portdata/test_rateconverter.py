from portdata.rateconverter import RateConverter
import os

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_converter_1():
    conv = RateConverter()
    conv.apply_settings(this_dir_path + "/../test_settings1.json")
    return conv


def test_available_currencies():
    conv = setup_converter_1()
    currencies = conv.get_available_currencies()
    assert(4 == len(currencies))
    assert(['CNY', 'HUF', 'NOK', 'USD'] == currencies)

