from datetime import datetime, timedelta, timezone
from typing import Annotated
from pwdlib import PasswordHash
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import jwt

password_hasher = PasswordHash.recommended()
app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "0f06b0245833804c7bc654725e455a273fe88c4712252a3e08b0d7261404309b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


async def hash_password(password: str):
    return password_hasher.hash(password)

async def verify_password(plain_password: str, hashed_password: str):
    return password_hasher.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = search_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_db =  authenticate_user(form.username, form.password)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    jwt_token = create_access_token(data={"sub": user_db.username})

    return {"access_token": jwt_token, "token_type": "bearer"}


@app.get("/users/me")
async def me(token: Annotated[str, Depends(oauth2)]):
    credentials_exception = HTTPException(
        status_code= 400,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = Token_data(username=username)
    except InvalidTokenError:
        raise credentials_exception


    user = search_user(username=token_data.username, type_user=True)
    if user is None:
        raise credentials_exception
    return user


class Token_data(BaseModel):
    username: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str


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


users_db = {
    "kevin": {
        "id": 1,
        "name": "Kevin",
        "email": "kevin@example.com",
        "age": 27,
        "city": "Medellin",
        "disabled": False,
        "username": "kevin",
        "password": "$2a$12$I7xcotb0XXGzjf9AxUeBHehQRvjviWG0m56j5bm29zyoUYAb4fDeu"
    },
    "alice": {
        "id": 2,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25,
        "city": "Los Angeles",
        "disabled": True,
        "username": "alice",
        "password": "$2a$12$2Pyr6PsUzKrjz0AW3UnMqezDX/LiBZ2T5.YGr.od4fbwI/EBjaDva"
    }
}