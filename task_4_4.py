import sqlalchemy


def selecting_2():
    res_singers_in_genre = connection.execute(f"""
        SELECT genre.title, COUNT(singer.id) FROM singer 
        JOIN singer_genre ON singer.id = singer_genre.singer_id
        JOIN genre ON singer_genre.genre_id = genre.id
        GROUP BY genre.title;
    """).fetchall()
    print("Исполнителей в каждом жанре:")
    for item in res_singers_in_genre:
        print(f"'{item[0]}' - {item[1]}")
    print('*' * 50)

    res_tracks_in_albums = connection.execute(f"""
        SELECT album.title, COUNT(track.id) FROM album
        JOIN track ON album.id = track.album_id
        WHERE year_release BETWEEN 2019 AND 2020
        GROUP BY album.title;
    """).fetchall()
    print("Треков в в альбомах 2019-2020 годов:")
    for item in res_tracks_in_albums:
        print(f"Альбом '{item[0]}', треков - {item[1]}")
    print('*' * 50)

    res_avg_tracks_in_albums = connection.execute(f"""
        SELECT album.title, ROUND(AVG(track.duration), 1) FROM album
        JOIN track ON album.id = track.album_id
        GROUP BY album.title;
    """).fetchall()
    for item in res_avg_tracks_in_albums:
        minutes = item[1] // 60
        seconds = item[1] - minutes * 60
        print(f'Альбом "{item[0]}", средняя продолжительность трека {minutes} мин {seconds} сек')
    print('*' * 50)

    res_singers_without_2020 = connection.execute(f"""
        SELECT DISTINCT singer_name FROM singer
        WHERE singer_name NOT IN (
            SELECT singer_name FROM singer
            JOIN singer_album ON singer.id = singer_album.singer_id
            JOIN album ON singer_album.album_id = album.id
            WHERE album.year_release = 2020);
    """).fetchall()
    print("В 2020 году у этих исполнителей не было альбомов:")
    for item in res_singers_without_2020:
        print(item[0])
    print('*' * 50)

    res_collection_with_singer = connection.execute(f"""
        SELECT DISTINCT collection_title FROM list_collections
        JOIN collection ON list_collections.id = collection.collection_id
        JOIN track ON track.id = collection.track_id
        JOIN album ON album.id = track.album_id
        JOIN singer_album ON album.id = singer_album.album_id
        JOIN singer ON singer.id = singer_album.singer_id
        WHERE singer.singer_name = 'Виктор Цой';
    """).fetchall()
    print("Треки исполнителя 'Виктор Цой' есть в сборниках:")
    for item in res_collection_with_singer:
        print(item[0])
    print('*' * 50)

    res_singer_not_one_genre = connection.execute(f"""
        SELECT album.title FROM album
        JOIN singer_album ON album.id = singer_album.album_id
        JOIN singer ON singer.id = singer_album.singer_id
        JOIN singer_genre ON singer.id = singer_genre.singer_id
        JOIN genre ON genre.id = singer_genre.genre_id
        GROUP BY album.title
        HAVING COUNT(genre.title) > 1;
    """).fetchall()
    print("Авторы следующих альбомов играют более, чем в одном жанре:")
    for item in res_singer_not_one_genre:
        print(item[0])
    print('*' * 50)

    res_tracks_not_in_collections = connection.execute(f"""
        SELECT track.title FROM track
        LEFT JOIN collection ON track.id = collection.track_id
        LEFT JOIN list_collections ON list_collections.id = collection.collection_id
        WHERE list_collections.collection_title IS NULL;
    """).fetchall()
    print("Треки, не входящие в сборники:")
    for item in res_tracks_not_in_collections:
        print(item[0])
    print('*' * 50)

    res_min_tracks = connection.execute(f"""
        SELECT singer.singer_name FROM track
        JOIN album ON album.id = track.album_id
        JOIN singer_album ON album.id = singer_album.album_id
        JOIN singer ON singer.id = singer_album.singer_id
        WHERE track.duration IN (SELECT MIN(track.duration) FROM track);
        """).fetchall()
    print("Авторы самых коротких треков:")
    for item in res_min_tracks:
        print(item[0])
    print('*' * 50)

    res_min_tracks_in = connection.execute(f"""
        SELECT album.title FROM track
        JOIN album ON album.id = track.album_id
        GROUP BY album.title
        HAVING COUNT(track.title) = (SELECT MIN(value) FROM
            (SELECT COUNT(track.title) value FROM track
            JOIN album ON album.id = track.album_id
            GROUP BY album.title) AS CNT
        );
    """).fetchall()
    print("Альбомы, содержащие наименьшее количество треков:")
    for item in res_min_tracks_in:
        print(item[0])


if __name__ == "__main__":
    login = ''
    password = ''
    base = ''

    db = f'postgresql://{login}:{password}@localhost:5432/{base}'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    selecting_2()
