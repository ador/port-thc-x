from portdata.portdata import PortData
import os
from flask_cors import CORS
from flask import Flask, Response


app = Flask(__name__)
poda = None
this_dir_path = os.path.dirname(os.path.realpath(__file__))

cors = CORS(app)


def setup_port_data():
    poda = PortData()
    poda.apply_settings(this_dir_path + "/../test_settings1.json")
    return poda


@app.route('/', methods=['GET', 'OPTIONS'])
def hello_world():
    return 'Hello, World!'


@app.route('/histogram/<ccode>', methods=['GET', 'OPTIONS'])
def histogram_for_country(ccode):
    histogram = poda.get_labeled_histogram_for_country(ccode, -1)
    return Response(
        '{ "data": ' + str(histogram).replace("'", '"') + '}',
        mimetype='application/json',
        content_type='application/json',
        headers={
            'Cache-Control': 'no-cache'
        }
    )


@app.route('/countrydatalist', methods=['GET', 'OPTIONS'])
def country_data_list():
    datalist = poda.get_all_countries_summary_data()
    return Response(
        '{ "datalist": ' + str(datalist).replace("'", '"') + '}',
        mimetype='application/json',
        content_type='application/json',
        headers={
            'Cache-Control': 'no-cache'
        }
    )


@app.route('/upload', methods=['POST'])
def upload_data():
    from flask import request
    currency = request.get_json().get('currency')
    value = request.get_json().get('value')
    supplier_id = request.get_json().get('supplier_id')
    port = request.get_json().get('port')
    poda.add_dataitem(currency=currency, supplier_id=supplier_id,
                      value=value, port=port)
    return "Thanks"


if __name__ == '__main__':
    poda = setup_port_data()
    app.run(debug=True, host='0.0.0.0')
