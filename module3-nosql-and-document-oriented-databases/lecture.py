#!/usr/bin/env python3

"""
How was working with MongoDB different from working with PostgreSQL?

MongoDB involves using code in another language such as Python to execute queries.
PostgreSQL uses SQL to make queries.
I found PostgreSQL to be harder.
"""

import sqlite3
import pymongo


client = pymongo.MongoClient("mongodb://dbuser:1ydDbDXrQASOBZVx@cluster0-shard-00-00-mqpxk.mongodb.net:27017,cluster0-shard-00-01-mqpxk.mongodb.net:27017,cluster0-shard-00-02-mqpxk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

sl_conn = sqlite3.connect("rpg_db.sqlite3")
sl_curs = sl_conn.cursor()

client.rpg.armory_item.drop()
client.rpg.armory_weapon.drop()
client.rpg.charactercreator_character.drop()

sl_curs.execute("""
    SELECT *
    FROM armory_item
""")
res = sl_curs.fetchall()
docs = [
    {
        "item_id": item_id,
        "name": name,
        "value": value,
        "weight": weight
    } for item_id, name, value, weight in res
]
client.rpg.armory_item.insert_many(docs)


sl_curs.execute("""
    SELECT *
    FROM armory_weapon
""")
res = sl_curs.fetchall()
docs = [
    {
        "item_ptr_id": item_ptr_id,
        "power": power
    } for item_ptr_id, power in res
]
client.rpg.armory_weapon.insert_many(docs)


sl_curs.execute("""
    SELECT *
    FROM charactercreator_character
""")
res = sl_curs.fetchall()
docs = [
    {
        "character_id": character_id,
        "name": name,
        "level": level,
        "exp": exp,
        "hp": hp,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "wisdom": wisdom,
    } for character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom in res
]
client.rpg.charactercreator_character.insert_many(docs)

print("number of characters:")
print(client.rpg.charactercreator_character.count_documents())



