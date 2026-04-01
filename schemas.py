from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    role: str

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str
    description: str
    project_manager_id: int

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        orm_mode = True


class BugCreate(BaseModel):
    title: str
    description: str
    status: str
    project_id: int
    reported_by: int

class BugResponse(BugCreate):
    id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    text: str
    user_id: int
    bug_id: int

class CommentResponse(CommentCreate):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str