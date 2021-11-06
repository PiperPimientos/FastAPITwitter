#Models branch

# Ahora recordemos que los modelos se definen por encima de los path operations y por debajo de las importaciones de clases.
# Crearemos
# class User()
# class Tweet()

# Pero recordemos que tendremos que importar BaseModel de pydantic. Recordemos siempre ordenar nuestros imports separando las categorías.

# Comencemos a estructurar el Modelo del User, usuario.
# Antes de comenzar con los atributos recordemos que necesitaremos validar campos (Fields) de pydantic, por lo que tambien importaremos la clase Field
# 1.	Un usuario debe tener un identificador único que los distinga de los demás.
# Crearemos el atributo user_id: UUID.
# Vemos que es de tipo UUID, esto es algo nuevo. Significa “Universal Unic Identifier” Es una clase especial de Python que nos permite colocarle un identificador especial a cada entidad
# Por lo tanto de la librería uuid importaremos UUID
# Ejemplo de como luce un UUID “1123243-ADSA123-asd3124”
# Ademas de que será un Field y este field tendra los parámetros de ser obligatorio
# 2.	Un usuario tiene que tener un email. Este atributo será de tipo EmailStr, recordemos que tenemos que instalar el validador de Email de pydantic con pip install pydantic[email]
# Tambien será un field obligatorio
# 3.	Ademas necesitaremos que coloque su first_name que será de tipo str y será Field obligatorio.
# Este Field será obligatorio, max Len de 50 y min de 1
# Copiaremos y pegaremos pero para last name
# 4.	Ahora haremos un birth_date, que pertenece a un tipo especial en Python que no hemos trabajado. El tipo date
# Recordemos que el tipo date se importa de datetime y que su funcion es presentar una fecha
# Este tipo será un Optional.
# Recordemos que el optional se importa desde la librería Typing
# Este, además, será un Field y tendra como default None.
# 5.	Ademas pues tenemos que tener en cuenta que al registrarse un usuario necesitara un password, que será mínimo de 8 caracteres y sera obligatorio.
# Pero recordemos que nunca es bueno reponder al cliente de la API con la contraseña, por lo tanto hay que crear un modelo separado de usuario.
# Aquí vamos a dejar elaboradas otras dos clases adicionales para User, la clase UserBase, que va tener información básica del usuario.
# Luego vamos a crear UserLogin que servirá para retornar cuando nuestro usuario ya se haya logeado a la aplicación. 
# Para Userbase necesitaremos los atributos de user_id y el email.
# Recordemos que UserBase heredara de BaseModel, pero cuando le coloquemos los atributos a este modelo, entones los demás tendrán que heredar de UserBase.
# UserLogin va contener solo el atributo de la contraseña porque es algo que utilizaremos solo cuando nos estemos logeando.
# Y para agregar las demás características del usuario, utilizaremos User.
# Ya con esto creamos los modelo de usuario de User.


#IMPORTS

#Python
from uuid import UUID
from datetime import date
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI

app = FastAPI()

#MODELS

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
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
class Tweets(BaseModel):
    pass

# PATH OPERATIONS

@app.get(path="/")
def home():
    return {"Twitter API": "Working"}