from sqlalchemy import Integer, String, Text, SmallInteger, Date, DateTime, func, ForeignKey, Boolean, text, Enum as SQLEnum, UniqueConstraint
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from app.database.init_db import Base

# class User(Base):
#     __tablename__ = "userinformation"

#     userid: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
#     role_id:Mapped[int] = mapped_column(ForeignKey("roleinformation.role_id"), index=True)
#     username: Mapped[str] = mapped_column(Text, unique=True, index=True)
#     password: Mapped[str] = mapped_column(Text)
#     enabled: Mapped[int] = mapped_column(SmallInteger)
#     accountnonexpired: Mapped[int] = mapped_column(SmallInteger)
#     accountnonlocked: Mapped[int] = mapped_column(SmallInteger)
#     credentialsnonexpired: Mapped[int] = mapped_column(SmallInteger)
#     rights: Mapped[int] = mapped_column(SmallInteger)

#     state_code: Mapped[int | None] = mapped_column(Integer)
#     mobile_number: Mapped[str | None] = mapped_column(String(12))
#     email_id: Mapped[str | None] = mapped_column(
#         String(70), unique=True, index=True
#     )

#     privilege: Mapped[str | None] = mapped_column(String)
#     designation: Mapped[str | None] = mapped_column(String(100))
#     loginname: Mapped[str | None] = mapped_column(String(150))

#     created_on: Mapped[datetime] = mapped_column(
#         DateTime(timezone=False),
#         server_default=func.now()
#     )
#     updated_on: Mapped[datetime | None] = mapped_column(
#         DateTime(timezone=False),
#         onupdate=func.now()
#     )

#     created_by: Mapped[str | None] = mapped_column(String(70))
#     updated_by: Mapped[str | None] = mapped_column(String(70))

#     project_name_old: Mapped[str | None] = mapped_column(String)
#     project_name: Mapped[int | None] = mapped_column(Integer)
#     unit_subunit: Mapped[str | None] = mapped_column(String)

#     status: Mapped[int | None] = mapped_column(Integer)
#     rank_id: Mapped[int | None] = mapped_column(Integer)

#     stcode: Mapped[str | None] = mapped_column(String)
#     dtcode: Mapped[str | None] = mapped_column(String)
#     fmn_code: Mapped[str | None] = mapped_column(String)

#     passwd_change_status: Mapped[int | None] = mapped_column(Integer)

#     sus_no: Mapped[str | None] = mapped_column(String(8), index=True)
#     army_no: Mapped[str | None] = mapped_column(String(9))

#     ac_dc_date: Mapped[date | None] = mapped_column(Date)

#     unit: Mapped[str | None] = mapped_column(String)
#     sub_unit: Mapped[str | None] = mapped_column(String)
#     bde: Mapped[str | None] = mapped_column(String)
#     div: Mapped[str | None] = mapped_column(String)
#     corps: Mapped[str | None] = mapped_column(String)

#     ic_no: Mapped[str | None] = mapped_column(String)

#     user_roles = relationship("Role",back_populates="role_users")

# class Role(Base):
#     __tablename__ = "roleinformation"

#     role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
#     role: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
#     access_lvl: Mapped[int | None] = mapped_column(SmallInteger, ForeignKey("hierarchy_levels.level_hierarchy"))
#     sub_access_lvl: Mapped[str | None] = mapped_column(String(255))
#     view: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
#     data_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false" ))
#     approve: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
#     role_url: Mapped[str | None] = mapped_column(String(255))
#     staff_lvl: Mapped[str] = mapped_column(String(100), nullable=False)

#     role_users = relationship("User", back_populates="user_roles", cascade="all, delete-orphan")
#     hierarchyLevels = relationship("HierarchyLevel", back_populates="role")

# class HierarchyLevel(Base):
#     __tablename__ = "hierarchy_levels"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#         index=True
#     )

#     level_name: Mapped[str] = mapped_column(
#         String(50),
#         nullable=False,
#         unique=True
#     )

#     level_hierarchy: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#         unique=True
#     )

#     role = relationship("Role", back_populates="hierarchyLevels")

# class StaffRank(Base):
#     __tablename__ = "staff_rank"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True
#     )

#     rank_name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True
#     )

#     rank_hierarchy: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#         unique=True
#     )

# class ModuleMaster(Base):
#     __tablename__ = "module_master"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#         index=True
#     )

#     module_name: Mapped[str | None] = mapped_column(
#         String(255), unique=True
#     )

#     module_url: Mapped[str | None] = mapped_column(
#         String(255)
#     )

#     module_id: Mapped[int | None] = mapped_column(
#         Integer
#     )

# class ScreenType(str, Enum):
#     SIDEBAR = "SIDEBAR"
#     NAVBAR = "NAVBAR"
#     PAGE = "PAGE"
    
# class Screens(Base):
#     __tablename__ = "screens"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#         index=True
#     )

#     screen_name: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False
#     )

#     screen_url: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False
#     )

#     module_id: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False
#     )

#     submodule_id: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False
#     )

#     sc_type: Mapped[ScreenType | None] = mapped_column(
#         SQLEnum(
#             ScreenType,
#             name="screen_type_enum",
#             create_constraint=True
#         ),
#         nullable=True
#     )

#     category: Mapped[str | None] = mapped_column(
#         String(100)
#     )

# class RoleScreenMap(Base):
#     __tablename__ = "role_screen_map"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#         index=True
#     )

#     role_id: Mapped[int | None] = mapped_column(Integer)
#     module_id: Mapped[int | None] = mapped_column(Integer)
#     submodule_id: Mapped[int | None] = mapped_column(Integer)
#     screen_id: Mapped[int | None] = mapped_column(Integer)

#     created_by: Mapped[str | None] = mapped_column(String(255))
#     created_date: Mapped[datetime | None] = mapped_column(
#         DateTime(timezone=False)
#     )

#     modify_by: Mapped[str | None] = mapped_column(String(255))
#     modify_date: Mapped[datetime | None] = mapped_column(
#         DateTime(timezone=False)
#     )

#     creation_by: Mapped[str | None] = mapped_column(String(255))
#     creation_date: Mapped[datetime | None] = mapped_column(
#         DateTime(timezone=False)
#     )
#     susno: Mapped[str | None] = mapped_column(String(100))

# class MstOrbat(Base):
#     __tablename__ = "mst_orbat"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#         index=True,
#     )

#     div_name: Mapped[str | None] = mapped_column(String)
#     bde_name: Mapped[str | None] = mapped_column(String)
#     unit_name: Mapped[str | None] = mapped_column(String)
#     fmn_code: Mapped[str | None] = mapped_column(String)
#     lvl_in_hierarchy: Mapped[str | None] = mapped_column(String)
#     sus_no: Mapped[str | None] = mapped_column(String)

#     created_by: Mapped[str | None] = mapped_column(String)
#     created_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))

#     modified_by: Mapped[str | None] = mapped_column(String)
#     modified_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))

#     deleted_by: Mapped[str | None] = mapped_column(String)
#     deleted_on: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))

#     status: Mapped[str | None] = mapped_column(String)
#     cmd_name: Mapped[str | None] = mapped_column(String)
#     corps_name: Mapped[str | None] = mapped_column(String)
#     name: Mapped[str | None] = mapped_column(String)
