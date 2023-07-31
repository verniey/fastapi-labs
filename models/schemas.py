from typing import List, Optional
from pydantic import BaseModel, validator
from decimal import Decimal

from uuid import UUID
from pydantic import Field

class DishBase(BaseModel):
    title: str
    description: str

class DishCreate(DishBase):
    price: Decimal

class Dish(DishBase):
    id: UUID
    price: str  # Custom field to represent price as a formatted string

    class Config:
        orm_mode = True
        from_attributes = True










class DishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None



class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None

class SubmenuCreate(SubmenuBase):
    pass

class Submenu(SubmenuBase):
    id: UUID
    menu_id: UUID

    dishes_count: int = 0

class SubmenuUpdate(BaseModel):
    title: str
    description: str



class MenuBase(BaseModel):
    title: str
    description: str 


class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    pass



class Menu(MenuBase):
    id: UUID 
    submenus_count: int
    dishes_count: int
    class Config:
        orm_mode = True
        