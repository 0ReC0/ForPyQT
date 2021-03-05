import sqlite3

with sqlite3.connect("films_db.sqlite") as con:

    cur = con.cursor()

    result = cur.execute(f"""SELECT * FROM films 
                WHERE year = ? and duration > ?
                """, (2010, 90)).fetchall()

    for elem in result:
        print(elem)



