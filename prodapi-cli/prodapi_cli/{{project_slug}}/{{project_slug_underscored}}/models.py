import uuid

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
