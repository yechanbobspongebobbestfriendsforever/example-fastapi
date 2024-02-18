from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, utils
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post(path="/", 
          status_code=status.HTTP_201_CREATED, 
          response_model=schemas.UserOut)
def create_user(user: schemas.UserBase, db: Session=Depends(get_db)):
    
    #hash the password - user.password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict()) ## **: unpack the dictionary
    db.add(new_user) #add our new post object
    db.commit() #commit
    db.refresh(new_user) #retrieve that new post and store back to new_post variable
    ## until here, new_post is still sqlalchemy model
    return new_user

@router.get(path="/", response_model=List[schemas.UserOut]) 
def get_user(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    print(users)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"user db is empty"
        ) 

    return users

@router.get(path="/{id}", response_model=schemas.UserOut) 
def get_user(id: int,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"user with id {id} does not exist"
        ) 
    
    return user

