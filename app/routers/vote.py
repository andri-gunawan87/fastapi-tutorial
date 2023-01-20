from fastapi import status, Depends, Response, APIRouter, Request
from sqlalchemy.orm import Session

from .. import models, schema, oauth2
from ..database import get_db
from ..exception import main

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/")
def Votes(response: Response,
          vote: schema.Vote,
          db: Session = Depends(get_db),
          currentUser = Depends(oauth2.getCurrentUser)
):
    postData =  db.query(models.Post.id == vote.post_id).first()
    if not postData:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": "Post not found"}
    
    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                            models.Vote.user_id == currentUser.id)
    voteData = voteQuery.first()
    if vote.dir == 1:
        if voteData:
            response.status_code = status.HTTP_409_CONFLICT
            return {"data": "User already vote this posts"}
        try:
            newVote = models.Vote(post_id = vote.post_id, user_id = currentUser.id)
            db.add(newVote)
            db.commit()
            response.status_code = status.HTTP_201_CREATED
            return {"data": "Post voted"}
        except Exception as ex:
            errorData = f"Error in vote posts{ex}"
            raise main.InternalException(name = errorData)
    else:
        if not voteData:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"data": "Vote for this post not found"}
        voteQuery.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_201_CREATED
        return {"data": "Post vote removed"}