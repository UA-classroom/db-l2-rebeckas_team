import os
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

import db
from schemas import BusinessCreate, BusinessOut, BusinessUpdate
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
    GET /businesses
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

