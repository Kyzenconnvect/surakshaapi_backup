from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi import APIRouter
import var, models
# from app.schemas import UserOut, UserAuth, TokenSchema
# from replit import db
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    JWT_REFRESH_SECRET_KEY,
    ALGORITHM
)
from uuid import uuid4
from jose import jwt
from models import TokenPayload
from datetime import datetime, timedelta

router = APIRouter()

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = "SELECT * FROM user WHERE phonenumber = %s;"
    var.cur.execute(query,(form_data.username,))
    customer = var.cur.fetchall()
    if(customer == []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    query = "SELECT pwd FROM user WHERE phonenumber = %s;"
    var.cur.execute(query,(form_data.username,))
    hashed_pass = var.cur.fetchall()
    if not verify_password(form_data.password, hashed_pass[0][0]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(form_data.username),
        "refresh_token": create_refresh_token(form_data.username),
    }

@router.post('/refreshtoken', summary="Refresh access token")
async def regenarate_access_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    new_access_token = create_access_token(token_data.sub)
    return {"access_token": new_access_token}
