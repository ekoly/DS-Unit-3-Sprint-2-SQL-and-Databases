#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("rpg_db.sqlite3")
c = conn.cursor()

print("""
-- How many total Characters are there?  """)
c.execute("""
    SELECT COUNT(cc.character_id)
    FROM charactercreator_character cc;
""")
print(c.fetchone())


print("""
-- How many of each specific subclass?
-- cleric """)
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_cleric cc;
""")
print(c.fetchone())

print("-- fighter")
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_fighter;
""")
print(c.fetchone())

print("-- mage")
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_mage;
""")
print(c.fetchone())

print("-- necromancer")
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_necromancer;
""")
print(c.fetchone())

print("-- thief")
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_thief;
""")
print(c.fetchone())

print("""
-- How many total Items?  """)
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_character_inventory;
""")
print(c.fetchone())

print("""
-- How many of the Items are weapons? How many are not?  """)
c.execute("""
SELECT COUNT(*)
FROM charactercreator_character_inventory cci
WHERE cci.item_id IN (
	SELECT aw.item_ptr_id
	FROM armory_weapon aw
);
""")
print(c.fetchone())

print("Not?")
c.execute("""
    SELECT COUNT(*)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id NOT IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    );
""")
print(c.fetchone())

print("""
-- How many Items does each character have? (Return first 20 rows) """)
c.execute("""
    SELECT cci.character_id, COUNT(*)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id NOT IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    ) GROUP BY cci.character_id
    LIMIT 20;
""")
print(c.fetchall())

print("""
-- How many Weapons does each character have? (Return first 20 rows) """)
c.execute("""
    SELECT cci.character_id, COUNT(*)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    ) GROUP BY cci.character_id
    LIMIT 20;
""")
print(c.fetchall())

print("""
-- On average, how many Items does each Character have?  """)
c.execute("""
    SELECT CAST(COUNT(cci.item_id) AS Float)/CAST(COUNT(DISTINCT cci.character_id) AS Float)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id NOT IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    );
""")
print(c.fetchone())

print("""
-- On average, how many Weapons does each character have?""")
c.execute("""
    SELECT CAST(COUNT(cci.item_id) AS Float)/CAST(COUNT(DISTINCT cci.character_id) AS Float)
    FROM charactercreator_character_inventory cci
    WHERE cci.item_id IN (
            SELECT aw.item_ptr_id
            FROM armory_weapon aw
    );
""")
print(c.fetchone())

conn.close()
