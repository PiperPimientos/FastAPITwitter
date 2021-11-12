#Path Operation Show Specific User



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
from fastapi import FastAPI, status, Body, Form, Path, HTTPException

app = FastAPI()

#MODELS

#User Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class PasswordMixin(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    

class UserLogin(PasswordMixin, UserBase):
    pass

class UserLoginOut(UserBase):
    message: str = Field(default="Login Succesfully!")

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

# @app.get(path="/")
# def home():
#     return {"Twitter API": "Working"}


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
    response_model=UserLoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(email: EmailStr = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a user in the app with a form

    Parameters:

        - Request body parameter

            - Form: UserLogin
    
    Return a json with UserLoginOut

        - user_id: UUID

        - email: EmailStr

        - message: str

    """    
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        login_dict = login.dict()
        login_dict["email"] = str(login_dict["email"])
        login_dict["password"] = str(login_dict["password"])
        if login_dict["email"] == email and login_dict["password"] == password:
            return UserLoginOut
        return results


@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users in the app

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
def show_specific_user(
            user_id: str = Path(
                ..., 
                gt=0,
                title="Person",
                description="Showing id person"
                ), 
):
    """
    This path operation shows a specific user information in the app

    Parameters:
        
        -
    
    Returns a json list with specific user in the app, with the following keys
         
        - user_id: UUID

        - email: EmailStr

        - first_name: str

        - last_name: str

        - birth_date: date
    """   
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user_id.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        if user_id not in user_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This person doesnt exist"
            )
        return {results: "It exists!"}
        return results

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
    """
    This path opepration shows all tweets in the app

    Parameters:
        
        -
    
    Returns a json list with all tweets in the app, with the following keys
         
        - tweet_id: UUID 

        - content: str

        - created_at: datetime

        - update_at: Optional[datetime]
        
        - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

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