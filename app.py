import os
import psycopg2
from db_setup import get_connection
from fastapi import FastAPI, HTTPException

import db

from schemas import BusinessCreate, BusinessOut, BusinessUpdate
from schemas import UserCreate, UserUpdate, UserOut
from schemas import CategoryCreate, CategoryUpdate, CategoryOut
from schemas import StaffMemberCreate, StaffMemberUpdate, StaffMemberOut
from schemas import BusinessImageCreate, BusinessImageOut
from schemas import OpeningHoursUpdateRequest, OpeningHoursOut
from schemas import ServiceCreate, ServiceUpdate
from schemas import BookingCreate, BookingUpdate, BookingStatusUpdate
from schemas import PaymentCreate, PaymentOut, PaymentStatusUpdate
from schemas import ReviewCreate, ReviewUpdate, ReviewOut


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

@app.get("/staffmembers", response_model=list[StaffMemberOut])
def list_staffmembers():
    con = get_connection()
    staff = db.get_all_staffmembers(con)
    return staff

@app.get("/staffmembers/{staff_id}", response_model=StaffMemberOut)
def get_staffmember(staff_id: int):
    con = get_connection()
    staff = db.get_staffmember_by_id(con, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@app.get("/businesses/{business_id}/staffmembers", response_model=list[StaffMemberOut])
def list_staff_for_business(business_id: int):
    """
    Returns all staff members belonging to a specific business.
    """
    con = get_connection()
    staff = db.get_staffmembers_by_business(con, business_id)
    return staff

@app.get("/business-images", response_model=list[BusinessImageOut])
def list_all_images():
    con = get_connection()
    return db.get_all_business_images(con)

@app.get("/businesses/{business_id}/images", response_model=list[BusinessImageOut])
def list_images_for_business(business_id: int):
    con = get_connection()
    images = db.get_images_by_business(con, business_id)
    return images
@app.get("/business-images/{image_id}", response_model=BusinessImageOut)
def get_business_image(image_id: int):
    con = get_connection()
    img = db.get_business_image(con, image_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img

@app.get("/businesses/{business_id}/opening-hours", response_model=list[OpeningHoursOut])
def get_opening_hours_for_business_route(business_id: int):
    con = get_connection()
    return db.get_opening_hours_for_business(con, business_id)

@app.get("/services/search-filter")
def filter_services_by_categories(categories: str):
    con = get_connection()
    category_ids = [int(c) for c in categories.split(",")]
    services = db.get_services_by_categories(con, category_ids)
    return services
@app.get("/services/{service_id}")
def get_service_endpoint(service_id: int):
    con = get_connection()
    service = db.get_service(con, service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service
@app.get("/businesses/{business_id}/services")
def list_services_for_business(business_id: int):
    con = get_connection()
    services = db.get_services_by_business(con, business_id)
    return services

@app.get("/categories/{category_id}/services")
def list_services_for_category(category_id: int):
    con = get_connection()
    return db.get_services_for_category(con, category_id)

@app.get("/services/{service_id}/categories")
def list_categories_for_service(service_id: int):
    con = get_connection()
    return db.get_categories_for_service(con, service_id)

@app.get("/businesses/{business_id}/categories/{category_id}/services")
def list_services_in_category_for_business(business_id: int, category_id: int):
    con = get_connection()
    services = db.get_services_by_business_and_category(con, business_id, category_id)

    return services

@app.get("/businesses/{business_id}/categories")
def list_categories_for_business(business_id: int):
    con = get_connection()
    categories = db.get_categories_for_business(con, business_id)
    return categories

@app.get("/bookings/{booking_id}")
def get_booking_endpoint(booking_id: int):
    con = get_connection()
    booking = db.get_booking(con, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.get("/bookings")
def list_bookings():
    con = get_connection()
    return db.get_bookings(con)

@app.get("/customers/{customer_id}/bookings")
def list_bookings_for_customer(customer_id: int):
    con = get_connection()
    return db.get_bookings_by_customer(con, customer_id)

@app.get("/businesses/{business_id}/bookings")
def list_bookings_for_business(business_id: int):
    con = get_connection()
    return db.get_bookings_by_business(con, business_id)

@app.get("/staff/{staff_id}/bookings")
def list_bookings_for_staff(staff_id: int):
    con = get_connection()
    return db.get_bookings_by_staff(con, staff_id)

@app.get("/services/{service_id}/bookings")
def list_bookings_for_service(service_id: int):
    con = get_connection()
    return db.get_bookings_by_service(con, service_id)

@app.get("/payments", response_model=list[PaymentOut])
def list_payments():
    con = get_connection()
    return db.get_all_payments(con)

@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int):
    con = get_connection()
    payment = db.get_payment(con, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.get("/bookings/{booking_id}/payments", response_model=list[PaymentOut])
def list_payments_for_booking(booking_id: int):
    con = get_connection()
    return db.get_payments_by_booking(con, booking_id)

@app.get("/businesses/{business_id}/revenue")
def get_business_revenue(business_id: int):
    con = get_connection()
    result = db.get_total_revenue_for_business(con, business_id)
    return result

@app.get("/bookings/unpaid")
def list_unpaid_bookings():
    con = get_connection()
    return db.get_unpaid_bookings(con)

@app.get("/businesses/{business_id}/bookings/unpaid")
def list_unpaid_bookings_for_business(business_id: int):
    con = get_connection()
    return db.get_unpaid_bookings_for_business(con, business_id)

@app.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review_endpoint(review_id: int):
    con = get_connection()
    review = db.get_review(con, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@app.get("/reviews", response_model=list[ReviewOut])
def list_reviews():
    con = get_connection()
    return db.get_all_reviews(con)

@app.get("/businesses/{business_id}/reviews", response_model=list[ReviewOut])
def list_reviews_for_business(business_id: int):
    con = get_connection()
    return db.get_reviews_by_business(con, business_id)

@app.get("/customers/{customer_id}/reviews", response_model=list[ReviewOut])
def list_reviews_for_customer(customer_id: int):
    con = get_connection()
    return db.get_reviews_by_customer(con, customer_id)

@app.get("/businesses/{business_id}/rating")
def get_business_rating(business_id: int):
    con = get_connection()
    result = db.get_average_rating_for_business(con, business_id)
    return result

@app.get("/businesses/top-rated")
def top_rated_businesses(limit: int = 10):
    con = get_connection()
    return db.get_top_rated_businesses(con, limit)

@app.get("/businesses/{business_id}/bookings/count")
def total_bookings_for_business(business_id: int):
    con = get_connection()
    return db.get_total_bookings_for_business(con, business_id)

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

@app.post("/staffmembers", status_code=201)
def create_staffmember_route(data: StaffMemberCreate):
    con = get_connection()
    new_id = db.create_staffmember(con, data)
    return {"id": new_id}

@app.post("/business-images", status_code=201)
def create_business_image_route(data: BusinessImageCreate):
    con = get_connection()
    new_id = db.create_business_image(con, data)
    return {"id": new_id}

@app.post("/services/", response_model=dict)
def create_service_endpoint(service: ServiceCreate):
    con = get_connection()
    new_service = db.create_service(con, service.dict())
    return new_service

@app.post("/services/{service_id}/categories/{category_id}")
def add_category(service_id: int, category_id: int):
    con = get_connection()
    res = db.add_category_to_service(con, service_id, category_id)
    return {"status": "added" if res else "already exists"}

@app.post("/bookings/")
def create_booking_endpoint(data: BookingCreate):
    con = get_connection()
    booking = db.create_booking(con, data.dict())
    return booking

@app.post("/payments", response_model=PaymentOut, status_code=201)
def create_payment_route(data: PaymentCreate):
    con = get_connection()
    payment = db.create_payment(con, data)
    return payment

@app.post("/reviews", response_model=ReviewOut)
def create_review_endpoint(data: ReviewCreate):
    con = get_connection()
    review = db.create_review(con, data)
    return review


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

@app.put("/staffmembers/{staff_id}", response_model=StaffMemberOut)
def update_staffmember_route(staff_id: int, data: StaffMemberUpdate):
    con = get_connection()
    updated = db.update_staffmember(con, staff_id, data)

    if not updated:
        raise HTTPException(status_code=404, detail="Staff member not found")

    return updated

@app.put("/businesses/{business_id}/opening-hours")
def update_opening_hours_for_business(business_id: int, opening_hours: OpeningHoursUpdateRequest):
    con = get_connection()
    db.replace_opening_hours(con, business_id, opening_hours.hours)
    return {"message": "Opening hours updated successfully"}

@app.put("/services/{service_id}")
def update_service_endpoint(service_id: int, updated: ServiceUpdate):
    con = get_connection()
    updated_service = db.update_service(con, service_id, updated.dict())
    
    if not updated_service:
        raise HTTPException(status_code=404, detail="Service not found")

    return updated_service

@app.put("/bookings/{booking_id}")
def update_booking_endpoint(booking_id: int, data: BookingUpdate):
    con = get_connection()
    updated = db.update_booking(con, booking_id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated

@app.put("/reviews/{review_id}", response_model=ReviewOut)
def update_review_endpoint(review_id: int, data: ReviewUpdate):
    con = get_connection()
    updated = db.update_review(con, review_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated

#-------------------------#
#----------PATCH----------#
#-------------------------#
@app.patch("/bookings/{booking_id}/status")
def update_booking_status_endpoint(booking_id: int, data: BookingStatusUpdate):
    con = get_connection()

    updated = db.update_booking_status(con, booking_id, data.status)

    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")

    return updated

@app.patch("/payments/{payment_id}/status", response_model=PaymentOut)
def update_payment_status_route(payment_id: int, data: PaymentStatusUpdate):
    con = get_connection()
    updated = db.update_payment_status(con, payment_id, data.status)

    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")

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

@app.delete("/staffmembers/{staff_id}", status_code=204)
def delete_staffmember_route(staff_id: int):
    con = get_connection()
    deleted = db.delete_staffmember(con, staff_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Staff member not found")

    return None

@app.delete("/business-images/{image_id}", status_code=204)
def delete_business_image_route(image_id: int):
    con = get_connection()
    deleted = db.delete_business_image(con, image_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")

    return None

@app.delete("/services/{service_id}")
def delete_service_endpoint(service_id: int):
    con = get_connection()
    result = db.delete_service(con, service_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")

    return {"message": "Service deleted"}

@app.delete("/services/{service_id}/categories/{category_id}")
def remove_category(service_id: int, category_id: int):
    con = get_connection()
    res = db.remove_category_from_service(con, service_id, category_id)
    return {"status": "removed" if res else "not found"}

@app.delete("/bookings/{booking_id}")
def delete_booking_endpoint(booking_id: int):
    con = get_connection()
    deleted = db.delete_booking(con, booking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}

@app.delete("/payments/{payment_id}", status_code=204)
def delete_payment_route(payment_id: int):
    con = get_connection()
    deleted = db.delete_payment(con, payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return None

@app.delete("/reviews/{review_id}", status_code=204)
def delete_review_endpoint(review_id: int):
    con = get_connection()
    deleted = db.delete_review(con, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return None
