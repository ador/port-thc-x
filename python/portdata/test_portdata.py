from portdata.portdata import PortData
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_read_sample_data():
    print("dirpath: " + dir_path)
    poda = PortData()
    poda.apply_settings(dir_path + "/../test_settings.json")
    data = poda.get_countrycodes()
    assert(3 == len(data))
    assert(['CN', 'HU', 'US'] == data)


# TODO
# def test_get_histogram():
#     poda.init()
#     histogram_with_outliers = poda.get_data_for_country("CN")
#     assert(10 == len(histogram_with_outliers))
