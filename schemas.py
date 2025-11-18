# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#-----------------#
#-----BUSINESS----#
#-----------------#
class BusinessBase(BaseModel):
    """
    Shared fields used by both creation and update operations for business.
    """
    main_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None


#I put owner_id only in the POST/PUT models because it is not a 
# core attribute of the business — it is a foreign key that 
# #is only relevant when creating or updating a business and does not
# #effect the identity of the business.
class BusinessCreate(BusinessBase):
    """
    Used when a client creates a new business (POST).
    Requires the owner_id and name fields, other fields are optional.
    """
    owner_id: int

class BusinessUpdate(BusinessBase):
    """
    Used for full replacement of a business (PUT).
    All required fields must be included and will overwrite existing values.
    """
    owner_id: int

class BusinessOut(BusinessBase):
    """
    Returned to the client when reading business data (GET).
    Includes database-generated fields such as id and created_at.
    """
    id: int
    owner_id: int
    created_at: datetime


#-----------------#
#-------USERS-----#
#-----------------#

class UserBase(BaseModel):
    """
    Shared fields used by both creation and update operations for users.
    """
    role: str
    firstname: str
    lastname: str
    username: str
    email: str
    phone_number: Optional[str] = None
    
class UserCreate(UserBase):
    """
    Schema used when someone registers or when a provider/admin account is created.
    All fields except phone_number are required.
    """
    pass

class UserUpdate(UserBase):
    """
    Schema used for full replacement of a user (PUT).
    """
    pass

class UserOut(UserBase):
    """
    Schema returned when fetching user information from the API.
    Includes database-generated fields such as id and created_at.
    """
    id: int
    created_at: datetime