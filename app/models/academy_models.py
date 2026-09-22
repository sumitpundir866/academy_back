from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

Base = declarative_base()

class ClassInfo(Base):
    __tablename__ = "class_info"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    age_group = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    role = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class GalleryclassVedio(Base):
    __tablename__ = "gallery_vedio"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
   

# class AboutInfo(Base):
#     __tablename__ = "about_info"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=True)
#     content = Column(Text, nullable=True)
#     mission = Column(Text, nullable=True)
#     vision = Column(Text, nullable=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

# class AcademyUser(Base):
#     __tablename__ = "academy_users"
    
#     userid = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True, nullable=False, index=True)
#     userrole = Column(String(100), nullable=False)
#     email = Column(String(100), unuique=True, nullable=True, index=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    user_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),  
        nullable=False
    )

    mobile_number: Mapped[str] = mapped_column(
        String(15),
        nullable=True,
        unique=True
    )

    user_role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    edit: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    delete: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    upload: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )