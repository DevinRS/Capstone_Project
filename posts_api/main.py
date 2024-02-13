from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import PickleType
import datetime
import base64
import streamlit.components.v1 as components
import fastapi
from pydantic import BaseModel

# ----
# Defining the database objects
# ----

Base = declarative_base()


class Models(Base):
    #set table name and columns
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    MLname = Column("name", String)
    post_owner = Column("owner", String)
    description = Column("description", String)
    longDescription = Column("longDesc", String)
    numLikes = Column("likes", Integer)
    numDislikes = Column("dislikes", Integer)
    uploadTime = Column("date", String)

    def __init__ (self, MLname, post_owner, description, longDescription, numLikes, numDislikes, uploadTime):
        self.MLname = MLname
        self.post_owner = post_owner
        self.description = description
        self.longDescription = longDescription
        self.numLikes = numLikes
        self.numDislikes = numDislikes
        self.uploadTime = uploadTime
    
    def __repr__ (self):   
        return f"{self.MLname}, {self.description}, {self.longDescription}, {self.numLikes}, {self.numDislikes}, {self.uploadTime}"
        
# ----
# Defining the database connection
# ----
engine = create_engine("sqlite:///posts.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# ----
# Defining the Pydantic models
# ----
class PostBase(BaseModel):
    MLname: str
    post_owner: str
    description: str
    longDescription: str
    numLikes: int
    numDislikes: int
    uploadTime: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    post_id: int

    class Config:
        orm_mode = True

# Defining the FastAPI app
# ----
app = fastapi.FastAPI()

# ----
# Defining the API endpoints
# ----
@app.post("/posts/")
async def create_post(post: PostCreate):
    # Convert the Pydantic model to a SQLAlchemy model
    post = Models(MLname=post.MLname, post_owner=post.post_owner, description=post.description, longDescription=post.longDescription, numLikes=post.numLikes, numDislikes=post.numDislikes, uploadTime=post.uploadTime)
    session.add(post)
    session.commit()
    return post

@app.get("/posts/")
async def read_posts():
    posts = session.query(Models).all()
    return posts

@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    post = session.query(Models).filter(Models.post_id == post_id).first()
    return post

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: PostCreate):
    post = session.query(Models).filter(Models.post_id == post_id).first()
    post.MLname = post.MLname
    post.post_owner = post.post_owner
    post.description = post.description
    post.longDescription = post.longDescription
    post.numLikes = post.numLikes
    post.numDislikes = post.numDislikes
    post.uploadTime = post.uploadTime
    session.commit()
    return post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = session.query(Models).filter(Models.post_id == post_id).first()
    session.delete(post)
    session.commit()
    return post
