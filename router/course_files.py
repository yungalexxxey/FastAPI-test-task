from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm.session import Session
from fastapi.responses import FileResponse
from db.database import get_db
from auth.oauth2 import get_current_user
from db import course_files_db

router = APIRouter(
    prefix='/files',
    tags=['files']
)


@router.post('/{name}/upload')
async def add_file_to_course(name: str, db: Session = Depends(get_db), upload_file: UploadFile = File(...),
                             cur_user=Depends(get_current_user)):
    return course_files_db.upload_file_to_course(name, cur_user.id, db, upload_file)


@router.delete('/{name}/delete')
async def delete_file_from_course(name: str, filename: str, db: Session = Depends(get_db),
                                  cur_user=Depends(get_current_user)):
    return course_files_db.delete_file_from_course(name, cur_user.id, filename, db)


@router.get('/{name}/get', response_class=FileResponse)
async def get_course_file(name: str, filename: str, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return course_files_db.get_file_from_course(name, cur_user.id, filename, db)
