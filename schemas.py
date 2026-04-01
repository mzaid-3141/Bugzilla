from pydantic import BaseModel

# ---------------- USER ----------------
class UserCreate(BaseModel):
    name: str
    email: str
    role: str

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


# ---------------- PROJECT ----------------
class ProjectCreate(BaseModel):
    name: str
    description: str
    project_manager_id: int

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        orm_mode = True


# ---------------- BUG ----------------
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


# ---------------- COMMENT ----------------
class CommentCreate(BaseModel):
    text: str
    user_id: int
    bug_id: int

class CommentResponse(CommentCreate):
    id: int

    class Config:
        from_attributes = True