
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy import func  # Add this import

from models import core as models

from models import schemas
from uuid import UUID


def get_submenus(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        return None

    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()

    for db_submenu in submenus:
        db_submenu.dishes_count = db.query(models.Dish).filter(models.Dish.submenu_id == db_submenu.id).count()

    return submenus


def get_submenu(db: Session, submenu_id: int):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if not db_submenu:
        return None

    # Calculate the count of dishes for the submenu using a subquery
    db_submenu.dishes_count = db.query(func.count(models.Dish.id)).filter(models.Dish.submenu_id == submenu_id).scalar()

    return db_submenu

def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: UUID):
    # Check if the Menu exists
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    # Check if the Submenu with the same title already exists in the specified Menu
    existing_submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, models.Submenu.title == submenu.title).first()
    if existing_submenu:
        raise HTTPException(status_code=400, detail="Submenu with the same title already exists in the Menu")

    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_submenus(db: Session, menu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()



def update_submenu(db: Session, submenu_id: UUID, submenu_update: schemas.SubmenuUpdate):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status_code=404, detail="Submenu not found")
    
    # Check if the Submenu with the same title already exists in a different Menu
    if submenu_update.title:
        existing_submenu = db.query(models.Submenu).filter(
            models.Submenu.id != submenu_id, models.Submenu.title == submenu_update.title
        ).first()
        if existing_submenu:
            raise HTTPException(status_code=400, detail="Submenu with the same title already exists in another Menu")

    for key, value in submenu_update.dict(exclude_unset=True).items():
        setattr(db_submenu, key, value)

    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if db_submenu:
        db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).delete()
        db.delete(db_submenu)
        db.commit()

        return True
    
    return False





