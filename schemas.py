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

class BusinessCreate(BusinessBase):
    """
    Used when a client creates a new business (POST).
    Requires the owner_id and name fields, other fields are optional.
    """
    owner_id: int   # required on POST

class BusinessUpdate(BusinessBase):
    """
    Used for full replacement of a business (PUT).
    All required fields must be included and will overwrite existing values.
    """
    owner_id: int   # required on PUT

class BusinessOut(BusinessBase):
    """
    Returned to the client when reading business data (GET).
    Includes database-generated fields such as id and created_at.
    """
    id: int
    owner_id: int
    created_at: datetime
