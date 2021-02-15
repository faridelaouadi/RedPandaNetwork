from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

table_service = TableService(account_name='redpanda', account_key='vSk4SX5tPC6IKz8u4glCHm86bJrjHjnOVrtf9tlclg+EGPiv/7r2CzyFYhW9qZvCpf68JNwuE70yuomAL1iy0w==')

# camera_0010 = {'PartitionKey': '0010', 'RowKey': '0010','lat':85.331,'long':27.72}
# camera_0011 = {'PartitionKey': '0011', 'RowKey': '0011','lat':86.331,'long':27.72}
# camera_0012 = {'PartitionKey': '0012', 'RowKey': '0012','lat':85.331,'long':28.12}
# camera_0013 = {'PartitionKey': '0013', 'RowKey': '0013','lat':84.331,'long':27.72}

def add_new_camera(cameraID, latitude, longitude):
    new_camera = {'PartitionKey': cameraID, 'RowKey': cameraID,'lat':latitude,'long':longitude}
    table_service.insert_entity('cameras', new_camera)

def get_all_cameras():
    camera_list = [] #(cameraID, lat, long)
    cameras = table_service.query_entities( 'cameras')
    for camera in cameras:
            print(f"Camera ID : {camera.PartitionKey} has position ({camera.lat},{camera.long})")
            camera_list.append([camera.PartitionKey,camera.lat,camera.long])
    return camera_list