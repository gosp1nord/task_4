import sqlalchemy


def insert_genre(title_genre):
    res = connection.execute(f"SELECT id FROM genre WHERE title = '{title_genre}';").fetchone()
    if not res:
        res = connection.execute(f"""
            INSERT INTO genre(title) VALUES ('{title_genre}');
            SELECT id FROM genre WHERE title = '{title_genre}';
        """).fetchone()
    return res[0]

def insert_singer(name):
    res = connection.execute(f"SELECT id FROM singer WHERE singer_name = '{name}';").fetchone()
    if not res:
        res = connection.execute(f"""
            INSERT INTO singer(singer_name) VALUES ('{name}');
            SELECT id FROM singer WHERE singer_name = '{name}';
        """).fetchone()
    return res[0]

def insert_singer_genre(res_singer_id, list_genre_id):
    list_res = connection.execute(f"SELECT genre_id FROM singer_genre WHERE singer_id = '{res_singer_id}';").fetchall()
    list_res = list(map(lambda x: x[0], list_res))
    for item in list_genre_id:
        if not list_res or item not in list_res:
            connection.execute(f"INSERT INTO singer_genre(singer_id, genre_id) VALUES ('{res_singer_id}', '{item}');")

def insert_album(title, year_release='0'):
    res = connection.execute(f"SELECT id FROM album WHERE title = '{title}';").fetchone()
    if year_release == '0' and not res:
        res = (0,)
    elif not res:
        res = connection.execute(f"""
            INSERT INTO album(title, year_release) VALUES ('{title}', '{year_release}');
            SELECT id FROM album WHERE title = '{title}';
        """).fetchone()
    return res[0]

def insert_singer_album(res_singer_id, list_album_id):
    list_res = connection.execute(f"SELECT album_id FROM singer_album WHERE singer_id = '{res_singer_id}';").fetchall()
    list_res = list(map(lambda x: x[0], list_res))
    for item in list_album_id:
        if not list_res or item not in list_res:
            connection.execute(f"INSERT INTO singer_album(singer_id, album_id) VALUES ('{res_singer_id}', '{item}');")

def insert_track(title_track, duration, album_id):
    res = connection.execute(f"SELECT id FROM track WHERE title = '{title_track}';").fetchone()
    if not res:
        res = connection.execute(f"""
            INSERT INTO track(title, duration, album_id) VALUES ('{title_track}', '{duration}', '{album_id}');
            SELECT id FROM track WHERE title = '{title_track}';
        """).fetchone()
    return res[0]

def insert_list_collections(title, release_year):
    res = connection.execute(f"SELECT id FROM list_collections WHERE collection_title = '{title}';").fetchone()
    if not res:
        res = connection.execute(f"""
            INSERT INTO list_collections(collection_title, release_year) VALUES ('{title}', '{release_year}');
            SELECT id FROM list_collections WHERE collection_title = '{title}';
        """).fetchone()
    return res[0]

def insert_collection(id_track, list_collection_id):
    list_res = connection.execute(f"SELECT collection_id FROM collection WHERE track_id = '{id_track}';").fetchall()
    list_res = list(map(lambda x: x[0], list_res))
    for item in list_collection_id:
        if not list_res or item not in list_res:
            connection.execute(f"INSERT INTO collection(collection_id, track_id) VALUES ('{item}', '{id_track}');")



