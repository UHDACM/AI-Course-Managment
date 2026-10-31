from datetime import datetime, timezone
from typing import Annotated

from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field

# MongoDB stores ids as ObjectId; convert them to plain strings for the API
PyObjectId = Annotated[str, BeforeValidator(str)]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MongoModel(BaseModel):
    # Reads "_id" from MongoDB documents (or "id"), but always sends "id" back
    id: PyObjectId = Field(validation_alias=AliasChoices("_id", "id"))

    model_config = ConfigDict(populate_by_name=True)
