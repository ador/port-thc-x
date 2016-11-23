from flask import Flask
from portdata.portdata import PortData
import os
import sys


app = Flask(__name__)
poda = None
this_dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_port_data():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings1.json")
    return poda


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/histogram/<ccode>')
def histogram_for_country(ccode):
    histogram = poda.get_labeled_histogram_for_country("CN", -1)
    return "data = " + str(histogram)


if __name__ == '__main__':
    # get the path of this script, to use relative paths from here
    poda = setup_port_data()
    app.run(debug=True, host='0.0.0.0')
