import aiohttp
import asyncio
import requests
import time
import requests
import json

async def main(filepaths):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for filepath in filepaths:
            task = asyncio.ensure_future(get_inference(session, filepath))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        return results


async def get_inference(session, filepath):
    url = "https://redpandaclassifier.cognitiveservices.azure.com/customvision/v3.0/Prediction/22689ca4-d96e-414f-8e9a-b913f7626f15/classify/iterations/Iteration4/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'de5c1effa9b9486b8ea2fd665faf461a'}
    async with session.post(url,data=open(filepath,"rb"),headers=headers) as r:
        response = await r.json()
        print(response)
        predictions = response['predictions']
        if predictions[0]['tagName'][0] == "-":
            return False
        else:
            return True



'''def isRedPanda(filepath):
    #inclding the latest iteration which is pretty accurate
    url = "https://redpandaclassifier.cognitiveservices.azure.com/customvision/v3.0/Prediction/22689ca4-d96e-414f-8e9a-b913f7626f15/classify/iterations/Iteration3/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'de5c1effa9b9486b8ea2fd665faf461a'}
    r =requests.post(url,data=open(filepath,"rb"),headers=headers)
    response = r.json()
    predictions = response['predictions']
    #the predictions always come in the format of "prediction first" so predictions[i] is what the classifier preidcted
    if predictions[0]['tagName'][0] == "-":
        #not panda
        return False
    else:
        return True
        '''


