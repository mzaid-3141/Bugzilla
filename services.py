from auth import hash_password
import models

def create_user(db, user):
    db_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        password=hash_password("123456")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_project(db, project):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        project_manager_id=project.project_manager_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_manager_projects(db, manager_id):
    return db.query(models.Project).filter(
        models.Project.project_manager_id == manager_id
    ).all()

def assign_user_to_project(db, project_id, user_id, manager_id):
    project = db.query(models.Project).filter_by(id=project_id).first()
    user = db.query(models.User).filter_by(id=user_id).first()

    if not user:
        return {"error": "User not found"}

    if not project:
        return {"error": "Project not found"}

    if user.role not in ["qa", "developer"]:
        return {"error": "Only QA or Developer can be assigned"}

    if project.project_manager_id != manager_id:
        return {"error": "Not authorized for this project"}

    if user in project.users:
        return {"error": "User already assigned to this project"}

    project.users.append(user)
    db.commit()
    return {"message": "User assigned"}

def create_user_with_project(db, data):
    if data.role not in ["qa", "developer"]:
        return {"error": "Only QA or Developer can be created"}

    user = models.User(
        name=data.name,
        email=data.email,
        role=data.role,
        password=hash_password("123456")
    )

    project = db.query(models.Project).filter_by(id=data.project_id).first()

    if not project:
        return None

    project.users.append(user)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def add_comment(db, bug_id, data):
    bug = db.query(models.Bug).filter_by(id=bug_id).first()

    if data.user_id != bug.assigned_id:
        return {"message":"Dev is not assigned to this project"}
    
    comment = models.Comment(
        text=data.text,
        user_id=data.user_id,
        bug_id=bug_id
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}

def resolve_bug(db, bug_id, user_id):
    bug = db.query(models.Bug).filter_by(id=bug_id).first()

    if not bug:
        return None
    
    if bug.status == "resolved":
        return{"message":"Bug alreaady resolved"}

    bug.status = "resolved"
    bug.assigned_id = user_id
    db.commit()

    return {"message": "Bug resolved"}

def create_bug(db, bug):
    db_bug = models.Bug(
        title=bug.title,
        description=bug.description,
        status="pending",
        project_id=bug.project_id,
        reported_by=bug.reported_by,
        assigned_id = None
    )
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug

def mark_done(db, bug_id):
    bug = db.query(models.Bug).filter_by(id=bug_id).first()

    if not bug:
        return None

    bug.status = "done"
    db.commit()

    return {"message": "Bug marked as done"}

def reopen_bug(db, bug_id, data):
    bug = db.query(models.Bug).filter_by(id=bug_id).first()

    if not bug:
        return None

    bug.status = "pending"
    bug.assigned_id = None

    comment = models.Comment(
        text=data.text,
        user_id=data.user_id,
        bug_id=bug_id
    )

    db.add(comment)
    db.commit()

    return {"message": "Bug reopened"}
