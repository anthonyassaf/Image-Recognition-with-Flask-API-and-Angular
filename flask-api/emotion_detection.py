import fer as FER
import matplotlib.pyplot as plt 
import json
from PIL import Image


def Switch(key):
    switcher = {
        "angry": 0,
        "disgust": 1,
        "fear": 2,
        "happy": 3,
        "sad":  4,
        "surprise":  5,
        "neutral":  6,
    }
    return switcher.get(key)


def emotion_detector():
    img = plt.imread(r"static\expressions\upload\upload.jpg")
    detector = FER.FER(mtcnn=True)
    emotions_dict = detector.detect_emotions(img)
    listOfFaceInfo = list()
    listAngry = list()
    listDisgust = list()
    listFear = list()
    listHappy = list()
    listSad = list()
    listSurprise = list()
    listNeutral = list()

    counter = 0
    for item in emotions_dict:
        for k, v in item.items():
            if type(v) == dict:
                for k2, v2 in v.items():
                    emotion = Switch(k2)
                    if emotion == 0:
                        listAngry.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 1:
                        listDisgust.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 2:
                        listFear.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 3:
                        listHappy.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 4:
                        listSad.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 5:
                        listSurprise.append({"name": "Person {}".format(counter), "value": v2})
                    elif emotion == 6:
                        listNeutral.append({"name": "Person {}".format(counter), "value": v2})

            else:
                boxDict = dict()
                croppedImage = img[v[1]:v[1] + v[2], v[0]:v[0] + v[3], :]
                im = Image.fromarray(croppedImage)
                path = r"static\expressions\prediction\prediction{0}.png".format(counter)
                im.save(path)
                boxDict['name'] = "Person {}".format(counter)
                boxDict['value'] = "static/expressions/prediction/prediction{0}.png".format(counter)
                listOfFaceInfo.append(boxDict)
        counter = counter + 1

    listEmotions = [
        {"name": "angry", "series": listAngry},
        {"name": "disgust", "series": listDisgust},
        {"name": "fear", "series": listFear},
        {"name": "happy", "series": listHappy},
        {"name": "sad", "series": listSad},
        {"name": "surprise", "series": listSurprise},
        {"name": "neutral", "series": listNeutral}
    ]

    faces_json = json.dumps(listOfFaceInfo)

    emotions_json = json.dumps(listEmotions)
    return emotions_json, faces_json
