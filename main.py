from flask import Flask, request, json
from flask_cors import CORS
from PIL import Image

mockdata = {"CO2_level": 3.53,
            "city_origin": "Ashkelon",
            "product_type": "orange",
            "category": 1,
            "traceability": []}

app = Flask(__name__)
cors = CORS(app)


# GET the picture
@app.route("/productpicture", methods=["POST"])
def get_picture():
    try:
        file = request.files['image']
        file.save('im-received.png')
        # Read the image via file.stream
        # img = Image.open(file.stream)
        response = app.response_class(response=json.dumps(mockdata), status=200, mimetype='application/json')
        return response
    except TypeError as error:
        print(error)


if __name__ == '__main__':
    app.run(debug=True)
