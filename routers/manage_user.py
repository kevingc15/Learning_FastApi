from fastapi import FastAPI, HTTPException, status
from db.client import client

from db.models.user import User
from db.schemas.user import user_schema

app = FastAPI()



@app.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists.")
    
    user_dict = dict(user)
    del user_dict["id"]
    id = client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(client.users.find_one({"_id": id}))

    return User(**new_user)
    


def search_user(field: any, key):
    try:
        user = client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"message": "An error occurred while searching for the user."}