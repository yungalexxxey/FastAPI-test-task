import shutil
import os

from sqlalchemy.orm.session import Session
from fastapi import UploadFile, HTTPException, status
from db.models import DbCourse, DbFile


def get_file_from_course(name: str, user_id: int, filename: str, db: Session):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    path = f"files/{name.replace(' ', '_')}/{filename}"
    file = db.query(DbFile).filter(DbFile.name == path)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return path


def upload_file_to_course(name: str, user_id: int, db: Session, upload_file: UploadFile):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    path = f"files/{str(course.name).replace(' ', '_')}/{upload_file.filename}"
    try:
        os.mkdir(f"files/{str(course.name).replace(' ', '_')}")
    except FileExistsError:
        pass
    with open(path, 'w+b') as f:
        shutil.copyfileobj(upload_file.file, f)
    new_file = DbFile(
        name=path,
        course_id=course.id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return {
        'filename': upload_file.filename,
        'type': upload_file.content_type,
        'url': new_file.name
    }


def delete_file_from_course(name: str, user_id: int, filename: str, db: Session):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must be admin')
    course = db.query(DbCourse).filter(DbCourse.name == name).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    path = f"files/{name.replace(' ', '_')}/{filename}"
    file = db.query(DbFile).filter(DbFile.name == path).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fail doesnt exist')
    os.remove(path)
    files = os.listdir(f"files/{name.replace(' ', '_')}")
    if not files:
        os.rmdir(f"files/{name.replace(' ', '_')}")
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(file)
    db.commit()
    return 'ok'
