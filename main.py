from fastapi import FastAPI, Depends, HTTPException
import services as _services
import sqlalchemy.orm as _orm
import schemas as _schemas
import typing
import datetime as _dt

app = FastAPI()
_services.create_database()

@app.post("/users/", response_model= _schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session=Depends(_services.get_db)):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="whoops the email is in use")
    return _services.create_user(db=db, user=user)

@app.get("/users/", response_model=list[_schemas.User])
def read_users(skip: int=0, limit: int=10, db: _orm.Session=Depends(_services.get_db)):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session=Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(user_id: int, post: _schemas.PostCreate, db:_orm.Session=Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
       raise HTTPException(status_code=404, detail="User not found")
    return _services.create_post(db=db, user_id=user_id, post=post)

@app.get("/posts/", response_model=list[_schemas.Post])
def read_posts(skip: int=0, limit: int=10, db: _orm.Session=Depends(_services.get_db)):
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session=Depends(_services.get_db)):
    db_post = _services.get_post(db=db, post_id=post_id)
    if db_post is None:
        HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.put("/posts/{post_id}/edit/", response_model=_schemas.Post)
def edit_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session=Depends(_services.get_db)):
    return _services.edit_post(db=db, post_id=post_id, post=post)
    
@app.delete("/posts/{post_id}/delete/")
def delete_post(post_id: int, db: _orm.Session=Depends(_services.get_db)):
     _services.delete_post(db=db, post_id=post_id)
     return{"message": f"post with id {post_id} has been deleted"}
