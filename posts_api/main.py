from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
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

# 1. Delete like and dislike columns from the posts table
# 2. Add a table for likes and dislikes:
#    likeDislikeTable(user_id, post_id, likeOrDislike[0,1])
class LikeDislikeTable(Base):
    __tablename__ = "likeDislikeTable"
    likeDislike_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_name = Column("owner_name", String)
    post_id = Column("post_id", Integer)
    likeOrDislike = Column("likeOrDislike", Boolean)

    def __init__ (self, owner_name, post_id, likeOrDislike):
        self.owner_name = owner_name
        self.post_id = post_id
        self.likeOrDislike = likeOrDislike

    def __repr__ (self):
        return f"{self.owner_name}, {self.post_id}, {self.likeOrDislike}"


class Models(Base):
    #set table name and columns
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    MLname = Column("name", String)
    post_owner = Column("owner", String)
    description = Column("description", String)
    longDescription = Column("longDesc", String)
    uploadTime = Column("date", String)

    def __init__ (self, MLname, post_owner, description, longDescription, uploadTime):
        self.MLname = MLname
        self.post_owner = post_owner
        self.description = description
        self.longDescription = longDescription
        self.uploadTime = uploadTime
    
    def __repr__ (self):   
        return f"{self.MLname}, {self.description}, {self.longDescription}, {self.uploadTime}"
        
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
    uploadTime: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    post_id: int

    class Config:
        orm_mode = True

# ----
# Defining the Pydantic models for LikeDislike table
# ----
class LikeDislikeBase(BaseModel):
    owner_name: str
    post_id: int
    likeOrDislike: bool

class LikeDislikeCreate(LikeDislikeBase):
    pass

class LikeDislike(LikeDislikeBase):
    likeDislike_id: int

    class Config:
        orm_mode = True

# ----


# Defining the FastAPI app
# ----
app = fastapi.FastAPI()

# ----
# Defining the API endpoints
# ----
@app.post("/posts/")
async def create_post(post: PostCreate):
    # Convert the Pydantic model to a SQLAlchemy model
    post = Models(MLname=post.MLname, post_owner=post.post_owner, description=post.description, longDescription=post.longDescription, uploadTime=post.uploadTime)

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
    post.uploadTime = post.uploadTime
    session.commit()
    return post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = session.query(Models).filter(Models.post_id == post_id).first()
    session.delete(post)

    # Delete all likes and dislikes for the post
    likes_dislikes = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
    for entry in likes_dislikes:
        session.delete(entry)

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
@app.post("/like/{post_id}/{owner_name}/{likeOrDislike}")
async def like_post(post_id: int, owner_name: str, likeOrDislike: int):
    # check if the owner_name has already liked or disliked the post, if already exists, update the likeOrDislike
    entry_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).filter(LikeDislikeTable.owner_name == owner_name).first()
    if entry_by_id is not None:
        entry_by_id.likeOrDislike = likeOrDislike
        session.commit()
        return entry_by_id
    
    # if the owner_name has not liked or disliked the post, create a new entry
    entry = LikeDislikeTable(owner_name=owner_name, post_id=post_id, likeOrDislike=likeOrDislike)
    session.add(entry)
    session.commit()
    return entry

# Get like for a post given a post_id
@app.get("/getlike/{post_id}")
async def get_like(post_id: int):
    entry_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
    like = 0
    for entry in entry_by_id:
        if entry.likeOrDislike == 1:
            like += 1
    return {"like": like}

# Get dislike for a post given a post_id
@app.get("/getdislike/{post_id}")
async def get_dislike(post_id: int):
    entry_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
    dislike = 0
    for entry in entry_by_id:
        if entry.likeOrDislike == 0:
            dislike += 1
    return {"dislike": dislike}

