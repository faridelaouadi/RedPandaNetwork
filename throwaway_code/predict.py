import requests
import json

def isRedPanda(image):
    #inclding the latest iteration which is pretty accurate
    url = "https://redpandaclassifier.cognitiveservices.azure.com/customvision/v3.0/Prediction/22689ca4-d96e-414f-8e9a-b913f7626f15/classify/iterations/Iteration3/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'de5c1effa9b9486b8ea2fd665faf461a'}
    r =requests.post(url,data=open(image,"rb"),headers=headers)

    response = r.json()
    predictions = response['predictions']

    #the predictions always come in the format of "prediction first" so predictions[i] is what the classifier preidcted
    if predictions[0]['tagName'][0] == "-":
        #not panda
        return False
    else:
        return True

    # for i in range(len(predictions)):
    #     print("{} with probability {}".format( predictions[i]['tagName'] , round(predictions[i]['probability'],2)))