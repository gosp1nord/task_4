import sqlalchemy


def create_tables():
    connection.execute("""
        CREATE table if not exists genre (
            id serial primary key,
            title varchar(300)
            );
        CREATE table if not exists singer(
            id serial primary key,
            singer_name varchar(100)
            );
        CREATE table if not exists singer_genre(
            id serial primary key,
            singer_id integer references singer (id) ON DELETE CASCADE,
            genre_id integer references genre (id) ON DELETE CASCADE
            );
        CREATE table if not exists album(
            id serial primary key,
            title varchar(300),
            year_release integer check (year_release > 0)
            );
        CREATE table if not exists singer_album(
            id serial primary key,
            singer_id integer references singer (id) ON DELETE CASCADE,
            album_id integer references album (id) ON DELETE CASCADE
            );
        CREATE table if not exists track(
            id serial primary key,
            title varchar(300),
            duration integer check (duration > 0),
            album_id integer references album (id)
            );
        CREATE table if not exists list_collections(
            id serial primary key,
            collection_title varchar(300),
            release_year integer check (release_year > 0)
            );
        CREATE table if not exists collection(
            id serial primary key,
            collection_id integer references list_collections (id) ON DELETE CASCADE,
            track_id integer references track (id) ON DELETE CASCADE
            );   
    """)


if __name__ == "__main__":
    login = ''
    password = ''
    base = ''

    db = f'postgresql://{login}:{password}@localhost:5432/{base}'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    create_tables()
