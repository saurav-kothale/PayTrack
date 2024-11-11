from sqlalchemy import JSON, Boolean, Column, DateTime, String

from database.database import Base


class User(Base):
    __tablename__ = "user"
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, primary_key=True)
    user_id = Column(String , unique = True)
    email_id = Column(String, unique=True)
    mobile_no = Column(String, unique=True)
    password = Column(String)
    retype_password = Column(String)


class UserRecord(Base):
    __tablename__ = "user record"
    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
    retype_password = Column(String)
    is_admin = Column(Boolean)
    inventory_privileges = Column(JSON)
    salary_privileges = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean)

