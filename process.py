from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from base64 import b64encode, b64decode
import urllib, json, requests, time

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['GET', 'POST'])
def predict_disease():
    if request.method == 'POST':
        data = request.get_json()
        
        image = data["image"]
        # # image = re.sub('^data:image/.+;base64,', '', image)
        # image = image.encode()
        # print(image[:100])
        # print(type(image))
        prediction_results = processPrediction(image)
        
        return jsonify(prediction_results)

       
def processPrediction(image):

    # Create client for prediction service.
    
    img_data = b64decode(image)

    ts = str(time.time())
    filename = "{ts}_image.jpg"  # timestamps concatenated with filename to make filename unique
    with open(filename, 'wb') as f:
        f.write(img_data)

    # Read the image and assign to payload.
    with open(filename, "rb") as image_file:
        content = image_file.read()
    payload = {"image": {"image_bytes": content}}

    # This is a free trial prediction key assigned by Microsoft Commonvision api
    prediction_key = '05e6fcca621f4a12a58a0eb6a2f3cf4f'

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    ## Request headers.
    header = {
        'Content-Type': 'application/octet-stream',
        'Prediction-Key': prediction_key,
        #'Ocp-Apim-Subscription-Key': subscription_key,
    }

    api_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/47c7fdc5-e718-4edc-ad62-401199b1d65b/image?iterationId=22039ff9-148c-4890-8118-dafc8f1b4576"

    r = requests.post(api_url, headers=header, data=content)
    return r.json()

@app.route('/')
@cross_origin(allow_headers=["Content-Type", "Connection", "x-auth", "x-key"])
def hello():
    return jsonify({
            "message": "Hello world",
        })

if __name__ == '__main__':
    app.run()