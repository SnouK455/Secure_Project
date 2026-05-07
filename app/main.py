from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.core.security import create_access_token
from app.db import Base, engine, get_db
from app.deps import get_current_user


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def add_security_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"name": settings.app_name, "status": "ok", "docs": "/docs"}


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt() -> str:
    return "User-agent: *\nDisallow:\n"


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserRegister, db: Session = Depends(get_db)) -> dict[str, str]:
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")
    try:
        crud.create_user(db, user_in)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered") from exc
    return {"message": "User created"}


@app.post("/auth/login", response_model=schemas.TokenOut)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)) -> schemas.TokenOut:
    user = crud.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return schemas.TokenOut(access_token=token)


@app.get("/notes", response_model=list[schemas.NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[models.Note]:
    return crud.get_notes_for_user(db, current_user.id)


@app.post("/notes", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Note:
    return crud.create_note(db, owner_id=current_user.id, note_in=note_in)


@app.get("/notes/{note_id}", response_model=schemas.NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Note:
    note = crud.get_note_for_user(db, current_user.id, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@app.put("/notes/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note_in: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Note:
    note = crud.get_note_for_user(db, current_user.id, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    if note_in.title is None and note_in.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    return crud.update_note(db, note=note, note_in=note_in)


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> None:
    note = crud.get_note_for_user(db, current_user.id, note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    crud.delete_note(db, note)
