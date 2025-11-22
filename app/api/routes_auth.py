from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from ..core.security import authenticate_user, create_access_token
from ..core.config import settings
from ..core.firebase import verify_firebase_token

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str

# LOGIN CON FIREBASE (id_token o uid)
class FirebaseLoginRequest(BaseModel):
    id_token: str = None


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/firebase", response_model=Token)
async def login_with_firebase(payload: FirebaseLoginRequest):
    try:
        print("Verifying Firebase token:", payload.id_token)
        decoded = verify_firebase_token(payload.id_token)
        print("Decoded Firebase token:", decoded)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase ID token",
        )

    uid = decoded.get("uid")
    email = decoded.get("email")

    if uid is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Firebase token does not contain a uid",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    claims = {
        "sub": uid,
    }
    if email:
        claims["email"] = email

    access_token = create_access_token(
        data=claims,
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}