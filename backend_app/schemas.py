from pydantic import BaseModel

class PostBase(BaseModel):
    MLname: str
    description: str
    long_description: str
    pickle_model: str
    rating: int
    uploadTime: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    post_id: int
    owner_id: int

    class Config:
        orm_mode = True

class MlmodelBase(BaseModel):
    sample_settings: str
    pickle_file: str


class MlmodelCreate(MlmodelBase):
    pass


class Mlmodel(MlmodelBase):
    model_id: int
    owner_id: int

    class Config:
        orm_mode = True


class GraphBase(BaseModel):
    graph_type: str
    X_axis: str
    Y_axis: str
    X_label: str
    Y_label: str
    title: str
    line_color: str
    label_color: str
    tick_color: str
    transparency: bool


class GraphCreate(GraphBase):
    pass


class Graph(GraphBase):
    graph_id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    graphs: list[Graph] = []
    mlmodels: list[Mlmodel] = []
    posts: list[Post] = []

    class Config:
        orm_mode = True
