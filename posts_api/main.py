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

    # Check if MLname already exists, if it does, raise an error message
    if session.query(Models).filter(Models.MLname == post.MLname).first() is not None:
        raise fastapi.HTTPException(status_code=400, detail="Model with this name already exists")
    else:
        session.add(post)
        session.commit()
        # return the post_id
        return {"post_id": post.post_id}

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

# ----
# FUTURE CHANGES
# ----

# Future DB changes
# 1. Delete like and dislike columns from the posts table
# 2. Add a table for likes and dislikes:
#    likeDislikeTable(user_id, post_id, likeOrDislike[0,1])


# Future API endpoints
# 1. Get like for a post
# 2. Get dislike for a post
# 3. Calculate Merit for a user
# 4. Sort Queries:
#   - Sort by date
#   - Sort by Like/Dislike ratio
#   - Sort by User Merit

# Like A Post
@app.post("/posts/like/{post_id}/{user_id}")
async def like_post(post_id: int, user_id: int):
    # Steps:
    # 1. Check if user_id, post_id pair already exists in the likeDislikeTable
    # 2. If it does, check if it is a like or dislike
    # 3. If it is a like, return an error message
    # 4. If it is a dislike, change it to a like
    # 5. If it does not exist, add a like to the likeDislikeTable

    pass

# Dislike A Post
@app.post("/posts/dislike/{post_id}/{user_id}")
async def dislike_post(post_id: int, user_id: int):
    pass

# Get Like for a post
@app.get("/posts/getlike/{post_id}")
async def get_like(post_id: int):
    pass

# Get Dislike for a post
@app.get("/posts/getdislike/{post_id}")
async def get_dislike(post_id: int):
    pass

# Calculate Merit for a user
@app.get("/posts/calculateusermerit/{user_id}")
async def calculate_user_merit(user_id: int):
    pass

# Sort Queries
@app.get("/posts/sortbydate/{amount}")
async def sort_by_date(amount: int):
    pass

@app.get("/posts/sortbylikedislikeratio/{amount}")
async def sort_by_like_dislike_ratio(amount: int):
    pass

@app.get("/posts/sortbyusermerit/{amount}")
async def sort_by_user_merit(amount: int):
    pass

