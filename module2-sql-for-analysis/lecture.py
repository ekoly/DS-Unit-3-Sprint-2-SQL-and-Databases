#!/usr/bin/env python3

import os
import psycopg2

host = os.environ["HOST"]
password = os.environ["PASSWORD"]
user = os.environ["USER"]

pg_conn = psycopg2.connect(host=host, user=user, password=password, database=user)
c = pg_conn.cursor()

c.execute("""
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name varchar(40) NOT NULL,
    data JSONB
);
""")

c.execute("""
INSERT INTO test_table (name, data) VALUES
(
    'A row name',
    null
),
(
    'Another row with JSON',
    '{"a": 1, "b": ["dog", "cat", 42]}'
);
""")

c.close()
pg_conn.commit()

import sqlite3

sl_conn = sqlite3.connect("rpg_db.sqlite3")
sl_curs = sl_conn.cursor()

sl_curs.execute("""
    SELECT COUNT(*)
    FROM charactercreator_character
""")
print(sl_curs.fetchone())

sl_curs.execute("""
    SELECT *
    FROM charactercreator_character
""")
res = sl_curs.fetchall()

pg_curs = pg_conn.cursor()

pg_curs.execute("""
CREATE TABLE charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  level INT,
  exp INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
""")
pg_conn.commit()

pg_curs.execute("""
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES """ + ",".join([str(character[1:]) for character in res]) + ";"
)

pg_conn.commit()
