from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas, utils, oauth2
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)


## login is post request as users need to pass credentials
@router.post(path="/login", response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm=Depends(), 
          db: Session=Depends(get_db)):
    #OAuth2PasswordRequestForm will only return username and password
    user = (db.query(models.User)
            .filter(models.User.email==user_credential.username)
            .first())
    
    if (not user) or (not utils.verify(user_credential.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials"
        ) 
    
    access_token = oauth2.create_access_token(
        data={"user_id":user.id}
    )
    
    return {"access_token":access_token, 
            "token_type":"bearer"}