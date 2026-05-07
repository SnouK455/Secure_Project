from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def create_user(db: Session, user_in: schemas.UserRegister) -> models.User:
    db_user = models.User(
        email=user_in.email.lower(),
        password_hash=get_password_hash(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_note(db: Session, owner_id: int, note_in: schemas.NoteCreate) -> models.Note:
    note = models.Note(title=note_in.title.strip(), content=note_in.content.strip(), owner_id=owner_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes_for_user(db: Session, owner_id: int) -> list[models.Note]:
    return db.query(models.Note).filter(models.Note.owner_id == owner_id).order_by(models.Note.id.desc()).all()


def get_note_for_user(db: Session, owner_id: int, note_id: int) -> models.Note | None:
    return (
        db.query(models.Note)
        .filter(models.Note.id == note_id, models.Note.owner_id == owner_id)
        .first()
    )


def update_note(db: Session, note: models.Note, note_in: schemas.NoteUpdate) -> models.Note:
    if note_in.title is not None:
        note.title = note_in.title.strip()
    if note_in.content is not None:
        note.content = note_in.content.strip()
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: models.Note) -> None:
    db.delete(note)
    db.commit()
