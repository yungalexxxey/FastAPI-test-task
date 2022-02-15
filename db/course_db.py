import shutil

from hash import Hash
from sqlalchemy.orm.session import Session
from schemas import CourseBase
from db.models import DbCourse, DbAssociation, DbFile, DbUser
from fastapi import HTTPException, status, UploadFile, File
import os


def create_course(name: str, db: Session, id: int):
    if id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    new_course = DbCourse(
        name=name,
        rating=0
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


def rate_course(name: str, db: Session):
    course = db.query(DbCourse).filter(DbCourse.name == name)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_rating = course.first().rating + 1
    course.update({
        DbCourse.rating: new_rating
    })
    db.commit()
    return 'ok'


def delete_course(name: str, db: Session, id: int):
    if id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    connect = db.query(DbAssociation).filter(DbAssociation.course_id == course.id)
    for con in connect:
        db.delete(con)
    db.delete(course)
    db.commit()
    return 'ok'


def get_course(name: str, db: Session):
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return course


def update_course(name: str, request: CourseBase, db: Session, id: int):
    if id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course: DbCourse = db.query(DbCourse).filter(DbCourse.name == name)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    course.update({
        DbCourse.name: request.name
    })
    db.commit()
    return 'ok'


def add_course(name: str, user_id: int, db: Session):
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    connect = db.query(DbAssociation).filter(DbAssociation.user_id == user_id,
                                             DbAssociation.course_id == course.id).first()
    if connect:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    new_connect = DbAssociation(
        user_id=user_id,
        course_id=course.id
    )
    db.add(new_connect)
    db.commit()
    return 'ok'


def delete_course_from_user(name: str, user_id: int, db: Session):
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    connect = db.query(DbAssociation).filter(DbAssociation.user_id == user_id,
                                             DbAssociation.course_id == course.id).first()
    db.delete(connect)
    db.commit()
    return 'ok'
