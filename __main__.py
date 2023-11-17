from pymongo import MongoClient
from typing import List
import json
import os
from googleapiclient.http import MediaFileUpload
from Google import Create_Service
from datetime import datetime

class BuildAndUploaderBolt:
    def __init__(self, collection_bolt, collection_link, path_to_data_file, path_to_3D_file):
        self.collection_bolt = collection_bolt
        self.collection_link = collection_link
        self.path_to_3D_file = path_to_3D_file
        self.path_to_data_file = path_to_data_file

    def connect_to_Mongodb(self, col):
        CONNECTION_STRING = "mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/"
        client = MongoClient(CONNECTION_STRING)
        Database = client['Dimension']
        Collection = Database[col]
        return Collection

    def get_DataSize(self, Collection):
        cursor = Collection.find()
        count = Collection.count_documents({})
        data = cursor[count-1]
        id = data['_id']
        data.pop('Timestamp')
        print(data)
        json_object = json.dumps(data)
        with open(self.path_to_data_file, "w") as outfile:
            outfile.write(json_object)
        return json_object, id

    def send_to_GGDrive(self, name_file):
        CLIENT_SECRET_FILE = '/Users/nunny/Desktop/Mecha/client-secret.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        file_metadata = {
            'name': name_file,
            'parents': ['1QlFw3dR1iYkuW86B8YEBYduxaJIX4iIQ']
        }
        media_content = MediaFileUpload(self.path_to_3D_file, mimetype='model/glb')
        file = service.files().create(
            body=file_metadata,
            media_body=media_content
        ).execute()
        print(file)
        file_id = file['id']
        file_link = f'https://drive.google.com/file/d/{file_id}/edit'
        print('File Link: {}'.format(file_link))
        return file_link

    def Build_a_Bolt(self):
        os.chdir('..')
        os.chdir('..')
        os.chdir('/Applications/Blender.app/Contents/MacOS/')
        os.system("ls -al")
        command = f'./blender -b -P /Users/nunny/Desktop/Mecha/Addbolt.py'
        os.system(command)

    def sendLink_to_DB(self, id, col, link):
        Collection = self.connect_to_Mongodb(col)
        timestamp = datetime.now()
        dict = { "_id": id, "link": link, "timestamp": timestamp}
        x = Collection.insert_one(dict)

    def run_loop(self):
        Collection = self.connect_to_Mongodb(self.collection_bolt)
        json_object, id = self.get_DataSize(Collection)
        doc_count = Collection.count_documents({})
        while True:
            current_count = Collection.count_documents({})
            if current_count != doc_count:
                with open(self.path_to_data_file, "w") as outfile:
                    outfile.write(json_object)
                if os.path.isfile(self.path_to_3D_file):
                    os.remove(self.path_to_3D_file)
                self.Build_a_Bolt()
                name_file = 'Bolt_ID' + str(id) + '.glb'
                link = self.send_to_GGDrive(name_file)
                self.sendLink_to_DB(id, self.collection_link, link)
                os.remove(self.path_to_3D_file)
            doc_count = current_count


if __name__ == "__main__":
    data = BuildAndUploaderBolt(
        collection_bolt = 'BoltBitHead',
        collection_link = 'GoogleLink', 
        path_to_3D_file = "/Users/nunny/Desktop/Mecha/3DModel/save_bolt.glb",    
        path_to_data_file = "/Users/nunny/Desktop/Mecha/data_size.json")
    data.run_loop()