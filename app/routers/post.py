from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(
    db: Session=Depends(get_db), 
    current_user:int=Depends(oauth2.get_current_user),
    limit:int=10,
    skip:int=0,
    search:Optional[str]=""
    ):
    
    ## normal SQL
    # cursor.execute(
    #     """
    #         SELECT * FROM posts 
    #         ORDER BY id ASC
    #     """
    # )
    # posts = cursor.fetchall()

    ## this is list of Post object

    # posts = db.query(models.Post)\
    #     .filter(models.Post.title.contains(search))\
    #     .limit(limit=limit)\
    #     .offset(skip)\
    #     .all()
        
    posts = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label('votes')
        ).join(
            models.Vote, 
            models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(
            limit=limit
        ).offset(
            skip
        ).all()
    # print(result)
        
    
    return posts


@router.get("/{id}", response_model=schemas.PostOut) ##{id} is called path parameter
def get_post(
    id: int,
    db: Session=Depends(get_db), 
    current_user:int=Depends(oauth2.get_current_user)
    ):
    
    ## normal SQL
    # cursor.execute(
    #     """
    #         SELECT * FROM posts 
    #         WHERE id = %s
    #     """,
    #     (str(id),)
    # )
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label('votes')
        ).join(
            models.Vote, 
            models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id {id} was not found"
        )
        
    return post


 ## url the user should go to create a post 
@router.post(path="/", 
          status_code=status.HTTP_201_CREATED, 
          response_model=schemas.Post)

def create_posts(post: schemas.PostCreate, 
                 db: Session=Depends(get_db), 
                 current_user:int=Depends(oauth2.get_current_user)
                 ): 
    
    # cursor.execute(
    #     """
    #         INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
    #         RETURNING *
    #     """, 
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()


    # new_post = models.Post(
    #     title=post.title, 
    #     content=post.content, 
    #     published=post.published
    # )

    new_post = models.Post(
        owner_id=current_user.id,
        **post.dict()
    ) 
    db.add(new_post) #add our new post object
    ## until here, new_post is still sqlalchemy model

    db.commit() #commit
    db.refresh(new_post) #retrieve the new post and store back to new_post variable
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session=Depends(get_db), 
    current_user:int=Depends(oauth2.get_current_user)
    ):
    # cursor.execute(
    #     """
    #         DELETE FROM posts 
    #         WHERE id = %s 
    #         RETURNING *
    #     """,
    #     (str(id),)
    # )
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id {id} was not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform the action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    post: schemas.PostCreate, 
    db: Session=Depends(get_db), 
    current_user:int=Depends(oauth2.get_current_user)
    ):
    # cursor.execute(
    #     """
    #         UPDATE posts SET title = %s, content = %s, published = %s 
    #         WHERE id = %s 
    #         RETURNING *
    #     """,
    #     (post.title, post.content, post.published, str(id))
    # )
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_first = post_query.first()
    
    if post_first == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id {id} was not found"
        )
    if post_first.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform the action")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()