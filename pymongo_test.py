#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:03:40 2020

@author: eugen
"""

import os
import pymongo
import datetime
import pprint
import subprocess

# Start service
# os.system("mongod --dbpath /home/eugen/develop/python/Cov19Vent/data/db2")
# subprocess.run(["mongod", "--dbpath", "/home/eugen/develop/python/Cov19Vent/data/db2"])

client = pymongo.MongoClient()

db = client.test_db

# client.server_info()

col1 = db.test_collection

def appArr():
    pass

i=0
for i in range(10):
    i+=11
    print(i)
    post3 = {
        #"_id": 10001,
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow(),
        "v": [1, 244],
        "n": i}

    col1.insert_one(post3).inserted_id

lis = list(col1.find({}))


db.list_collection_names()

post_id = col1.insert_one(post2).inserted_id

pprint.pprint(col1.find_one())

db.col1.updateOne(post2)



help(client)

# Stop service
os.system("mongod --dbpath /home/eugen/develop/python/Cov19Vent/data/db2 --shutdown")
