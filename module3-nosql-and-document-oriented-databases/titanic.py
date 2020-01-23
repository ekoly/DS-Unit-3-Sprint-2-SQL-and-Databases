#!/usr/bin/env python3

import os
import pandas as pd
import pymongo

USER = os.environ["MONGO_USER"]
PASS = os.environ["MONGO_PASS"]

client = pymongo.MongoClient(f"mongodb://{USER}:{PASS}@cluster0-shard-00-00-mqpxk.mongodb.net:27017,cluster0-shard-00-01-mqpxk.mongodb.net:27017,cluster0-shard-00-02-mqpxk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

client.titanic.titanic.drop()

titanic_df = pd.read_csv("titanic.csv")
docs = [
    {
        "titanic_id": titanic_id,
        "Survived": survived,
        "Pclass": pclass,
        "Name": name,
        "Sex": sex,
        "Age": age,
        "siblings_or_spouses_aboard": siblings_or_spouses_aboard,
        "parents_or_children_aboard": parents_or_children_aboard,
        "Fare": fare
    } for titanic_id, survived, pclass, name, sex, age, siblings_or_spouses_aboard, parents_or_children_aboard, fare
    in titanic_df.itertuples()
]

client.titanic.titanic.insert_many(docs)

for row in client.titanic.titanic.find({"Name": "Mr. Owen Harris Braund"}):
    print(row)
