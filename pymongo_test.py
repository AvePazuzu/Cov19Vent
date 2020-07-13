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
import time
# import subprocess

# Start service
# os.system("mongod --dbpath /home/eugen/develop/python/Cov19Vent/data/db2")
# subprocess.run(["mongod", "--dbpath", "/home/eugen/develop/python/Cov19Vent/data/db2"])

client = pymongo.MongoClient()

db = client.test_db

# client.server_info()

col1 = db.test_collection


# =============================================================================
# Speed test for inserting documents
# =============================================================================
tI0 = time.time()
i=0
for i in range(100):
    i+=110
    # print(i)
    post3 = {
        #"_id": 10001,
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow(),
        "v": [],
        "n": i}

    col1.insert_one(post3).inserted_id
tI1 = time.time()
dtI = tI1-tI0
print(dtI)

# =============================================================================
# Speed test for pushing updates into a document array
# =============================================================================

def update(n, new):
    col1.update_one({'n': n}, {'$push': {"v": new}})

tU0 = time.time()
j = 0
for i in range(100):
    j += 1
    
    update(8, j)

update(20, {"a":5, "b":6})


tU1 = time.time()
dtU = tU1-tU0
print(dtU)

col1.find_one({"n": 20})

lis = list(col1.find({}))

db.list_collection_names()

post_id = col1.insert_one(post2).inserted_id

pprint.pprint(col1.find_one())

db.col1.updateOne(post2)



help(client)

# Stop service
os.system("mongod --dbpath /home/eugen/develop/python/Cov19Vent/data/db2 --shutdown")
