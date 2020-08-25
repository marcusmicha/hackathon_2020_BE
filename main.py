from flask import Flask, request, json
from flask_cors import CORS
import base64

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
    # binary img
    # file = request.files['image']
    # file.save('im-received.png')
    # # Read the image via file.stream
    # # img = Image.open(file.stream)
    # response = app.response_class(response=json.dumps(mockdata), status=200, mimetype='application/json')
    # return response
    #  except TypeError as error:
    # print(error)

    # base64 img
    payload = request.json
    imgstring = payload['image']
    imgstring += "=" * ((4 - len(imgstring) % 4) % 4)
    imgdata = base64.b64decode(imgstring)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames

    with open(filename, 'wb') as f:
        f.write(imgdata)
    response = app.response_class(response=json.dumps(mockdata), status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(debug=True)
