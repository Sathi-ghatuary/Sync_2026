from pydantic import BaseModel


class TitleEntry(BaseModel):
    id: str
    text: str
    embedding: list[float] | None = None
