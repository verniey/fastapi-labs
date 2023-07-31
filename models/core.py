
# Add a unique constraint on the menu_id column to enforce that each Submenu can only belong to one Menu
# __table_args__ = (UniqueConstraint('menu_id'),)


from models.database import engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


class Menu(Base):
    __tablename__ = "menus" 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True, unique=False)
    description = Column(String, index=True)
    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete")
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True, unique=False)
    description = Column(String, index=True)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete")

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")