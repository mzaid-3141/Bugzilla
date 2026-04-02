from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal
import services
import os

router = APIRouter()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(required_roles: list):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_checker



@router.post("/admin/users")
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db),
                current_user=Depends(require_role(["admin"]))):
    return services.create_user(db, user)

@router.post("/admin/projects")
def create_project(project: schemas.ProjectCreate,
                   db: Session = Depends(get_db),
                   current_user=Depends(require_role(["admin"]))):
    return services.create_project(db, project)

@router.get("/manager/projects/{manager_id}")
def get_projects(manager_id: int,
                 db: Session = Depends(get_db),
                 current_user=Depends(require_role(["manager"]))):
    return services.get_manager_projects(db, manager_id)

@router.post("/manager/projects/{project_id}/assign/{user_id}")
def assign_user(project_id: int,
                user_id: int,
                db: Session = Depends(get_db),
                current_user=Depends(require_role(["manager"]))):

    manager_id = current_user["user_id"]

    return services.assign_user_to_project(db, project_id, user_id, manager_id)

@router.post("/manager/users-with-project")
def create_user_with_project(data: schemas.UserWithProject,
                             db: Session = Depends(get_db),
                             current_user=Depends(require_role(["manager"]))):
    return services.create_user_with_project(db, data)

@router.post("/developer/bugs/{bug_id}/comment")
def add_solution(bug_id: int,
                 data: schemas.CommentCreate,
                 db: Session = Depends(get_db),
                 current_user=Depends(require_role(["developer"]))):
    return services.add_comment(db, bug_id, data)

@router.post("/developer/bugs/{bug_id}/resolve")
def resolve_bug(bug_id: int,
                db: Session = Depends(get_db),
                current_user=Depends(require_role(["developer"]))):
    return services.resolve_bug(db, bug_id, current_user)

@router.post("/qa/bugs")
def create_bug(bug: schemas.BugCreate,
               db: Session = Depends(get_db),
               current_user=Depends(require_role(["qa"]))):
    return services.create_bug(db, bug)

@router.post("/qa/bugs/{bug_id}/done")
def mark_done(bug_id: int,
              db: Session = Depends(get_db),
              current_user=Depends(require_role(["qa"]))):
    return services.mark_done(db, bug_id)

@router.post("/qa/bugs/{bug_id}/reopen")
def reopen_bug(bug_id: int,
               data: schemas.CommentCreate,
               db: Session = Depends(get_db),
               current_user=Depends(require_role(["qa"]))):
    return services.reopen_bug(db, bug_id, data)