from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.auth_utils import authenticate_user, create_access_token
from app.dependencies import get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(tags=["login"])


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = crud.get_user_by_name(db, form_data.username)
    if not authenticate_user(user, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    crud.update_user(db, user.id, {"last_login": datetime.now(timezone.utc)})
    access_token = create_access_token(
        data={"sub": user.name}, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(access_token=access_token, token_type="bearer")
