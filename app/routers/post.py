from fastapi import status, Depends, Response, APIRouter, Request
from sqlalchemy.orm import Session

from .. import models, schema
from ..database import get_db
from ..exception import main

router = APIRouter(
    prefix="/posts"
)


@router.get("/", response_model=schema.ResponseDataAll)
async def getAllPost(
    response: Response, 
    db: Session = Depends(get_db)
):
    data = db.query(models.Post).all()
    response.status_code = status.HTTP_200_OK
    return {"data": data}

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schema.ResponseData)
def createPost(
    post: schema.CreatePost,
    response: Response, 
    db: Session = Depends(get_db)
):
    try:
        newPost = models.Post(**post.dict())
        print(newPost)
        db.add(newPost)
        db.commit()
        db.refresh(newPost)
        return {"data": newPost}
    except Exception as ex:
        errorData = f"Cant create post! {ex}"
        raise main.UnicornException(name = errorData)

@router.get("/detail/{id}", response_model=schema.ResponseData)
def getPost(
    id, 
    response: Response, 
    db: Session = Depends(get_db)
):
    try:
        data = db.query(models.Post).filter(models.Post.id == id).first()
        if data == None:
            errorData = f"Cant find post with id: {id}"
            raise main.UnicornException(name = errorData)
        return {"data": data}
    
    except Exception as ex:
        errorData = f"Cant find post with id: {id}"
        raise main.UnicornException(name = errorData)

@router.get("/delete/{id}", response_model=schema.ResponseData)
def deletePost(
    id, 
    response: Response, 
    db: Session = Depends(get_db)
):
    try:
        data = db.query(models.Post).filter(models.Post.id == id)
        if data.first() == None:
            errorData = f"Cant find user with id: {id}"
            raise main.UnicornException(name = errorData)
        data.delete(synchronize_session=False)
        db.commit()
        return {"data": "Success delete data"}
    except Exception as ex:
        errorData = f"Cant delete user with id: {id}"
        raise main.UnicornException(name = errorData)

@router.put("/update/{id}", 
         response_model=schema.ResponseData
)
def updatePost(
    id, 
    post: schema.CreatePost, 
    response: Response, 
    db: Session = Depends(get_db)
):
    try:
        baseQuery = db.query(models.Post).filter(models.Post.id == id)
        data = baseQuery.first()
        if data == None:
            errorData = f"Cant finda post with id {id}"
            raise main.UnicornException(name = errorData)
        baseQuery.update(post.dict(), synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_202_ACCEPTED
        return {"data": baseQuery.first()}
    except Exception as ex:
        errorData = f"Cant update user with id: {id}"
        raise main.AnotherException(name = errorData, message=errorData, status=404)