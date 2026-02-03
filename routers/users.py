from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    id: int
    username: str
    age: int
    city: str

users = [
    User(id=1, username="user1", age=25, city="Medellin"), 
    User(id=2, username="user2", age=30, city="Los Angeles")]



@router.get("/")
async def get_users():
    return users

@router.get("/users")
async def get_all_users():
    return HTTPException(status_code=404, detail="User not found")

@router.get("/{id}")
async def get_user(id: int):
    return [user for user in users if user.id == id]





