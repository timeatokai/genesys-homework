from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

DatabaseDep = Annotated[Session, Depends(get_db)]


@router.post("/create", response_model=User)
async def create_user(user: UserCreate, db: DatabaseDep):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already in use")

    return crud.create_user(db=db, user=user)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: DatabaseDep):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User ID not in database")

    return crud.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: DatabaseDep) -> int:
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User ID not in database")

    return crud.delete_user(db=db, user_id=user_id)


@router.get("/list", response_model=list[User])
async def list_users(db: DatabaseDep):
    return crud.list_users(db)
