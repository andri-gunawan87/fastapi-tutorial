from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schema, models, utils, oauth2
from ..exception import main

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    userData = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not userData:
        messeage = "Invalid Email/Password"
        raise main.NotFoundException(name=messeage)
    
    if not utils.verify(userCredentials.password, userData.password):
        messeage = "Invalid Email/Password"
        raise main.NotFoundException(name=messeage)
    
    accessToken = oauth2.createAccessToken(data= {"userId": str(userData.id)})
    return {"data": {"token": accessToken,
                     "schema": "bearer"}}
    