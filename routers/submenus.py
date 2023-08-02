
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict
from typing import List, Optional

from models.database import get_db
from uuid import UUID


from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from services import submenus as submenu_service
from models import schemas
from services import menus as menu_service


submenu_router = APIRouter(prefix='/api/v1/menus')


@submenu_router.get("/{menu_id}/submenus", response_model=list[schemas.Submenu])
def get_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    return submenu_service.get_submenus(db, menu_id)


@submenu_router.get("/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: UUID, submenu_id: Optional[UUID]=None, db: Session = Depends(get_db)):
    if submenu_id:
        submenu = submenu_service.get_submenu(db, submenu_id)
        if submenu is None:
            raise HTTPException(status_code=404, detail="submenu not found")
        return submenu
                
    return {"message": "submenu not found"}


@submenu_router.post("/{menu_id}/submenus", response_model=schemas.Submenu, status_code=HTTP_201_CREATED)
def post_submenu(menu_id: UUID, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    submenu = submenu_service.create_submenu(db, submenu, menu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    
    return 


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def update_submenu(menu_id: UUID, submenu_id: UUID, submenu_update: schemas.SubmenuUpdate, db: Session = Depends(get_db)):
    return submenu_service.update_submenu(db, submenu_id=submenu_id, submenu_update=submenu_update)


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    deleted = submenu_service.delete_submenu(db, submenu_id)
    if deleted:
        # Return a success response when the submenu is successfully deleted
        return {"status": True, "message": "The submenu has been deleted"}

    else:
        # If the submenu is not found or cannot be deleted, raise an HTTPException with status code 404
        raise HTTPException(status_code=404, detail="Submenu not found")