from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import PickleType

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    graphs = relationship("Graph", back_populates="owner")
    mlmodels = relationship("Mlmodels", back_populates="owner")
    posts = relationship("Post", back_populates="owner")

class Graph(Base):
    __tablename__ = "graphs"

    graph_id = Column(Integer, primary_key=True, index=True)
    graph_type = Column(String, index=True)
    X_axis = Column(String, index=True)
    Y_axis = Column(String, index=True)
    X_label = Column(String, index=True)
    Y_label = Column(String, index=True)
    title = Column(String, index=True)
    line_color = Column(String, index=True)
    label_color = Column(String, index=True)
    tick_color = Column(String, index=True)
    transparency = Column(Boolean, index=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="graphs")

class Mlmodels(Base):
    __tablename__ = "mlmodels"

    model_id = Column(Integer, primary_key=True, index=True)
    sample_settings = Column(String, index=True)
    pickle_file = Column(PickleType, index=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="mlmodels")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    MLname = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    long_description = Column(String, index=True)
    pickle_model = Column(PickleType, index=True)
    rating = Column(Integer, index=True)
    uploadTime = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="posts")

