import models


def get_all_users(db):
    return db.query(models.User).all()


def get_all_projects(db):
    return db.query(models.Project).all()


def get_all_bugs(db):
    return db.query(models.Bug).all()



def get_manager_bugs(db, manager_id):
    # get projects managed by this manager
    projects = db.query(models.Project).filter_by(project_manager_id=manager_id).all()
    project_ids = [p.id for p in projects]

    if not project_ids:
        return []

    # get bugs in those projects
    return db.query(models.Bug).filter(models.Bug.project_id.in_(project_ids)).all()



def get_developer_bugs(db, user_id):
    user = db.query(models.User).filter_by(id=user_id).first()

    if not user:
        return []

    project_ids = [p.id for p in user.projects]

    if not project_ids:
        return []

    return db.query(models.Bug).filter(models.Bug.project_id.in_(project_ids)).all()



def get_resolved_bugs(db):
    return db.query(models.Bug).filter_by(status="resolved").all()