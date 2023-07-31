from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models import core as models

from models import schemas
from uuid import UUID, uuid4


def get_menus(db: Session):
    menus = db.query(models.Menu).all()
    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
    return menus

def get_menu(db: Session, menu_id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if menu:
        # Calculate the submenus_count and dishes_count
        submenus_count = len(menu.submenus)
        dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

        # Update the menu object with the calculated counts
        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

    return menu



def create_menu_V2(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    # Calculate and set submenus_count
    db_menu.submenus_count = len(menu.submenus) if menu.submenus else 0

    # Calculate and set dishes_count
    dishes_count = 0
    if menu.submenus:
        for submenu in menu.submenus:
            dishes_count += len(submenu.dishes) if submenu.dishes else 0
    db_menu.dishes_count = dishes_count

    db.commit()
    db.refresh(db_menu)
    return db_menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(
        id=uuid4(),
        title=menu.title,
        description=menu.description,
        submenus_count=0,
        dishes_count=0
    )
    db.add(db_menu)
    db.commit()
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