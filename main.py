#Path Operation Structure Users

# Ahora construiremos nuestros path operations. Empezaremos por los usuarios.

# 1.	git checkout -b “path_operation_structure_users
# 2.	La primera path operation es la de /signup.
# Haremos el decorator, que sera una petición tipo .post, porque el cliente enviara la información de registro.
# El path operation decorator va llevar todas las buenas practicas que hemos visto hasta ahora.
# path=”/signup”
# response_model=User #En response model heredaremos de User, pues necesitamos tanto lo que ya tenia User heredado de UserBase, como los atributos que agrega.
# status_code=status. #Sera 201 CREATED. Recordemos que debemos importer status de fastapi.
# summary=”Register a User”
# tags=[“Users”]
# 3.	Ahora haremos la path operation function que se llamara signup
# Por el momento la dejaremos sin parámetros y le pondremos un pass, porque vamos a definir la estructura de las path operation solamente.
# 4.	Copiaremos toda la estructura y la pegaremos para todas las path operations que tendremos de los usuarios y empezaremos a modificarlo según sus funcionalidades.
# Recordemos que en los que no estemos solicitando llenar un Field al cliente, vamos a cambiar el tipo de petición a un .get. En los que toca borrar con el .delete. Y en los que hay que actualizar .put
# En /users, el response model no sera precisamente un User. Pues como muestra todos los usuarios, necesitaremos que el JSON contenga todos los usuarios, necesitaremos algo de la librería typing que es la clase List, que nos permite definir que el tipo de una variable va ser una lista de cosas.
# Por lo tanto el response model, es una lista de usuarios List[User].


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

