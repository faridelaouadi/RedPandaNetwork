import requests
import json
url="https://redpandaclassifier.cognitiveservices.azure.com/customvision/v3.0/Prediction/22689ca4-d96e-414f-8e9a-b913f7626f15/classify/iterations/Iteration2/image"
headers={'content-type':'application/octet-stream','Prediction-Key':'de5c1effa9b9486b8ea2fd665faf461a'}
r =requests.post(url,data=open("pic.jpeg","rb"),headers=headers)

response = r.json()
predictions = response['predictions']

for i in range(len(predictions)):
    print("{} with probability {}".format( predictions[i]['tagName'] , round(predictions[i]['probability'],2)))