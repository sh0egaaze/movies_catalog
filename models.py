from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated


class MovieCreate(BaseModel):
    title: str
    year: Annotated[int, Field(..., ge=1888, le=datetime.now().year)]
    genre: str
    rating: Annotated[float, Field(..., ge=0, le=10)]

class MovieResponse(BaseModel):
    id: int
    title: str
    year: int
    genre: str
    rating: float