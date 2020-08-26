from flask import Flask, request, json
from flask_cors import CORS
import base64
from tensorflow import keras
from PIL import Image
import numpy as np

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

UNIT = 'CO2 EQ emitted per kg/Liter of'
dict_food = {'beans': 1.77,
             'cake': 7.48,
             'candy': 2.67,
             'cereal': 3.11,
             'chips': 0.8,
             'chocolate': 7.82,
             'coffee': 16.48,
             'corn': 0.99,
             'flour': 1.44,
             'honey': 0.97,
             'jam': 2.16,
             'juice': 1.52,
             'milk': 2.78,
             'nuts': 0.28,
             'oil': 5.94,
             'pasta': 1.44,
             'rice': 3.84,
             'soda': 1.98,
             'spices': 12.12,
             'sugar': 2.67,
             'tea': 0.0,
             'tomato sauce': 1.43,
             'fish': 5.18,
             'vinegar': 5.75,
             'water': 0.0}
loaded_model = keras.models.load_model('hackathon_2020_BE/my_model')


app = Flask(__name__)
cors = CORS(app)


# GET the picture
@app.route("/productpicture", methods=["POST"])
def get_picture():
    payload = request.json
    imgstring = payload['image']
    imgstring += "=" * ((4 - len(imgstring) % 4) % 4)
    imgdata = base64.b64decode(imgstring)
    filename = 'product_image.jpeg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    cur_im = Image.open("hackathon_2020_BE/product_image.jpeg")
    my_img = []
    cur_im_arr = image.img_to_array(cur_im)
    my_img.append(cur_im_arr)
    my_img = np.array(my_img)
    my_img_preproc = preprocess_input(my_img)

    res_ = loaded_model.predict(my_img_preproc)
    res = np.round_(res_[0][0])
    product_type = 'Beans' if res == 0 else 'Juice'
    score = dict_food[product_type.lower()]
    if score < 3:
        category = 1
    if 3 <= score < 5:
        category = 2
    if score > 5:
        category = 3

    res = {
        "CO2_level": score,
        "city_origin": "Ashkelon",
        "product_type": product_type,
        "category": category,
        "traceability": []}
    print('Image model score = ', res_, '\n')
    print("final res", res, '\n')

    response = app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run()