# Calculate Merit for a user
@app.get("/calculateusermerit/{owner_name}")
async def calculate_user_merit(owner_name: str):
    merit = 0
    # get all post by owner_name
    posts_by_owner = session.query(Models).filter(Models.post_owner == owner_name).all()
    for post in posts_by_owner:
        post_id = post.post_id
        entry_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
        for entry in entry_by_id:
            if entry.likeOrDislike == 1:
                merit += 1
            else:
                merit -= 1

    # add merit based on how many posts the user has
    merit += len(posts_by_owner)

    # Find owner_name in likeDislikeTable
    # For each entry, add 1 merit for leaving a review
    entries_by_owner = session.query(LikeDislikeTable).filter(LikeDislikeTable.owner_name == owner_name).all()
    merit += len(entries_by_owner)

    return {"merit": merit}
    

# New Endpoint to get POSTS after denormalization which contains like and dislike count
@app.get("/postsdenormalized/")
async def read_posts_denormalized():
    posts = session.query(Models).all()
    posts_denormalized = []
    for post in posts:
        post_dict = post.__dict__
        post_id = post_dict["post_id"]
        post_dict["like"] = 0
        post_dict["dislike"] = 0
        entries_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
        for entry in entries_by_id:
            if entry.likeOrDislike == 1:
                post_dict["like"] += 1
            else:
                post_dict["dislike"] += 1
        posts_denormalized.append(post_dict)
    return posts_denormalized

# get denormalized post sorted by date, newest first
@app.get("/postsdenormalizedsortedbydate/")
async def read_posts_denormalized_sorted_by_date():
    posts = session.query(Models).order_by(Models.uploadTime.desc()).all()
    posts_denormalized = []
    for post in posts:
        post_dict = post.__dict__
        post_id = post_dict["post_id"]
        post_dict["like"] = 0
        post_dict["dislike"] = 0
        entries_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
        for entry in entries_by_id:
            if entry.likeOrDislike == 1:
                post_dict["like"] += 1
            else:
                post_dict["dislike"] += 1
        posts_denormalized.append(post_dict)
    return posts_denormalized

# get denormalized post sorted by model name
@app.get("/postsdenormalizedsortedbyname/")
async def read_posts_denormalized_sorted_by_name():
    posts = session.query(Models).order_by(Models.MLname).all()
    posts_denormalized = []
    for post in posts:
        post_dict = post.__dict__
        post_id = post_dict["post_id"]
        post_dict["like"] = 0
        post_dict["dislike"] = 0
        entries_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
        for entry in entries_by_id:
            if entry.likeOrDislike == 1:
                post_dict["like"] += 1
            else:
                post_dict["dislike"] += 1
        posts_denormalized.append(post_dict)
    return posts_denormalized

# get denormalized post sorted by like/dislike ratio
@app.get("/postsdenormalizedsortedbyratio/")
async def read_posts_denormalized_sorted_by_ratio():
    posts = session.query(Models).all()
    posts_denormalized = []
    for post in posts:
        post_dict = post.__dict__
        post_id = post_dict["post_id"]
        post_dict["like"] = 0
        post_dict["dislike"] = 0
        entries_by_id = session.query(LikeDislikeTable).filter(LikeDislikeTable.post_id == post_id).all()
        for entry in entries_by_id:
            if entry.likeOrDislike == 1:
                post_dict["like"] += 1
            else:
                post_dict["dislike"] += 1
        posts_denormalized.append(post_dict)

    # sort by like/dislike ratio, if both are 0, set the ratio to 0
    posts_denormalized.sort(key=lambda x: x["like"]/(x["like"] + x["dislike"]) if x["like"] + x["dislike"] != 0 else 0, reverse=True)
    return posts_denormalized

# Tester function to print likeDislikeTable
@app.get("/likeDislikeTable")
async def read_likeDislikeTable():
    likeDislikeTable = session.query(LikeDislikeTable).all()

    # Convert SQLAlchemy objects to dictionaries
    likeDislikeTable_dict = []
    for entry in likeDislikeTable:
        likeDislikeTable_dict.append(entry.__dict__)

    return likeDislikeTable_dict

