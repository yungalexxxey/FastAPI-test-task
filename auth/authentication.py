from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_db
from hash import Hash
from db import models
from auth import oauth2

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: models.DbUser = db.query(models.DbUser).filter(models.DbUser.name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this login doesn't exist")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong password")
    access_token = oauth2.create_access_token(data={'sub': user.name})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.name
    }
