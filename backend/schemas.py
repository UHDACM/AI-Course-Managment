from pydantic import BaseModel, ConfigDict, Field


class ClassBase(BaseModel):
    classname: str = Field(min_length=1, max_length=100)
    assignment1: str | None = None


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    classname: str | None = Field(default=None, min_length=1, max_length=100)
    assignment1: str | None = None


class ClassResponse(ClassBase):
    model_config = ConfigDict(from_attributes=True)

    class_id: int