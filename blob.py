import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, AccountSasPermissions
from tables import *
import random
from PIL import Image


def lossy_compress(image_name,filepath):

    picture = Image.open(filepath) #open the uncompressed image
    new_image_filepath = filepath[:-len(image_name)]+"Compressed_"+image_name

    picture.save(new_image_filepath,optimize=True,quality=8) #the higher the quality, the less compressed the result is
    return new_image_filepath



def upload_image_to_container(container_name,image_name,filepath):
    compressed_image_filepath = lossy_compress(image_name,filepath) #compress the image - images from camera traps are very large!
    connect_str = "#ENTER YOUR CONNECTION STRING HERE"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container = ContainerClient.from_connection_string(connect_str, container_name)
    try:
        container_properties = container.get_container_properties() #check to see if the container for the camera trap exists
    except Exception as e:
        container_client = blob_service_client.create_container(container_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name) #get a reference to the blob container
    with open(compressed_image_filepath, "rb") as data:
        blob_client.upload_blob(data) 
    os.remove(compressed_image_filepath)#remove the image from server
    return blob_client.url #return the url link to access the image

def get_images_from_container(container_name):
    connect_str = "#ENTER YOUR CONNECTION STRING HERE"
    container = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)

    blob_list = container.list_blobs()
    for blob in blob_list:
        blob_instance = BlobClient.from_connection_string(conn_str=connect_str, container_name=container_name, blob_name=blob.name)
        with open(f"./static/images/{blob.name}", "wb") as my_blob:
            blob_data = blob_instance.download_blob()
            blob_data.readinto(my_blob)

def upload_to_other(image_name,filepath):
    #upload to blob
    url = upload_image_to_container("other",image_name,filepath)
    #get the image url
    #generating random points to plot the panda, this will be converted to extracting location metadata once sonam activates it on the camera traps
    latitude = round(random.uniform(84.3,86.6),3)
    longitude = round(random.uniform(27.3,28.2),3)
    new_other = {'PartitionKey': image_name, 'RowKey': image_name, 'imageURL':url, 'lat':latitude,'long':longitude}
    try:
        table_service.insert_entity('others', new_other)
    except:
        table_service.create_table('others')
        table_service.insert_entity('others', new_other)