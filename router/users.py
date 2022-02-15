from schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from db import user_db
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/create_user', response_model=UserDisplay)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return user_db.create_user(db, request)


@router.get('/get_user', response_model=UserDisplay)
async def get_user(db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return user_db.get_user(db, cur_user.id)


@router.put('/update')
async def update_user(request: UserBase, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return user_db.update_user(db, cur_user.id, request)


@router.delete('/delete')
async def delete_user(db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    return user_db.delete_user(db, cur_user.id)
