from flask import Flask, json
from flask_cors import CORS

mockdata = {"CO2_level": 3.53,
            "city_origin": "Ashkelon",
            "product_type": "orange",
            "category": 1,
            "traceability": []}

app = Flask(__name__)
cors = CORS(app)


# GET the picture
@app.route()
def get_picture():
    response = app.response_class(response=json.dumps(mockdata), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
