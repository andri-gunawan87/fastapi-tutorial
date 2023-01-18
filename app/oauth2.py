from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from . import schema
from .exception import main

oauthSchema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "3272357538782F413F4428472B4B6250645367566B5970337336763979244226"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createAccessToken(data: dict):
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt

def verifyAccessToken(tokenData, credentialExceptions):
    try:
        payload = jwt.decode(tokenData, SECRET_KEY, algorithms=[ALGORITHM])
        userId = payload.get("userId")
        if userId is None:
            raise credentialExceptions
        tokenDataId = schema.TokenData(id = userId)
    except JWTError:
        raise credentialExceptions
    return tokenDataId
    
def getCurrentUser(tokenData: str = Depends(oauthSchema)):
    credentialException = main.UnauthorizedException(message = "errorData")
    return verifyAccessToken(tokenData, credentialException)