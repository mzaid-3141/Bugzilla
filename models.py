from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

project_users = Table(
    "project_users",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    projects = relationship("Project", secondary=project_users, back_populates="users")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    project_manager_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", secondary=project_users, back_populates="projects")

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    reported_by = Column(Integer, ForeignKey("users.id"))
    assigned_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    bug_id = Column(Integer, ForeignKey("bugs.id"))