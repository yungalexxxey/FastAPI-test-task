from hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser, DbCourse, DbAssociation
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):
    user = db.query(DbUser).filter(DbUser.name == request.name).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with that username already exist')
    user = db.query(DbUser).filter(DbUser.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with that username already exist')
    new_user = DbUser(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_name(db: Session, name: str):
    user = db.query(DbUser).filter(DbUser.name == name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user.update({
        DbUser.name: request.name,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
    return 'ok'
