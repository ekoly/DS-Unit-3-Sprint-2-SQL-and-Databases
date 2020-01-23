#!/usr/bin/env python3

import os
import pandas as pd
import pymongo

USER = os.environ["MONGO_USER"]
PASS = os.environ["MONGO_PASS"]

client = pymongo.MongoClient(f"mongodb://{USER}:{PASS}@cluster0-shard-00-00-mqpxk.mongodb.net:27017,cluster0-shard-00-01-mqpxk.mongodb.net:27017,cluster0-shard-00-02-mqpxk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

c = client.titanic.titanic

num_survived = c.count_documents({"Survived": 1})
num_not_survived = c.count_documents({"Survived": 0})
print(f"{num_survived} survivors, {num_not_survived} nonsurvivors")
