from pydantic import BaseModel, EmailStr, constr

class RegisterSchema(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True