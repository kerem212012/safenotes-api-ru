import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, create_engine, select

from app import models  # noqa: F401  # ensures model metadata is registered
from app.models import User

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///safenotes.db")
engine = create_engine(DATABASE_URL)
password_hasher = PasswordHash.recommended()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="SafeNotes API", lifespan=lifespan)


class UserPublic(BaseModel):
    id: int
    username: str


class RegisterPayload(BaseModel):
    username: str
    password: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterPayload) -> UserPublic:
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.user_name == payload.username)).first()
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

        user = User(
            user_name=payload.username,
            password_hash=password_hasher.hash(payload.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return UserPublic(id=user.id, username=user.user_name)


# Add users, password hashing, JWT login, and owner-scoped notes.
