
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy import func  # Add this import

from models import core as models
from typing import List, Optional

from models import schemas
from uuid import UUID

from services import menus as menu_service



def get_submenus(db: Session, menu_id: UUID):

    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    for submenu in submenus:
        submenu.dishes_count = len(submenu.dishes)
    return submenus



def get_submenu(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dishes_count = len(db_submenu.dishes)  # Calculate dishes_count based on the dishes relationship
    

    # Create a dictionary representing the submenu response
    submenu_response = {
        "id": db_submenu.id,
        "title": db_submenu.title,
        "description": db_submenu.description,
        "dishes_count": dishes_count
    }



    return submenu_response
    

def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: UUID):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

def create_submenu_7(db: Session, submenu: schemas.SubmenuCreate, menu_id: UUID):
    db_submenu = models.Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id,
    )
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_submenus_2(db: Session, menu_id: UUID):
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

def delete_submenu_9(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if submenu_id is None:
        # Handle the case when submenu_id is None (null)
        # You can raise an HTTPException or return a response based on your application logic.
        raise HTTPException(status_code=400, detail="Invalid submenu_id. Please provide a valid UUID.")

    try:
        db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).delete()
        db.delete(db_submenu)
        db.commit()
        return {"message": "Submenu and associated dishes deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting submenu and dishes")


def delete_submenu(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if db_submenu:
        db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).delete()
        db.delete(db_submenu)
        db.commit()
        return True
    
    return False


def delete_submenu_3(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if submenu_id is None:
        # Handle the case when submenu_id is None (null)
        # You can raise an HTTPException or return a response based on your application logic.
        raise HTTPException(status_code=400, detail="Invalid submenu_id. Please provide a valid UUID.")

    try:
        db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).delete()
        db.delete(db_submenu)
        db.commit()
        return {"message": "Submenu and associated dishes deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting submenu and dishes")
