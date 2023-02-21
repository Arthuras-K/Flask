from pydantic import BaseModel
from pydantic import ValidationError


# Создаем класс отвечающий за валидацию json-ов
class CreateUser(BaseModel):
    username: str
    email: str
    password: str


class CreateAd(BaseModel):
    title: str
    description: str
    user_id: int


def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as err:
        err.errors()

def validate_create_ad(json_data):
    try:
        user_schema = CreateAd(**json_data)
        return user_schema.dict()
    except ValidationError as err:
        err.errors()


print(validate_create_user({'username': 'r5ti', 'password': '125345'}))