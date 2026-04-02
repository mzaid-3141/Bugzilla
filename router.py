from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services
import models
from database import SessionLocal
from auth import get_current_user 


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/admin/users")
def get_users(db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_all_users(db)


@router.get("/admin/projects")
def get_projects(db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_all_projects(db)


@router.get("/admin/bugs")
def get_bugs(db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_all_bugs(db)



@router.get("/manager/bugs")
def manager_bugs(db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):

    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_manager_bugs(db, current_user.id)



@router.get("/developer/bugs")
def developer_bugs(db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):

    if current_user.role != "developer":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_developer_bugs(db, current_user.id)



@router.get("/qa/bugs/resolved")
def qa_resolved_bugs(db: Session = Depends(get_db),
                     current_user=Depends(get_current_user)):

    if current_user.role != "qa":
        raise HTTPException(status_code=403, detail="Not authorized")

    return services.get_resolved_bugs(db)