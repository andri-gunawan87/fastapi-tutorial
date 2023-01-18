from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "3272357538782F413F4428472B4B6250645367566B5970337336763979244226"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createAccessToken(data: dict):
    toEncode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt