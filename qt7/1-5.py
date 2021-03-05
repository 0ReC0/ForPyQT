import sqlite3

name = input()

with sqlite3.connect("music_db.sqlite") as con:
    cur = con.cursor()

    result = cur.execute("""
                SELECT DISTINCT Track.Name FROM Track
                    WHERE AlbumId IN (
                        SELECT AlbumId FROM  Album
                            WHERE ArtistId = (
                                SELECT Artist.ArtistId FROM Artist
                                    WHERE Artist.Name = ?
                                )
                        ) ORDER BY Name ASC 
                     """, (name,))

    for elem in result:
        print(elem[0])
