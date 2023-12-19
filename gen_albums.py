import csv
import sqlite3

conn = sqlite3.connect("songs.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY AUTOINCREMENT, artist TEXT, album TEXT, release_date TEXT, image TEXT, genres TEXT, label TEXT, copyrights TEXT, price REAL)")
cursor.connection.commit()

# CREATE INDEX artist_idx ON songs(artist);
# CREATE INDEX album_idx ON songs(album);

data = {}

with open("input.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        artist = row["Album Artist Name(s)"]
        album = row["Album Name"]
        release_date = row["Album Release Date"]
        image = row["Album Image URL"]
        genres = row["Artist Genres"]
        label = row["Label"]
        copyrights = row["Copyrights"]
        data[artist+album] = {
            "artist": artist,
            "album": album,
            "release_date": release_date,
            "image": image,
            "genres": genres,
            "label": label,
            "copyrights": copyrights}

for d in data:
    artist = data[d]["artist"]
    album = data[d]["album"]
    release_date = data[d]["release_date"]
    image = data[d]["image"]
    genres = data[d]["genres"]
    label = data[d]["label"]
    copyrights = data[d]["copyrights"]

    cursor.execute("INSERT INTO songs (artist, album, release_date, image, genres, label, copyrights) VALUES (?, ?, ?, ?, ?, ?, ?)",(artist, album, release_date, image, genres, label, copyrights))
    cursor.connection.commit()

cursor.close()
conn.close()