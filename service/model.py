from pydantic import BaseModel


class SizeModel(BaseModel):
    original: str
    compressed: str


class DecompressSizeModel(BaseModel):
    original: str
    compressed: str
    decompressed: str


class TimeModel(BaseModel):
    compressed: str
    decompressed: str


class UrlModel(BaseModel):
    compressed: str
    decompressed: str


class DataModel(BaseModel):
    type: str
    algorithm: str
    url: str
    size: SizeModel
    time: str


class DecompressDataModel(BaseModel):
    type: str
    algorithm: str
    url: UrlModel
    size: DecompressSizeModel
    time: TimeModel


class CompressResponseModel(BaseModel):
    data: DataModel


class DecompressResponseModel(BaseModel):
    data: DecompressDataModel
