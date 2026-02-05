from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from app.router import oauth2
router = APIRouter(
    prefix= "/posts",
    tags=["posts"]
)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "i like pizza", "id": 2},
]  # in memory variable but in real porj it will be db


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# when request comes in get method url is gonna be "/" it checks one by one which path matches order matters

# @router.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Posts).all()
#     return {"data": posts}





# get all posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] =""):
    # 1. FastAPI runs get_db until the 'yield'
    # 2. You use 'db' here to do your work
    # 3. When this function returns, FastAPI goes back to get_db and runs 'db.close()'
    # cursor.execute("""select title, content from posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    result  = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return result


# add post but onnly if user is logged in
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)
):  # this will convert the payload to dict and store in payload variable
    # id = len(my_posts) + 1
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts.append(post_dict)
    # return {"data": post_dict}
    # cursor.execute(
    #     """INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # we can pass all keys using **
    new_post = models.Posts(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get individual post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int, response: Response, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)
):  # fastpai directly can access passed param so id is recived in def its str need to convert if want to compare with number
    # cursor.execute("""select * from posts where id= %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id{id} not found"
        )
    return post
    # post = find_post(id)
    # if post:
    #     return {"post_detail": post}
    # else:
    #     # response.status_code = 404 rather than remember each code just use status module it suggests u can check and give
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"msg": f"post with {id} was not found"}
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with {id} was not found",
    #     )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    # Check if list is empty first
    # cursor.execute("delete from posts where id = %s returning *", (id,))
    # my_posts  = cursor.fetchone()
    # conn.commit()
    # if not my_posts:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="No posts exist to delete"
    #     )

    # for index, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         my_posts.pop(index)
    #         # 204 means we return NOTHING.
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)

    # If the loop finishes without returning, the ID wasn't found
    my_posts = db.query(models.Posts).filter(models.Posts.id == id)
    post = my_posts.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform operation"
        ) 
    my_posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    my_posts = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = my_posts.first()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform operation"
        ) 
    my_posts.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return my_posts.first()
    # for index, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         updatepost = updatepost.model_dump()
    #         updatepost["id"] = id
    #         my_posts[index] = updatepost
    #         # 204 means we return NOTHING.
    # return updatepost
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
    # )
