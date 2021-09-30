import sqlite3

db = sqlite3.connect('2048.sqlite')

cursor = db.cursor()
cursor.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)""")

def get_best():
    cursor.execute("""
    SELECT name user, max(score) score FROM RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3
    """)
    return cursor.fetchall()


print(get_best())

#cursor.close()

