# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


#-------------------------#
#----------GET------------#
#-------------------------#
class BusinessOut(BaseModel):
    """
    Used when we RETURN a business to the client (GET).
    Includes id and created_at.
    """
    id: int
    owner_id: int
    main_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    created_at: datetime

#-------------------------#
#---------POST------------#
#-------------------------#
class BusinessCreate(BaseModel):
    """
    Used when a client creates a business (POST).
    Mandatory to send owner_id(int) and name(string max 30 characters)
    Optional: main_category_id(int), description(string), street_name(sting),
    street_number(string), city(string), postal_code(string)
    """
    owner_id: int
    main_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None


#-------------------------#
#----------PUT------------#
#-------------------------#
class BusinessUpdate(BaseModel):
    """
    Used when we REPLACE a business (PUT).
    Mandatory to send key business_id(int), owner_id(int) and name(string max 30 characters)
    Optional: main_category_id(int), description(string), street_name(sting),
    street_number(string), city(string), postal_code(string)
    """
    owner_id: int
    main_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

