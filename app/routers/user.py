from fastapi import status, Depends, Response, APIRouter
from sqlalchemy.orm import Session

from .. import models, schema, utils, oauth2
from ..database import get_db
from ..exception import main

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUserResponse)
def create_user(
    user: schema.CreateUserRequest, 
    response: Response, 
    db: Session = Depends(get_db)
):
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    
    isExistingEmail = db.query(models.User).filter(models.User.email == user.email).first()
    if isExistingEmail:
        statusCode = 422
        name = "This email already registered"
        raise main.InternalException(name=name, status=statusCode)
    try:
        newUser = models.User(**user.dict())
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return {"data": newUser}
    except Exception as ex:
        statusCode = 422
        raise main.InternalException(name=str(ex), status=statusCode)

@router.get('/detail/{id}', response_model=schema.CreateUserResponse)
def getUser(
    id,
    response: Response,
    db: Session = Depends(get_db),
    currentUser = Depends(oauth2.getCurrentUser),
):
    userData = db.query(models.User).filter(models.User.id == id).first()
    if not userData:
        errorData = f"Cant find user with id: {id}"
        raise main.NotFoundException(name = errorData)
    
    return {"data": userData}