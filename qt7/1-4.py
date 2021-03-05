import sqlite3

db_name = input()

with sqlite3.connect(db_name) as con:

    cur = con.cursor()

    result = cur.execute("""
                    SELECT title FROM films
                        WHERE films.duration >= 60
                            AND films.genre = (
                                SELECT id from genres
                                    WHERE genres.title = 'комедия'
                            )
                     """)

    for elem in result:
        print(elem[0])
