from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from age_gender_detection import age_gender_detector
from face_mask_detection import face_mask_detector
import cv2
import os
from PIL import Image

from emotion_detection import emotion_detector

app = Flask(__name__)
CORS(app)
app.debug = True

images = {}


@app.route("/age_gender_detection", methods=["POST", "GET"])
def age_gender_detection():
    if request.method == 'POST':
        f = request.files['image']
        filename = 'upload.jpg'
        path = os.path.join('./static/age-gender/upload', filename)
        f.save(path)
        img = cv2.imread(path)
        output = age_gender_detector(img)
        img = Image.fromarray(output, 'RGB')
        img.save('./static/age-gender/prediction/prediction.png')
        return jsonify(result={"status": 200})
    else:
        tempFileObj = NamedTemporaryFile(mode='w+b', suffix='jpg')
        pilImage = open('./static/age-gender/prediction/prediction.png', 'rb')
        copyfileobj(pilImage, tempFileObj)
        pilImage.close()
        os.remove('./static/age-gender/prediction/prediction.png')
        tempFileObj.seek(0, 0)
        response = send_file(tempFileObj, as_attachment=True, attachment_filename='prediction.png')
        return response


@app.route("/expressions_detection", methods=["GET", "POST"])
def expressions_detection():
    if request.method == 'POST':
        for f in os.listdir('./static/expressions/prediction'):
            os.remove(os.path.join('./static/expressions/prediction', f))
        for f in os.listdir('./static/expressions/upload'):
            os.remove(os.path.join('./static/expressions/upload', f))
        f = request.files['image']
        filename = 'upload.jpg'
        path = os.path.join('./static/expressions/upload', filename)
        f.save(path)
        return jsonify(result={"status": 200})
    if request.method == 'GET':
        global images
        data, images = emotion_detector()
        return data


@app.route("/image", methods=["GET"])
def image():
    return images


@app.route("/face_mask_detection", methods=["POST", "GET"])
def face_mask_detection():
    if request.method == 'POST':
        f = request.files['image']
        filename = 'upload.jpg'
        path = os.path.join('./static/mask/upload', filename)
        f.save(path)
        img = cv2.imread(path)
        face_mask_detector(img)
        return jsonify(result={"status": 200})
    else:
        tempFileObj = NamedTemporaryFile(mode='w+b', suffix='jpg')
        pilImage = open('./static/mask/prediction/prediction.png', 'rb')
        copyfileobj(pilImage, tempFileObj)
        pilImage.close()
        os.remove('./static/mask/prediction/prediction.png')
        tempFileObj.seek(0, 0)
        response = send_file(tempFileObj, as_attachment=True, attachment_filename='prediction.png')
        return response


if __name__ == '__main__':
    app.run()
