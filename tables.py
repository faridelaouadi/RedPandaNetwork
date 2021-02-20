from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import os

account_key=os.getenv("AZURE_TABLE_ACCOUNT_KEY")

table_service = TableService(account_name='redpanda', account_key="vSk4SX5tPC6IKz8u4glCHm86bJrjHjnOVrtf9tlclg+EGPiv/7r2CzyFYhW9qZvCpf68JNwuE70yuomAL1iy0w==")

def add_new_camera(cameraID, latitude, longitude):
    new_camera = {'PartitionKey': cameraID, 'RowKey': cameraID,'lat':latitude,'long':longitude}
    table_service.insert_entity('cameras', new_camera)

def get_all_cameras():
    #returns list of all cameras on the map
    camera_list = [] #(cameraID, lat, long)
    cameras = table_service.query_entities('cameras')
    for camera in cameras:
            print(f"Camera ID : {camera.PartitionKey} has position ({camera.lat},{camera.long})")
            camera_list.append([camera.PartitionKey,camera.lat,camera.long])
    return camera_list

def get_all_sightings():
    #returns list of all panda sightings
    sightings_list = []
    sightings = table_service.query_entities( 'others')
    for sighting in sightings:
        sightings_list.append([sighting.imageURL, sighting.lat, sighting.long])
    return sightings_list