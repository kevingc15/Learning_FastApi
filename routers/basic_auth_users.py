from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    city: str
    disabled: bool

class UserDB(User):
    username: str
    password: str

def search_user(username: str, type_user: bool | None = None):
    if username in users_db:
        if type_user:
            return User(**users_db[username])
        return UserDB(**users_db[username])
        
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    return {"access_token": user.username, "token_type": "bearer"}
    

@app.get("/users/me")
async def me(token: str = Depends(oauth2)):
    user = search_user(token, type_user=True)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


users_db = {
    "kevin": {
        "id": 1,
        "name": "Kevin",
        "email": "kevin@example.com",
        "age": 27,
        "city": "Medellin",
        "disabled": False,
        "username": "kevin",
        "password": "password123"
    },
    "alice": {
        "id": 2,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25,
        "city": "Los Angeles",
        "disabled": True,
        "username": "alice",
        "password": "password456"
    }
}