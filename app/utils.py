from passlib.context import CryptContext

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)