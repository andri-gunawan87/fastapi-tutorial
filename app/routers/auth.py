from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schema, models, utils, oauth2
from ..exception import main

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schema.TokenResponse)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db)):
    userData = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not userData:
        errorMesseage = "Invalid Email/Password"
        raise main.UnauthorizedException(message=errorMesseage)
    
    if not utils.verify(userCredentials.password, userData.password):
        errorMesseage = "Invalid Email/Password"
        raise main.UnauthorizedException(message=errorMesseage)
    
    accessToken = oauth2.createAccessToken(data= {"userId": str(userData.id)})
    return {"data": {"token": accessToken,
                     "schemaType": "bearer"}}
    