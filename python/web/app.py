from portdata.portdata import PortData
import os
import sys
from flask_cors import CORS, cross_origin
from flask import Flask, Response, jsonify



app = Flask(__name__)
poda = None
this_dir_path = os.path.dirname(os.path.realpath(__file__))

#cors = CORS(app, resources={r"/localhost:5000": {"origins": "*"}})
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


def setup_port_data():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings1.json")
    return poda


@app.route('/', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type'])
def hello_world():
    return 'Hello, World!'


@app.route('/histogram/<ccode>')
@cross_origin(origin='*', headers=['Content-Type'])
def histogram_for_country(ccode):
    histogram = poda.get_labeled_histogram_for_country(ccode, -1)
    return Response(
        '{ "data": ' + str(histogram).replace("'", '"') + '}',
        mimetype='application/json',
        content_type='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


if __name__ == '__main__':
    # get the path of this script, to use relative paths from here
    poda = setup_port_data()
    app.run(debug=True, host='0.0.0.0')
