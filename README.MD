project repo:
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

1. Clone the repository: `git clone https://github.com/verniey/fastapi-labs`
2. Navigate to the project directory: `cd project`
3. Create vertual enviroment `python3 -m venv venv`  and activate a virtual environment `source venv/bin/activate`(recommended).
3. Install pip-tools: `pip install pip-tools`
4. Compile requirements: `pip-compile requirements.in`
5. Sync packages: `pip-sync`
------

## Database Configuration

Set up the PostgreSQL database by modifying the SQLALCHEMY_DATABASE_URL in your environment configuration or directly in the code.

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/task1" ```



## Getting Started

Start the application `uvicorn main:app --reload`

