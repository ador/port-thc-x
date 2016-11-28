from portdata.portdata import PortData
import os
import pytest

# get the path of this script, to use relative paths from here
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_port_data():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings1.json")
    return poda


def test_get_countrycodes():
    poda = setup_port_data()
    countrycodes = poda.get_countrycodes()
    assert(3 == len(countrycodes))
    assert(['CN', 'HU', 'US'] == countrycodes)


def test_get_labeled_data_for_country_OK():
    # Note: test data is prepared such that 'supplier_id' is 99 for outliers
    poda = setup_port_data()
    poda.label_data("CN")
    labeled = poda.get_labeled_data_for_country("CN")
    assert(9 == len(labeled))
    assert('USD' == labeled[0]['currency'])
    assert(99 != labeled[3]['supplier_id'])
    assert('OK' == labeled[3]['label'])


def test_get_labeled_data_for_country_OUTLIER():
    # Note: test data is prepared such that 'supplier_id' is 99 for outliers
    poda = setup_port_data()
    poda.label_data("CN")
    labeled = poda.get_labeled_data_for_country("CN")
    print("all " + str(labeled))
    should_be_outliers = [d for d in labeled if d['supplier_id'] == 99]
    assert(2 == len(should_be_outliers))
    print("sho " + str(should_be_outliers))
    for ol in should_be_outliers:
        assert('OUTLIER' == ol['label'])


def test_histogram_1():
    poda = setup_port_data()
    num_bins = 3
    histogram = poda.get_labeled_histogram_for_country("CN", num_bins)
    assert(num_bins == len(histogram))

    assert(histogram[0]['label'] == '60.00 - 318.33')
    assert(histogram[0]['normal'] == 0)
    assert(histogram[0]['outlier'] == 2)

    assert(histogram[1]['label'] == '318.33 - 576.67')
    assert(histogram[1]['normal'] == 0)
    assert(histogram[1]['outlier'] == 0)

    assert(histogram[2]['label'] == '576.67 - 835.00')
    assert(histogram[2]['normal'] == 7)
    assert(histogram[2]['outlier'] == 0)


def test_histogram_2():
    poda = setup_port_data()
    num_bins = 5
    histogram = poda.get_labeled_histogram_for_country("CN", num_bins)
    assert(num_bins == len(histogram))

    assert(histogram[0]['label'] == '60.00 - 215.00')
    assert(histogram[0]['normal'] == 0)
    assert(histogram[0]['outlier'] == 2)

    assert(histogram[1]['normal'] == 0)
    assert(histogram[1]['outlier'] == 0)
    assert(histogram[2]['normal'] == 0)
    assert(histogram[2]['outlier'] == 0)
    assert(histogram[3]['normal'] == 0)
    assert(histogram[3]['outlier'] == 0)

    assert(histogram[4]['label'] == '680.00 - 835.00')
    assert(histogram[4]['normal'] == 7)
    assert(histogram[4]['outlier'] == 0)


def test_add_data_1():
    poda = setup_port_data()
    assert(0 == len(poda.get_orig_data_for_country("XX")))
    curr = "HUF"
    supp = 999
    value = 23.4
    port = "XXALA"
    poda.add_dataitem(currency=curr, supplier_id=supp, value=value, port=port)
    assert(1 == len(poda.get_orig_data_for_country("XX")))
    poda.label_data("XX")
    labeled = poda.get_labeled_data_for_country("XX")
    assert(1 == len(labeled))
    # default label is "ok" if there is not enough data
    assert('OK' == labeled[0]['label'])


def test_add_data_2():
    poda = setup_port_data()
    assert(0 == len(poda.get_orig_data_for_country("XX")))
    curr = "HUF"
    supp = 999
    value = 23.4
    port = "XXALA"
    # we add the same data here for 6 times
    for i in range(6):
        poda.add_dataitem(currency=curr, supplier_id=supp,
                          value=value, port=port)
    # then we add an extra value, to be detected as an outlier
    poda.add_dataitem(currency=curr, supplier_id=supp,
                      value=(value*3), port=port)
    poda.label_data("XX")
    # check
    labeled = poda.get_labeled_data_for_country("XX")
    assert(7 == len(labeled))
    # default label is "ok" if there is not enough data
    assert('OK' == labeled[0]['label'])
    # values will be sorted by increasing value,so the last will be the outlier
    assert('OUTLIER' == labeled[6]['label'])


def test_add_data_3():
    poda = setup_port_data()
    assert(9 == len(poda.get_orig_data_for_country("CN")))
    curr = "HUF"
    supp = 999
    value = 23.4
    port = "CNALA"
    # we add one extra small outlier value to the chinese set
    poda.add_dataitem(currency=curr, supplier_id=supp,
                      value=value, port=port)
    # call the outlier detector algo
    poda.label_data("CN")
    # check
    labeled = poda.get_labeled_data_for_country("CN")
    assert(10 == len(labeled))
    # values are sorted by increasing value, so the first will be the outlier
    assert('OUTLIER' == labeled[0]['label'])

