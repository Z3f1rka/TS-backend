from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class Object(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    file: dict | None = None


class ObjectCreateParameters(BaseModel):
    title: Optional[str]


class ObjectReturn(Object):
    model_config = ConfigDict(from_attributes=True)
    # approved_id: int | None = None
    # status: str
    created_at: datetime
    user_id: int
    id: int
    main_object_id: int


class ObjectUpdateParameters(Object):
    main_object_id: int
    user_id: int


class PrivateObjectReturn(ObjectReturn):
    id: int


class AllObjectReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    file: dict | None = None
    # photo: str | None = None
    id: int
    main_object_id: int
