import sqlite3
from typing import TypeAlias


MovieData: TypeAlias = dict[str, int | str | float]

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn

def db_init() -> str | None:
    conn = get_db()
    try:
        conn.execute('''create table if not exists movies (
                            id integer primary key autoincrement,
                            title text not null,
                            year integer not null,
                            genre text not null,
                            rating real check (rating >= 0 and rating <= 10) not null)''')
        conn.commit()
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()

def show_movies() -> list[MovieData]:
    conn = get_db()
    rows = conn.execute('select * from movies').fetchall()
    conn.close()
    list_rows = [dict(r) for r in rows]
    return list_rows

def top_five_movies() -> list[MovieData]:
    conn = get_db()
    rows = conn.execute('select * from movies order by rating desc limit 5').fetchall()
    conn.close()
    list_rows = [dict(r) for r in rows]
    return list_rows

def show_by_genre(genre: str) -> list[MovieData]:
    conn = get_db()
    rows = conn.execute('select * from movies where genre like ?', (f'%{genre}%',)).fetchall()
    conn.close()
    list_rows = [dict(r) for r in rows]
    return list_rows

def show_movie(movie_id: int) -> MovieData | None:
    conn = get_db()
    row = conn.execute('select * from movies where id = ?', (movie_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)

def add_movie(movie_title: str, movie_year: int, movie_genre: str, movie_rating: float) -> int | str:
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('insert into movies (title, year, genre, rating) values (?, ?, ?, ?)', (movie_title, movie_year, movie_genre, movie_rating))
        conn.commit()
        movie_id = cursor.lastrowid
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()
    return movie_id

def remove_movie(movie_id: int) -> str | None:
    conn = get_db()
    try:
        conn.execute('delete from movies where id = ?', (movie_id,))
        conn.commit()
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()