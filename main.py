#Path Operation Create Tweet


# Crearemos u nuevo branch llamado “tweet_post” porque vamos a trabajar en la path operation para crear un nuevo tweet.
# 1.	Vamos a copiar el contenido de nuestra path operation function de signup y lo vamos a pegar en nuestra funcion de post a tweet
# Modificaremos todo
# Empezando por el docstring y el parámetro de la funcion que sera tweet de tipo Tweet y sera igual a un Body parameter obligatorio
# 2.	Ahora trabajaremos con la lógica
# cambiaremos el .json por el tweets.json
# cambiaremos todos los users por tweet y en los tweet_dict los cambiaremos por los atributos del model Tweets
# 3.	Ahora nos toca castear a updated_at, pero si es que existe.
# Para ello utilizaremos la condicional
# Si existe updated_at, en updated_at vamos a castear su contenido a string
# if tweet_dict[“updated_at”]:
#          tweet_dict[“updated_at”] = str(tweet_dict[“updated_at”])
# 4.	Si nos vamos a la documentación interactiva y nos vamos a Create a Tweet
# Si le damos try it out y le cambiamos el contenido para el ejemplo
 
# Tenemos un error 500.
# Vamos al traceback y nos dice que tenemos un key error
# Vamos a remover el condicional en update_at
# Ahora si ejecutamos de nuevo, tenemos otro error 5000 que nos dice
# Objecto of type UUID is not JSON serializable. Es decir que tenemos un archivo tipo UUID que tiene algo que no puede pertenecer a un .json
# Si nos fijamos en el código, veremos que todo parece bien casteado.
# Si nos vamos a la documentación interactiva y vemos la estructura del reques body veremos que tendremos un tweet_id convertido a string que si se podría guardar en un JSON. 
# {
#   "tweet_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#   "content": "Primer tweet de la historia",
#   "created_at": "2021-11-11T10:58:40.613605",
#   "update_at": "2021-11-11T15:59:54.669Z",
#   "by": {
#     "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#     "email": "felipe@example.com",
#     "first_name": "Felipe",
#     "last_name": "Restrepo",
#     "birth_date": "1997-11-11"
#   }
# }
# Sin embargo, es mas que lógico, hay un tipo UUID que no estamos serializando, este es el user_id
# Para castearlo a un string tenemos que acceder al tweet_dict y accedemos a la llave by, que se corresponde al usuario, y si accedemos a la llave by del diccionario, en otra lista podemos acceder a las llaves internas de ese diccionario, por lo que accedemos a user_id,
# De ahí solo queda castearlo convirtiendo lo mismo a un str
# 1.	Accedemos a tweet_dict[“by”][“user_id”] = str(tweet_dict[“by”][“user_id”])
# 2.	Haremos lo mismo con el birth_date que también tendremos que castearlo
# 3.	Si ahora nos vamos a la documentación interactiva y ejecutamos, veremos que tenemos un 201.




#IMPORTS

#Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI, status, Body

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

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

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
def signup(
    user: UserRegister = Body(...),
):
    """
    Signup

    This path operation register a user in the app

    Parameters:

        - Request body parameter

            - user: UserRegister
    
    Return a json with the basic user information

        - user_id: UUID

        - email: EmailStr

        - first_name: str

        - last_name: str

        - birth_date: date

    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user





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
    """
    This path opepration shows all users in the app

    Parameters:
        
        -
    
    Returns a json list with all users in the app, with the following keys
         
        - user_id: UUID

        - email: EmailStr

        - first_name: str

        - last_name: str

        - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

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
def create_tweet(
    tweet: Tweets = Body(...),
):
    """
    Create a tweet

    This path operation post a tweet in the app

    Parameters:

        - Request body parameter

            - tweet: Tweets
    
    Return a json with the basic tweet information

        - tweet_id: UUID 

        - content: str

        - created_at: datetime

        - update_at: Optional[datetime]
        
        - by: User

    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["update_at"] = str(tweet_dict["update_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


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