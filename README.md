[![Build Status](https://clt-a88b6d82-2b5e-4b58-bba9-555322fe0d27.visualstudio.com/RedPandaNetwork/_apis/build/status/faridelaouadi.RedPandaNetwork?branchName=master)](https://clt-a88b6d82-2b5e-4b58-bba9-555322fe0d27.visualstudio.com/RedPandaNetwork/_build/latest?definitionId=1&branchName=master)


![](rpn_dashboard.png)

Background
----------
- [Project 15​](http://aka.ms/project15) from Microsoft is on a mission to accelerate innovation in environmental conservation and ecological sustainability. Cloud computing, Internet of Things (IoT) and Artificial Intelligence (AI) bring great opportunity to drive advancements in a myriad of sustainability efforts including preserving biodiversity and protecting critical habitat.

- As part of the UCL IXN, I had the opportunity to work alongside Microsoft to create a web app for the ["Red Panda Network"](https://www.redpandanetwork.org/) to streamline major ineffeciencies in their workflow. 

Current Progress
----------------
![Alt Text](https://media.giphy.com/media/V5pTpVD9gUuxQdMmqL/giphy.gif)

- User Authentication using Azure Active Directory
- Web App Design adhering to Don Norman's design principles and Preece's Interaction design principles
- Azure map with clickable icons for camera traps 
- Web scraper to gather training data for red panda classifier (scrape.py)
- Red panda classifier using [Custom Vision](https://www.customvision.ai/) and script for inference
- Web app hosted on Azure using Azure app service [Click to view](https://redpandanetwork.azurewebsites.net/)
- CI/CD workflow using Github and Azure Pipelines 
- Asynchronous analysis of uploaded images (max of 10 per batch)
- Upload new images using Azure blob storage
- Unit tests using Pytest and Selenium
- Code Refactoring

Backlog 
--------
- Project Handover

Extra
-----

Full Video demonstration : [Click to view](https://youtu.be/RTiv9G_X0rY)


How can I run this project?
-----

###Prerequisites###

- You will need to have an Azure account 
- Basic understanding of Python 3

####Setting up Active Directory####
- To enable signing in using a Microsoft Account, we have to set up the service on your azure portal
- Follow [this](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-v2-python-webapp) tutorial to get going
- In the file “app_config.py”, modify the Client_ID, Client_Secret, Redirect_Path with your unique values for your created service.
- Once this is done, you should now be able to log into the platform using your microsoft account 

####Setting up Azure Map####
- To be able to use the interactive map, we need to create an azure map service in the azure portal 
- Follow [this](https://docs.microsoft.com/en-gb/azure/azure-maps/quick-demo-map-app) tutorial to get going
- In the file static/js/azureMap.js change the subscriptionKey to your unique subscription key
- Once this is done, you should now be able to interact with the map

####Setting up Azure storage####
- Create a storage account by following [this](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal) tutorial
- Locate your storage account.
- In the Settings section of the storage account overview, select Access keys. Here, you can view your account access keys and the complete connection string for each key.
- Find the Connection string value under key1, and select the Copy button to copy the connection string. 
- Replace this connection string with all occurrences of “connect_str” in blob.py
- Replace the “account_key” with this key in tables.py as well as the “account_name” with your account_name. All this information can be found by going to the credentials tab in the account storage.
- Also replace “account_key”,”account_name” and “connect_str” in app.py

###Getting started###
- Download the repo 
- Follow all the prerequisite steps to set up the azure account with all the relevant services
- Create a virtual environment and install dependencies in requirements.txt to get all the dependencies required for the project
- Run the development server using “ flask run “
- Navigate to http://localhost:5000/ to see the project running locally 
- Now to deploy this onto a custom domain we need to host the code somewhere
- Create a github account and upload the code there to host it 
- We will be using azure pipelines to build the app and using app service to host it on a custom domain
- Follow [this](https://docs.microsoft.com/en-gb/azure/devops/pipelines/ecosystems/python-webapp?view=azure-devops) tutorial to build and deploy the web app
- Replace the azure-pipelines.yml with your unique yaml file generated from the tutorial 
- Once all this is done, you should be able to run the live version from the domain that appears in the azure app service dashboard
- Enjoy!

