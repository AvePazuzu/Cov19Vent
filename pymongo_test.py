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
import yaml
 
# import subprocess

# Start service
# os.system("mongod --dbpath /home/eugen/develop/python/Cov19Vent/data/db2")
# subprocess.run(["mongod", "--dbpath", "/home/eugen/develop/python/Cov19Vent/data/db2"])

with open('./bin/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
sID = config["session"]    

try:
    client = pymongo.MongoClient()
    # Initiate database
    db = client.cov19Vent
    
    # client.server_info()
    
    # initiate collection
    col = db.sID
except:
    print("connection failed.")

lis = list(col.find({}))










t = datetime.datetime.now()
param = {"p1": "wer", "p2": 230004, "p3": "wer23" }

post2 = {"session_id": t,
         "setpoints": param,
         "records": [{"timestamp": datetime.datetime.now(),
                     "step":1,
                     "pressure":1,
                     "kPC": 1}]}
post3 = {"session_id": t,
         "setpoints": param,
         "records": []}

# insert initial post
col.insert_one(post3).inserted_id








# bb = col.find_one({"session_id":t})
# for i in bb:
#     print(i)
# tI0 = time.time()
    
    

def up():
    pu = {"timestamp": datetime.datetime.now(),
          "step": 23,
          "pressure":23}    
    try:
        col.update_one({"session_id":t}, {"$push":{"records": pu}})
    except:
        print("DB operation failed")

up()

print("Next")

# tI1 = time.time()
# dtI = tI1-tI0
# print(dtI)
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
