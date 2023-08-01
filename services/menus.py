from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models import core as models

from models import schemas
from uuid import UUID, uuid4
from fastapi.encoders import jsonable_encoder  # Import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import func
from typing import List, Dict


def get_menus(db: Session):
    return db.query(models.Menu).all()

def get_menu(db: Session, menu_id: str):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    # Calculate the count of submenus for the menu
    submenus_count = db.query(func.count(models.Submenu.id)).filter(models.Submenu.menu_id == menu_id).scalar()

    # Calculate the count of dishes for the menu
    dishes_count = db.query(func.count(models.Dish.id)).join(models.Submenu).filter(models.Submenu.menu_id == menu_id).scalar()

    # Assign the calculated counts to the menu object
    menu.submenus_count = submenus_count
    menu.dishes_count = dishes_count

    return menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(
        title=menu.title,
        description=menu.description,
    )

    
    db.add(db_menu)
    db.commit()

    # Refresh the database object to get the updated submenus_count
    db.refresh(db_menu)

    return db_menu


def update_menu(db: Session, menu_id: int, menu_update: schemas.MenuUpdate):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db_menu.title = menu_update.title
        db_menu.description = menu_update.description
        db.commit()
        db.refresh(db_menu)
        return db_menu
    return None


def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        # Return None when the menu is successfully deleted
        return True
    else:
        return False