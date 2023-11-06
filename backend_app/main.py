from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----
# User
# ----
# API endpoints 1: create a new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# API endpoints 2: get a user based on range from skip to limit
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# API endpoints 3: delete a user based on username
@app.delete("/users/{username}", response_model=schemas.User)
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Username not found")
    return crud.delete_user(db=db, username=username)


# ----
# Graph
# ----
# API endpoints 4: create a new graph for a user
@app.post("/users/{user_id}/graphs/", response_model=schemas.Graph)
def create_graph_for_user(
    user_id: int, graph: schemas.GraphCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_graph(db=db, graph=graph, user_id=user_id)

# API endpoints 5: get all graphs based on range from skip to limit
@app.get("/graphs/", response_model=list[schemas.Graph])
def read_graphs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    graphs = crud.get_graphs(db, skip=skip, limit=limit)
    return graphs

# API endpoints 6: delete all graphs
@app.delete("/graphs/", response_model=list[schemas.Graph])
def delete_graphs(db: Session = Depends(get_db)):
    return crud.delete_graphs(db=db)


# ----
# Mlmodel
# ----
# API endpoints 7: create a new mlmodel for a user
@app.post("/users/{user_id}/mlmodels/", response_model=schemas.Mlmodel)
def create_mlmodel_for_user(
    user_id: int, mlmodel: schemas.MlmodelCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_mlmodel(db=db, mlmodel=mlmodel, user_id=user_id)

# API endpoints 8: get all mlmodels based on range from skip to limit
@app.get("/mlmodels/", response_model=list[schemas.Mlmodel])
def read_mlmodels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    mlmodels = crud.get_mlmodels(db, skip=skip, limit=limit)
    return mlmodels

# API endpoints 9: delete all mlmodels
@app.delete("/mlmodels/", response_model=list[schemas.Mlmodel])
def delete_mlmodels(db: Session = Depends(get_db)):
    return crud.delete_mlmodels(db=db)


# ----
# Post
# ----
# API endpoints 10: create a new post for a user
@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # check if MLname already exists
    db_post = crud.get_post_by_MLname(db, MLname=post.MLname)
    if db_post:
        raise HTTPException(status_code=400, detail="MLname already registered")
    return crud.create_user_post(db=db, post=post, user_id=user_id)

# API endpoints 11: get all posts based on range from skip to limit
@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# API endpoints 12: delete all posts
@app.delete("/posts/", response_model=list[schemas.Post])
def delete_posts(db: Session = Depends(get_db)):
    return crud.delete_posts(db=db)

