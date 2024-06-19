from pydantic import BaseModel


class SizeModel(BaseModel):
    original: str
    compressed: str


class DataModel(BaseModel):
    type: str
    algorithm: str
    url: str
    size: SizeModel
    time: str


class CompressResponseModel(BaseModel):
    data: DataModel
