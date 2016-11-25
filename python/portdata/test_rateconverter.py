from portdata.rateconverter import RateConverter
import os

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_converter():
    conv = RateConverter()
    conv.apply_settings(this_dir_path + "/../test_settings1.json")
    return conv


def test_available_currencies():
    conv = setup_converter()
    currencies = conv.get_available_currencies()
    assert(3 <= len(currencies))
    assert('CNY' in currencies)
    assert('HUF' in currencies)
    assert('NOK' in currencies)


def test_convert_USD():
    # Note: precision is set to 1 in the settnigs file 
    conv = setup_converter()
    assert(1.0 == conv.convert_to_usd("USD", 1.0))
    assert(14.0 == conv.convert_to_usd("USD", 13.99))
    assert(0 == conv.convert_to_usd("USD", 0))


def test_convert_other():
    # Note:  rates from the default settings file:
    # "NOK": 8.578353
    # "CNY": 6.919257
    # "HUF": 292.810601
    conv = setup_converter()
    assert(0.0 == conv.convert_to_usd("HUF", 1))
    assert(1 == conv.convert_to_usd("HUF", 292.8))
    assert(34.2 == conv.convert_to_usd("HUF", 10000.0))
    assert(10 == conv.convert_to_usd("NOK", 85.78))
    assert(116.6 == conv.convert_to_usd("NOK", 1000))
    assert(100 == conv.convert_to_usd("CNY", 691.9))

