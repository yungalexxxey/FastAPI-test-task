import os
import shutil
import zipfile

from schemas import UserBase, UserDisplay, CourseBase, CourseDisplay
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from db.database import get_db
from sqlalchemy.orm import Session
from db import course_db
from auth.oauth2 import get_current_user
from router.course_files import router as course_files_router

router = APIRouter(
    prefix='/course',
    tags=['course']
)
router.include_router(course_files_router)


@router.delete('/{name}/delete')
async def delete_course_from_user(name: str, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_db.delete_course_from_user(name, cur_user.id, db)


@router.get('/{name}', response_model=CourseDisplay)
def get_course(name: str, db: Session = Depends(get_db),cur_user=Depends(get_current_user)):
    return course_db.get_course(name, db)


@router.post('/create/{name}')
def create_course(name: str, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_db.create_course(name, db, cur_user.id)


@router.put('/{name}/update')
def update_course(name: str, request: CourseBase, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_db.update_course(name, request, db, cur_user.id)


@router.delete('/{name}/delete/')
def delete_course(name: str, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_db.delete_course(name, db, cur_user.id)


@router.post('/{name}/rate', tags=['user'])
def rate_course(name: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return course_db.rate_course(name, db)


@router.post('/add/{name}',tags=['user'])
async def connect_to_course(name: str, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_db.add_course(name, cur_user.id, db)









