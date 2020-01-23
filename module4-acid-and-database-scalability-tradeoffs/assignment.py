#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("titanic.sqlite3")
c = conn.cursor()

print("""
- How many passengers survived, and how many died?
""")
c.execute("""
    SELECT COUNT(*) || ' died.'
    FROM titanic
    WHERE Survived = 0;
""")
print(c.fetchone())
c.execute("""
    SELECT COUNT(*) || ' survived.'
    FROM titanic
    WHERE Survived = 1;
""")
print(c.fetchone())


print("""
- How many passengers were in each class?
""")
c.execute("""
    SELECT COUNT(*) || ' passengers in class ' || Pclass
    FROM titanic
    GROUP BY Pclass
""")
print(c.fetchall())


print("""
- How many passengers survived/died within each class?
""")
c.execute("""
    SELECT COUNT(*) || ' passengers in class ' || Pclass || (CASE WHEN Survived == 1 THEN ' survived.' ELSE ' died.' END)
    FROM titanic
    GROUP BY Pclass, Survived
""")
print(c.fetchall())


print("""
- What was the average age of survivors vs nonsurvivors?
""")
c.execute("""
    SELECT AVG(Age) || (CASE WHEN Survived == 1 THEN ' was the average age of survivors' ELSE ' was the average age of nonsurvivors' END)
    FROM titanic
    GROUP BY Survived;
""")
print(c.fetchall())


print("""
- What was the average age of each passenger class?
""")
c.execute("""
    SELECT 'Average age of: ' || (
        CASE
            WHEN Pclass = 1 THEN 'first class'
            WHEN Pclass = 2 THEN 'second class'
            WHEN Pclass = 3 THEN 'third class'
        END
    ) || ': ' || AVG(Age)
    FROM titanic
    GROUP BY Pclass
""")
print(c.fetchall())

print("""
- What was the average fare by passenger class? By survival?
""")
c.execute("""
    SELECT 'Average fare of: ' || (
        CASE
            WHEN Pclass = 1 THEN 'first class'
            WHEN Pclass = 2 THEN 'second class'
            WHEN Pclass = 3 THEN 'third class'
        END
    ) || ': ' || AVG(Fare)
    FROM titanic
    GROUP BY Pclass
""")
print(c.fetchall())

c.execute("""
    SELECT 'Average fare of: ' || (
        CASE
            WHEN Survived = 1 THEN 'surivors'
            WHEN Survived = 0 THEN 'nonsurvivors'
        END
    ) || ': ' || AVG(Fare)
    FROM titanic
    GROUP BY Survived
""")
print(c.fetchall())

print("""
- How many siblings/spouses aboard on average, by passenger class? By survival?
""")
c.execute("""
    SELECT 'Average number of siblings/spouses of: ' || (
        CASE
            WHEN Pclass = 1 THEN 'first class'
            WHEN Pclass = 2 THEN 'second class'
            WHEN Pclass = 3 THEN 'third class'
        END
    ) || ': ' || AVG("Siblings/Spouses Aboard")
    FROM titanic
    GROUP BY Pclass
""")
print(c.fetchall())

c.execute("""
    SELECT 'Average number of siblings/spouses of: ' || (
        CASE
            WHEN Survived = 1 THEN 'surivors'
            WHEN Survived = 0 THEN 'nonsurvivors'
        END
    ) || ': ' || AVG("Siblings/Spouses Aboard")
    FROM titanic
    GROUP BY Survived
""")
print(c.fetchall())


print("""
- How many parents/children aboard on average, by passenger class? By survival?
""")
c.execute("""
    SELECT 'Average number of parents/children of ' || (
        CASE
            WHEN Pclass = 1 THEN 'first class'
            WHEN Pclass = 2 THEN 'second class'
            WHEN Pclass = 3 THEN 'third class'
        END
    ) || ': ' || AVG("Parents/Children Aboard")
    FROM titanic
    GROUP BY Pclass
""")
print(c.fetchall())

c.execute("""
    SELECT 'Average number of parents/children of: ' || (
        CASE
            WHEN Survived = 1 THEN 'surivors'
            WHEN Survived = 0 THEN 'nonsurvivors'
        END
    ) || ': ' || AVG("Parents/Children Aboard")
    FROM titanic
    GROUP BY Survived
""")
print(c.fetchall())

print("""
- Do any passengers have the same name?
""")
c.execute("""
    SELECT *
    FROM (
        SELECT COUNT(*) as name_count, Name
        FROM titanic
        GROUP BY Name
    ) WHERE name_count > 1;
""")
print(c.fetchall())

print("""
- (Bonus! Hard, may require pulling and processing with Python) How many married
  couples were aboard the Titanic? Assume that two people (one `Mr.` and one
  `Mrs.`) with the same last name and with at least 1 sibling/spouse aboard are
  a married couple.
""")
