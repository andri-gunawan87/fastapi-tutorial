from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schema, database, models
from .exception import main
from .config import settings

oauthSchema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

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
    
def getCurrentUser(tokenData: str = Depends(oauthSchema), db: Session = Depends(database.get_db)):
    credentialException = main.UnauthorizedException(message = "errorData")
    tokenData = verifyAccessToken(tokenData, credentialException)
    userData = db.query(models.User).filter(models.User.id == tokenData.id).first()
    return userData