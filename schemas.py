from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str
    email: str


class Course(BaseModel):
    name: str
    rating: int

    class Config:
        orm_mode = True


class UserDisplay(BaseModel):
    name: str
    email: str
    courses: list[Course] = []

    class Config:
        orm_mode = True


class File(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CourseDisplay(BaseModel):
    name: str
    files: list[File]

    class Config:
        orm_mode = True