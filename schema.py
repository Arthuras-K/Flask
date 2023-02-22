import re
from pydantic import BaseModel, ValidationError, validator
from errors import HttpError


PASSWORD_REGEX = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])[A-Za-z\d@$!#%*?&_]{8,60}$"
    )

# Создаем класс отвечающий за валидацию json-ов
class CreateUser(BaseModel):
    username: str
    email: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(PASSWORD_REGEX, value):
            raise ValueError('password is to easy')
        return value


class CreateAd(BaseModel):
    title: str
    description: str
    user_id: int


def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as err:
        raise HttpError(status_code=400, message = err.errors())


def validate_create_ad(json_data):
    try:
        user_schema = CreateAd(**json_data)
        return user_schema.dict()
    except ValidationError as err:
        raise HttpError(status_code=400, message = err.errors())
