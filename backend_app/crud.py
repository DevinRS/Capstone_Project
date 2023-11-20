from sqlalchemy.orm import Session

from . import models, schemas


# ----
# User
# ----
# Get a user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

# Get a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Get all users base on a range (from skip to limit)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Create a new User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user by username
def delete_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    db.delete(db_user)
    db.commit()
    return db_user


# ----
# Graph
# ----
# Get all graphs base on a range (from skip to limit)
def get_graphs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Graph).offset(skip).limit(limit).all()

# Create a new Graph
def create_user_graph(db: Session, graph: schemas.GraphCreate, user_id: int):
    db_graph = models.Graph(**graph.dict(), owner_id=user_id)
    db.add(db_graph)
    db.commit()
    db.refresh(db_graph)
    return db_graph

# delete all graphs
def delete_graphs(db: Session):
    db_graphs = db.query(models.Graph).all()
    for graph in db_graphs:
        db.delete(graph)
    db.commit()
    return db_graphs

# ----
# Mlmodel
# ----
# Get all mlmodels base on a range (from skip to limit)
def get_mlmodels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mlmodels).offset(skip).limit(limit).all()

# Create a new Mlmodel
def create_user_mlmodel(db: Session, mlmodel: schemas.MlmodelCreate, user_id: int):
    db_mlmodel = models.Mlmodels(**mlmodel.dict(), owner_id=user_id)
    db.add(db_mlmodel)
    db.commit()
    db.refresh(db_mlmodel)
    return db_mlmodel

# delete all mlmodels
def delete_mlmodels(db: Session):
    db_mlmodels = db.query(models.Mlmodels).all()
    for mlmodel in db_mlmodels:
        db.delete(mlmodel)
    db.commit()
    return db_mlmodels

# ----
# Post
# ----
# Get all posts base on a range (from skip to limit)
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

# Get a post by MLname
def get_post_by_MLname(db: Session, MLname: str):
    return db.query(models.Post).filter(models.Post.MLname == MLname).first()

# Create a new Post
def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# delete all posts
def delete_posts(db: Session):
    db_posts = db.query(models.Post).all()
    for post in db_posts:
        db.delete(post)
    db.commit()
    return db_posts
