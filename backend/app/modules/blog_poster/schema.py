from typing import Optional

from pydantic import BaseModel


class BlogPosterRequest(BaseModel):
    query: str
    verbose: Optional[bool] = False
