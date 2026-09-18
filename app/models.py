from sqlmodel import SQLModel, Field


class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    user_name: str = Field(unique=True, index=True)
    password_hash: str


class Note(SQLModel):
    id: int = Field(default=None, primary_key=True)
    user:int=Field(foreign_key="user.id",index=True)
    title:str
    content:str
