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

# Ahora crearemos el Tweet model. 
# 1.	Primer atributo sera el tweet_id, del mismo tipo UUID del user id.
# 2.	Tendremos un content, que sera el contenido del tweet, tipo str, y sera un Field de pydantic también
# Sera obligatorio, 
# tendra un max_length de 280 caracteres
# un min len de 1 carácter
# 3.	Un created_at, que sera la fecha de creación del tweet y esto sera de tipo datetime, ya no solo date, porque datetime sera el modulo que además nos muestre hora, minuto segundo, además este sera un Field que contenga los siguientes parámetros.
# Aclaracion: Tendremos que importar, además de datetime, el modulo datetime, para que tengamos la hora, minuto y segundo en la que se creo el tweet.
# created_at: datetime = Field(default=datetime.now())
# 4.	Ahora ademas, con el mismo molde de created_at, tendremos un atributo Field llamado updated_at, para actualizar el Tweet. Sabemos que esto no se puede en twitter, pero esto es un twitter con estereoides
# Ademas este tipo datetime, sera opcional, pues solo se utilizara para actualizar.
# 5.	Falta un ultimo atributo que sera by: User, que como vemos es de tipo User, es decir hereda de la clase User, para decir quien en el modelo de tweet quien es el usuario de procedencia.
# Sera un Field, obligatorio



#IMPORTS

#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI

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