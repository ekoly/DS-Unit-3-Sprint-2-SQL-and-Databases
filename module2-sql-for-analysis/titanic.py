#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd
import sqlite3
import psycopg2

sl_conn = sqlite3.connect("titanic.sqlite3")
titanic_df = pd.read_csv("titanic.csv")
titanic_df['Name'] = titanic_df['Name'].str.replace(r"[\"\',]", '')
titanic_df.to_sql("titanic", sl_conn)
sl_conn.commit()

sl_curs = sl_conn.cursor()


host = os.environ["HOST"]
password = os.environ["PASSWORD"]
user = os.environ["USER"]

pg_conn = psycopg2.connect(host=host, user=user, password=password, database=user)
pg_curs = pg_conn.cursor()

print("Titanic sqlite3 schema:")
print(sl_curs.execute("PRAGMA table_info(titanic);").fetchall())
"""
[(0, 'index', 'INTEGER', 0, None, 0), (1, 'Survived', 'INTEGER', 0, None, 0), (2, 'Pclass', 'INTEGER', 0, None, 0), (3, 'Name', 'TEXT', 0, None, 0), (4, 'Sex', 'TEXT', 0, None, 0), (5, 'Age', 'REAL', 0, None, 0), (6, 'Siblings/Spouses Aboard', 'INTEGER', 0, None, 0), (7, 'Parents/Children Aboard', 'INTEGER', 0, None, 0), (8, 'Fare', 'REAL', 0, None, 0)]
"""

pg_curs.execute("""
CREATE TABLE titanic (
    titanic_id SERIAL PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name TEXT,
    Sex TEXT,
    Age INT,
    Siblings_or_spouses_aboard INT,
    Parents_or_children_aboard INT,
    Fare INT
);
""")
pg_curs.close()
pg_conn.commit();

res = sl_curs.execute("""
    SELECT *
    FROM titanic;
""").fetchall()
sl_curs.close()

pg_curs = pg_conn.cursor()
pg_curs.execute("""
INSERT INTO titanic
(Survived, Pclass, Name, Sex, Age, Siblings_or_spouses_aboard, Parents_or_children_aboard, Fare)
VALUES """ + ",".join([str(pas[1:]) for pas in res]) + ";"
)
pg_conn.commit()

pg_curs.close()
