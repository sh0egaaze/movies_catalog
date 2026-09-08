import database, models

from fastapi import FastAPI, HTTPException
from typing import TypeAlias


Response: TypeAlias = dict[str, str | int]

app = FastAPI()

@app.on_event("startup")
def root() -> None:
    db_init_err = database.db_init()
    if db_init_err is not None:
        raise RuntimeError(f"Database init error: {db_init_err}")

@app.get("/movies", response_model=list[models.MovieResponse])
def get_movies() -> list[database.MovieData]:
    find_movies = database.show_movies()
    if find_movies:
        return find_movies
    raise HTTPException(status_code=404, detail="Movies not found")

@app.get("/movies/top", response_model=list[models.MovieResponse])
def get_top_movies() -> list[database.MovieData]:
    find_movies = database.top_five_movies()
    if find_movies:
        return find_movies
    raise HTTPException(status_code=404, detail="Movies not found")

@app.get("/movies/genre/{genre}", response_model=list[models.MovieResponse])
def get_by_genre(genre: str) -> list[database.MovieData]:
    find_movies = database.show_by_genre(genre)
    if find_movies:
        return find_movies
    raise HTTPException(status_code=404, detail="Movies not found")

@app.get("/movies/{movie_id}", response_model=models.MovieResponse)
def get_movie(movie_id: int)-> database.MovieData:
    find_movie = database.show_movie(movie_id)
    if find_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return find_movie

@app.post("/movies", response_model=Response)
def create_movie(movie: models.MovieCreate) -> Response:
    result = database.add_movie(movie.title, movie.year, movie.genre, movie.rating)
    if isinstance(result, str):
        raise HTTPException(status_code=500, detail=f"Database error: {result}")
    return {"movie_id": result}

@app.delete("/movies/{movie_id}", response_model=Response)
def delete_movie(movie_id: int) -> Response:
    delete_err = database.remove_movie(movie_id)
    if delete_err is not None:
        raise HTTPException(status_code=500, detail=f"Database error: {delete_err}")
    return {"message": "Movie deleted successfully"}