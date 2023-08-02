
# Restaurant Menu System

This project implements a system for managing menus, submenus, and dishes for a restaurant. It allows creating, updating, and querying menus, submenus, and dishes, while maintaining the required dependencies and constraints.

## TECHNOLOGIES

- Python 3.11.4
- FastAPI
- Postgres
- SQLAlchemy
- Uvicorn

## Entities

The project involves three main entities:

1. **Menu**: Represents the main menu of the restaurant.
2. **Submenu**: Represents a subsection of a menu, containing dishes.
3. **Dish**: Represents a dish available in the restaurant.

## Dependencies and Constraints

- A menu can have multiple submenus associated with it.
- A submenu can contain multiple dishes.
- A dish must be associated with a submenu, not directly with a menu.
- A dish cannot be present in more than one submenu.
- A submenu cannot belong to more than one menu.
- When a menu is deleted, all associated submenus and dishes should be deleted as well.
- When a submenu is deleted, all associated dishes should be deleted.

## Functionality

- The prices of dishes are rounded to two decimal places.
- When listing menus, the count of submenus and dishes in each menu is displayed.
- When listing submenus, the count of dishes in each submenu is displayed.

## Test Scenario

- The database should be empty at the start of the test scenario.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python packages and dependencies using pip-tools:

   ```bash
   pip install pip-tools
   pip-compile
   pip-sync

3. Set up the PostgreSQL database by modifying the SQLALCHEMY_DATABASE_URL in your environment configuration or directly in the code.

3. Start the application `uvicorn main:app --reload`