def insert_tables():
    genres = ['????????????', '????????', '????????????', '??????', '??????-??????', '??????????']
    for item in genres:
        insert_genre(item)

    singers = [
        ('?????? ??????????', ('????????????', '????????????'), (('?? - ????????????', 2008), ('?????????????? ????????', 2019))),
        ('??????????', ('??????', '??????-??????', '??????????'), (('???????????????????? ????????', 2009), ('??????????, ???????? ??????????????', 2010), ('?????????? ??????????????????', 2020))),
        ('?????????? ??????????????', ('??????', '????????????'), (('Lieutenant Golitsyn', 2000), ('Dangerous', 1991), ('Thriller', 1982))),
        ('?????? ??????????', ('??????????'), (('Confrontation', 1983), ('Uprising', 1980), ('Survival', 1979))),
        ('???????? ??????', ('??????', '??????-??????'), (('Eternity', 2017), ('EOEO', 2019), ('Speed On', 2020))),
        ('?????????? ????????????', ('????????', '????????????'), (('?????? ?????? ??', 2021), ('???????????????? ????????', 2018), ('?????? ?????????? ????????????????', 2017))),
        ('????????????', ('????????????', '??????-??????'), (('Candy Flip', 2019), ('Sayonara Boy X', 2020), ('?????????????? ????????', 2018))),
        ('MiyaGi & Andy Panda', ('??????', '??????-??????'), (('YAMAKASI', 2019), ('Kosandra', 2021), ('Brooklyn', 2020))),
        ('???????????? ??????', ('??????'), (('???????????? ??????????', 1987), ('???????????? ???? ?????????? ????????????', 1989), ('???????????? ????????????', 1990))),
        ('Bob James', ('????????'), (('One', 1974)))
    ]
    for item in singers:
        res_singer_id = insert_singer(item[0])
        list_genre_id = []
        if isinstance(item[1], str):
            list_genre_id.append(insert_genre(item[1]))
        else:
            for i in item[1]:
                list_genre_id.append(insert_genre(i))
        insert_singer_genre(res_singer_id, list_genre_id)

        list_album_id = []
        for i in item[2]:
            if isinstance(i, tuple):
                list_album_id.append(insert_album(i[0], i[1]))
            else:
                list_album_id.append(insert_album(item[2][0], year_release=item[2][1]))
                break
        insert_singer_album(res_singer_id, list_album_id)


    tracks = [
        ('???? ?????????????? ????????', '236', '?????????????? ????????', (('The BEST', 2015), ('???????????????? ??????????', 2019))),
        ('?? ???????????????? ??????????????', '139', '?????????????? ????????', ()),
        ('??????????????', '288', '?????????? ??????????????????', (('?????????????????? ??????????????', 2011), ('???????? ???? ?????????? ???? ??????????', 2014), ('??????????????', 2020))),
        ('Thriller', '358', 'Thriller', (('Scream', 1989), ('King of Pop', 1999))),
        ('Dangerous', '418', 'Dangerous', (('Scream', 1989), ('King of Pop', 1999))),
        ('Chant Down Babylon', '155', 'Confrontation', (('Climb the Ladder', 1987), ('Greatest Hits at Studio One', 1999))),
        ('Zion Train', '214', 'Uprising', (('Climb the Ladder', 1987), ('127 King Street', 1992), ('Man to Man', 1993))),
        ('?????????? ??????', '194', '?????? ?????? ??', (('?????????????? ????????', 2021), ('????????????????', 2020))),
        ('?????????????? ????????', '169', '?????? ?????? ??', (('????????????????', 2020), ('Mira me beb??', 2019), ('????????????????', 2018))),
        ('??????????????????', '139', '???????????????? ????????', (('????????????????', 2018), ('Mira me beb??', 2019))),
        ('?????? ????????????', '185', '?????? ?????????? ????????????????', (('?? ????????', 2017))),
        ('?????????? ?????? ????????', '307', '???????????? ???? ?????????? ????????????', (('?????????? ?????? ????????', 1989), ('?????????????????? ??????????', 1988), ('??????????????', 2020))),
        ('???????????? ???? ?????????? ????????????', '226', '???????????? ???? ?????????? ????????????', (('????????', 1990))),
        ('???????????? ??????????', '286', '???????????? ??????????', (('???????????? ???? ?????????? ????????????', 1989), ('????????', 1990))),
        ('Angela', '342', 'One', (('Fire Into Music', 1974), ('Veronica Gaat Door', 1976))),
        ('In The Garden', '186', 'One', (('Individuals', 1975), ('Bitter Suite', 1982), ('Second Suite', 1980))),
    ]

    for item in tracks:
        id_album = insert_album(item[2])
        if not id_album:
            print(f'?? ???????????? ???????????????? ???????????????? ?????????????? "{item[2]}", ?? ?????????????? ?????????????? ???????? {item[0]} ???? ????????????.')
            continue
        id_track = insert_track(item[0], item[1], id_album)

        list_collection_id = []
        for i in item[3]:
            if isinstance(i, tuple):
                list_collection_id.append(insert_list_collections(i[0], i[1]))
            else:
                list_collection_id.append(insert_list_collections(item[3][0], item[3][1]))
                break

        insert_collection(id_track, list_collection_id)


if __name__ == "__main__":
    login = ''
    password = ''
    base = ''

    db = f'postgresql://{login}:{password}@localhost:5432/{base}'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    insert_tables()
