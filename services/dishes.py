from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from models import core as models

from models import schemas

from services import menus as menu_service

from uuid import UUID


def get_dishes(db: Session, submenu_id: UUID):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()

def get_dish_2(db: Session, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id,
        models.Dish.id == dish_id
    ).first()

def get_dish(db: Session, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
    return db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id,
        models.Dish.id == dish_id
    ).first()

# CREATE DISH


def create_dish(db: Session, dish: schemas.DishCreate, menu_id: str, submenu_id: str):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu is None:
        return None

    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if db_submenu is None:
        return None

    db_dish = models.Dish(title=dish.title, description=dish.description, price=dish.price)
    db_dish.submenu = db_submenu
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    
    # Convert the price to a formatted string with two decimal places
    dish_response = schemas.Dish(
        id=db_dish.id,
        title=db_dish.title,
        description=db_dish.description,
        price="{:.2f}".format(db_dish.price)
    )
    
    return dish_response










# --------------





def create_dish_2(db: Session, dish: schemas.DishCreate, submenu_id: int):
    # Check if the Dish title already exists in any of the Submenus of the Menu
    existing_dish = (
        db.query(models.Dish)
        .join(models.Submenu)
        #.filter(models.Dish.title == dish.title, models.Submenu.id != submenu_id)
        .filter(models.Submenu.id != submenu_id)
        .first()
    )
    if existing_dish:
        raise HTTPException(status_code=400, detail="Dish title must be unique within the Menu")

    db_dish = models.Dish(title=dish.title, description=dish.description, price=round(dish.price, 2))
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status_code=404, detail="Submenu not found")

    db_submenu.dishes.append(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_id: UUID, dish_update: schemas.DishUpdate):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Check if the Dish is linked to a Submenu
    if db_dish.submenu_id is None:
        raise HTTPException(status_code=400, detail="Dish cannot be linked directly to a Menu")

    for key, value in dish_update.dict(exclude_unset=True).items():
        setattr(db_dish, key, value)

    # Check if the Dish is already linked to another Submenu
    if 'submenu_id' in dish_update and dish_update.submenu_id != db_dish.submenu_id:
        existing_dish = db.query(models.Dish).filter(models.Dish.submenu_id == dish_update.submenu_id).first()
        if existing_dish:
            raise HTTPException(status_code=400, detail="Dish already exists in another Submenu")

    db.commit()
    db.refresh(db_dish)
    return db_dish



def delete_dish(db: Session, dish_id: int):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if db_dish:
        db.delete(db_dish)
        db.commit()    
        return True
    
    return False