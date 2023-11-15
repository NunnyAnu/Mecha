from pymongo import MongoClient
from typing import List
import json
import os
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

class BuildAndUploaderBolt:
    def __init__(self, path_to_data_file, path_to_3D_file):
        self.path_to_3D_file = path_to_3D_file
        self.path_to_data_file = path_to_data_file

    def connect_to_Mongodb(self):
        CONNECTION_STRING = "mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/"
        client = MongoClient(CONNECTION_STRING)
        Database = client['Dimension']
        Collection = Database['BoltBitHead']
        return Collection

    def get_DataSize(self, Collection):
        cursor = Collection.find()
        count = Collection.count_documents({})
        data = cursor[count-1]
        data.pop('Timestamp')
        print(data)
        json_object = json.dumps(data)
        with open(self.path_to_data_file, "w") as outfile:
            outfile.write(json_object)
        return count, json_object

    def send_to_GGDrive(self):
        CLIENT_SECRET_FILE = '/Users/nunny/Desktop/Mecha/client-secret.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        file_metadata = {
            'name': 'bolt.fbx',
            'parents': ['1QlFw3dR1iYkuW86B8YEBYduxaJIX4iIQ']
        }
        media_content = MediaFileUpload(self.path_to_3D_file, mimetype='model/fbx')
        file = service.files().create(
            body=file_metadata,
            media_body=media_content
        ).execute()
        print(file)

    def Build_a_Bolt(self):
        os.chdir('..')
        os.chdir('..')
        os.chdir('/Applications/Blender.app/Contents/MacOS/')
        os.system("ls -al")
        command = f'./blender -b -P /Users/nunny/Desktop/Mecha/Addbolt.py'
        os.system(command)

    def run_loop(self):
        Collection = self.connect_to_Mongodb()
        count, json_object = self.get_DataSize(Collection)
        while Collection.count_documents({}) != count:
            with open(self.path_to_data_file, "w") as outfile:
                outfile.write(json_object)
            if os.path.isfile(self.path_to_3D_file):
                os.remove(self.path_to_3D_file)
            self.Build_a_Bolt()
            self.send_to_GGDrive()
            os.remove(self.path_to_3D_file3D_file)


if __name__ == "__main__":
    data = BuildAndUploaderBolt(
        path_to_3D_file = "/Users/nunny/Desktop/Mecha/3DModel/bolt.fbx",    
        path_to_data_file = "/Users/nunny/Desktop/Mecha/data_size.json")
    data.run_loop()