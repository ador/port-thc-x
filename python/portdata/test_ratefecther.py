from portdata.ratefetcher import RateFetcher
import os

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_fetcher():
    fetcher = RateFetcher()
    fetcher.apply_settings(this_dir_path + "/../test_settings1.json")
    return fetcher


def test_fetch():
    # we should not query the real endpoint too often
    # because there is a monthly limit at openexchangerates
    # of how many times we can download data
    # pass
    fetcher = setup_fetcher()
    rates = fetcher.get_rates()
    assert(rates["USD"] == 1)
    assert(rates["NOK"] == 8.578353)
