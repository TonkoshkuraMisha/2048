import sqlite3

db = sqlite3.connect('2048.sqlite')

cursor = db.cursor()
cursor.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)""")

cursor.execute("""
SELECT name user, max(score) score FROM RECORDS
GROUP by name
ORDER by score DESC
LIMIT 3
""")

results = cursor.fetchall()
print(results)

cursor.close()