import sqlalchemy


def selecting():
    res_albums = connection.execute(f"SELECT title, year_release FROM album WHERE year_release >= 2008;").fetchall()
    print(f"Альбомы после 2008 года:")
    for item in res_albums:
        print(f"Альбом '{item[0]}' выпущен в {item[1]} году")
    print('*' * 50)

    res_long_track = connection.execute(f"SELECT title, duration FROM track ORDER BY duration DESC;").fetchone()
    minutes = res_long_track[1] // 60
    seconds = res_long_track[1] - minutes * 60
    if minutes:
        print(f"Самый длинный трек - '{res_long_track[0]}', длительность {minutes} мин {seconds} сек.")
    else:
        print(f"Самый длинный трек - '{res_long_track[0]}', длительность {seconds} сек.")
    print('*' * 50)

    res_list_tracks = connection.execute(f"SELECT title, duration FROM track WHERE duration >= 210;").fetchall()
    for item in res_list_tracks:
        minutes = item[1] // 60
        seconds = item[1] - minutes * 60
        print(f'Трек "{item[0]}", длительность {minutes} мин {seconds} сек')
    print('*' * 50)

    res_list_collections = connection.execute(f"SELECT collection_title, release_year FROM list_collections WHERE release_year BETWEEN 2018 AND 2020;").fetchall()
    for item in res_list_collections:
        print(f"Сборник '{item[0]}' выпущен в {item[1]} году")
    print('*' * 50)

    res_list_singers = connection.execute(f"SELECT singer_name FROM singer WHERE singer_name NOT LIKE '%% %%';").fetchall()
    print(f"Исполнители с именем в одно слово:")
    for item in res_list_singers:
        print(item[0])
    print('*' * 50)

    res_list_names_tracks = connection.execute(f"SELECT title FROM track WHERE title LIKE '%%мой%%' OR title LIKE '%%my%%';").fetchall()
    for item in res_list_names_tracks:
        print(f"В названии трека '{item[0]}' есть нужный шаблон")

if __name__ == "__main__":
    login = ''
    password = ''
    base = ''

    db = f'postgresql://{login}:{password}@localhost:5432/{base}'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    selecting()
