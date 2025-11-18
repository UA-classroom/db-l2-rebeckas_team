import os
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

import db
from schemas import BusinessCreate, BusinessOut, BusinessUpdate
from schemas import UserCreate, UserUpdate, UserOut
from schemas import CategoryCreate, CategoryUpdate, CategoryOut
app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""

#-------------------------#
#----------GET------------#
#-------------------------#
@app.get("/businesses/", response_model=list[BusinessOut])
def list_businesses():
    """
    GET /businesses/
    Returns all businesses in the database.
    """
    con = get_connection()
    businesses = db.get_all_businesses(con)
    return businesses


@app.get("/businesses/{business_id}", response_model=BusinessOut)
def get_business(business_id: int):
    """
    GET /businesses/id
    Returns one business, or 404 if not found.
    """
    con = get_connection()
    business = db.get_business_by_id(con, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.get("/users/", response_model=list[UserOut])
def list_users():
    """
    GET /users/
    Returns all users in the database.
    """
    con = get_connection()
    users = db.get_all_users(con)
    return users

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """
    GET /users/id
    Returns one user, or 404 if not found.
    """
    con = get_connection()
    user = db.get_user_by_id(con, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/categories", response_model=list[CategoryOut])
def list_categories():
    con = get_connection()
    return db.get_all_categories(con)

@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int):
    con = get_connection()
    category = db.get_category_by_id(con, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#-------------------------#
#---------POST------------#
#-------------------------#

@app.post("/businesses/", status_code=201)
def create_business(business: BusinessCreate):
    """
    POST /businesses
    Creates a new business and returns its id.
    """
    con = get_connection()
    new_id = db.create_business(con, business)
    return {"business_id": new_id}

@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    """
    POST /users/
    Creates a new user and returns its id.
    """
    con = get_connection()
    new_id = db.create_user(con, user)
    return {"id": new_id}

@app.post("/categories", status_code=201)
def create_category(data: CategoryCreate):
    con = get_connection()
    new_id = db.create_category(con, data)
    return {"id": new_id}


#-------------------------#
#----------PUT------------#
#-------------------------#
@app.put("/businesses/{business_id}", response_model=BusinessOut)
def update_business(business_id: int, data: BusinessUpdate):
    """
    PUT /businesses/{business_id}
    Updates an existing business and returns the updated record.
    """
    con = get_connection()
    updated = db.update_business(con, business_id, data)

    if not updated:
        raise HTTPException(status_code=404, detail="Business not found")

    return updated

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate):
    """
    PUT /users/{user_id}
    Updates an existing user and returns the updated record.
    """
    con = get_connection()
    updated = db.update_user(con, user_id, data)
    
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated

@app.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdate):
    con = get_connection()
    updated = db.update_category(con, category_id, data)

    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated


#-------------------------#
#---------DELETE----------#
#-------------------------#
@app.delete("/businesses/{business_id}", status_code=204)
def delete_business(business_id: int):
    """
    DELETE /businesses/{business_id}
    Deletes an existing business.
    """
    con = get_connection()
    deleted = db.delete_business(con, business_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found")

    return None

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """
    DELETE /users/{user_id}
    Deletes an existing user.
    """
    con = get_connection()
    deleted = db.delete_user(con, user_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    
    return None

@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int):
    con = get_connection()
    deleted = db.delete_category(con, category_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    return None
