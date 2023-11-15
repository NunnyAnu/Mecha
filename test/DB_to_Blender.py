from pymongo import MongoClient
from typing import List
import json

CONNECTION_STRING = "mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/"
client = MongoClient(CONNECTION_STRING)
Database = client['Dimension']
Collection = Database['BoltBitHead']

cursor = Collection.find()
count = Collection.count_documents({})
print(count)
data = cursor[count-1]
data.pop('Timestamp')
print(data)

# show recently size
json_object = json.dumps(data)
 
with open("/Users/nunny/Desktop/Mecha/data_size.json", "w") as outfile:
    outfile.write(json_object)