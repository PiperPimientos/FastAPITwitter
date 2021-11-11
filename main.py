#Path Operation Structure Tweets

# Ahora haremos nuestros tweet path operations.
# 1.	git checkout -b “path_operation_structure_tweets”
# 2.	Ahora, el path operation de home, es el que nos trae a ver todos los tweets, asi que lo pondremos dentro de nuestros path operations de tweets.
# Le agregaremos todos los parámetros del .get
# Por ejemplo, algo de especial detalle es que como nos va mostrar todos los tweets, lo correcto es que lo incluyamos el modelo del response model en una lista como lo hicimos con el /users
# 3.	Luego tendremos los demás path operations de tweets que ya habíamos hecho en el esquema del grafico de todos los endpoints de nuestra aplicación



#IMPORTS

#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI, status

app = FastAPI()

#MODELS

#User Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    birth_date: Optional[date] = Field(default=None)

#Tweet Model

class Tweets(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=280
    )
    created_at: datetime = Field (default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# PATH OPERATIONS

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}


## Users

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup():
    pass

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a specific user information",
    tags=["Users"]
)
def show_specific_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a specific user information",
    tags=["Users"]
)
def delete_specific_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a specific user information",
    tags=["Users"]
)
def update_specific_user():
    pass

## Tweets

@app.get(
    path="/",
    response_model=List[Tweets],
    status_code=status.HTTP_200_OK,
    summary="Show All Tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter API": "Working"}

@app.post(
    path="/post",
    response_model=Tweets,
    status_code=status.HTTP_201_CREATED,
    summary="Create a Tweet",
    tags=["Tweets"]
)
def create_tweet():
    pass

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Show specific Tweet",
    tags=["Tweets"]
)
def show_specific_tweet():
    pass

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)
def delete_tweet():
    pass

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"]
)
def update_tweet():
    pass