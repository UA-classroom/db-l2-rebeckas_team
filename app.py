import os
from datetime import datetime

import db
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas import (
    AvailableSlotsOut,
    BookingCreate,
    BookingOut,
    BookingStatusUpdate,
    BookingUpdate,
    BusinessCreate,
    BusinessDetail,
    BusinessImageCreate,
    BusinessImageOut,
    BusinessOut,
    BusinessUpdate,
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    OpeningHoursOut,
    OpeningHoursUpdateRequest,
    PaymentCreate,
    PaymentOut,
    PaymentStatusUpdate,
    ReviewCreate,
    ReviewOut,
    ReviewUpdate,
    ServiceCreate,
    ServiceDetail,
    ServiceUpdate,
    StaffMemberCreate,
    StaffMemberDetail,
    StaffMemberOut,
    StaffMemberUpdate,
    UserCreate,
    UserOut,
    UserUpdate,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- STATIC FILES: Image Hosting Setup ---
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

#-------------------------#
#----------GET------------#
#-------------------------#

@app.get("/businesses/", response_model=list[BusinessDetail], status_code=200)
def list_businesses():
    """
    GET /businesses/
    Returns all businesses in the database.
    """
    con = get_connection()
    return db.get_all_businesses(con)


@app.get("/businesses/top-rated", status_code=200)
def top_rated_businesses(limit: int = 10):
    """
    GET /businesses/top-rated
    Returns the top-rated businesses, limited by the 'limit' parameter.
    """
    con = get_connection()
    return db.get_top_rated_businesses(con, limit)


@app.get("/businesses/{business_id}", response_model=BusinessDetail, status_code=200)
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


@app.get("/users/", response_model=list[UserOut], status_code=200)
def list_users():
    """
    GET /users/
    Returns all users in the database.
    """
    con = get_connection()
    return db.get_all_users(con)


@app.get("/users/{user_id}", response_model=UserOut, status_code=200)
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


@app.get("/categories/", response_model=list[CategoryOut], status_code=200)
def list_categories():
    """
    GET /categories/
    Returns all categories in the database.
    """
    con = get_connection()
    return db.get_all_categories(con)

@app.get("/categories/tree")
def get_category_tree():
    """
    GET /categories/tree
    Returns the full category hierarchy as nested dictionaries.
    """
    con = get_connection()
    categories = db.get_all_categories(con)

    # Build {id: category_dict}
    nodes = {c["id"]: {**c, "children": []} for c in categories}

    roots = []

    for c in categories:
        if c["parent_id"]:
            parent = nodes.get(c["parent_id"])
            if parent:
                parent["children"].append(nodes[c["id"]])
        else:
            roots.append(nodes[c["id"]])

    return roots

@app.get("/categories/{category_id}", response_model=CategoryOut, status_code=200)
def get_category(category_id: int):
    """
    GET /categories/id
    Returns one category, or 404 if not found.
    """
    con = get_connection()
    category = db.get_category_by_id(con, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/staffmembers/", response_model=list[StaffMemberDetail], status_code=200)
def list_staffmembers():
    """
    GET /staffmembers/
    Returns all staff members in the database.
    """
    con = get_connection()
    return db.get_all_staffmembers(con)


@app.get("/staffmembers/{staff_id}", response_model=StaffMemberOut, status_code=200)
def get_staffmember(staff_id: int):
    """
    GET /staffmembers/id
    Returns one staff member, or 404 if not found.
    """
    con = get_connection()
    staff = db.get_staffmember_by_id(con, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


@app.get("/businesses/{business_id}/staffmembers", response_model=list[StaffMemberOut], status_code=200)
def list_staff_for_business(business_id: int):
    """
    Returns all staff members belonging to a specific business.
    """
    con = get_connection()
    return db.get_staffmembers_by_business(con, business_id)


@app.get("/business-images", response_model=list[BusinessImageOut], status_code=200)
def list_all_images():
    """
    GET /business-images
    Returns all business images in the database.
    """
    con = get_connection()
    return db.get_all_business_images(con)


@app.get("/businesses/{business_id}/images", response_model=list[BusinessImageOut], status_code=200)
def list_images_for_business(business_id: int):
    """
    GET /businesses/id/images
    Returns all images for a specific business.
    """
    con = get_connection()
    return db.get_images_by_business(con, business_id)


@app.get("/business-images/{image_id}", response_model=BusinessImageOut, status_code=200)
def get_business_image(image_id: int):
    """
    GET /business-images/id
    Returns one business image, or 404 if not found.
    """
    con = get_connection()
    image = db.get_business_image(con, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@app.get("/businesses/{business_id}/opening-hours", response_model=list[OpeningHoursOut], status_code=200)
def get_opening_hours_for_business_route(business_id: int):
    """
    GET /businesses/id/opening-hours
    Returns opening hours for a specific business.
    """
    con = get_connection()
    return db.get_opening_hours_for_business(con, business_id)


@app.get("/services/search-filter", status_code=200)
def filter_services_by_categories(categories: str):
    """
    GET /services/search-filter
    Returns services filtered by a comma-separated list of category IDs.
    """
    con = get_connection()
    ids = [int(c) for c in categories.split(",")]
    return db.get_services_by_categories(con, ids)


@app.get("/services/{service_id}", status_code=200)
def get_service_endpoint(service_id: int):
    """
    GET /services/id
    Returns one service, or 404 if not found.
    """
    con = get_connection()
    service = db.get_service(con, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@app.get("/businesses/{business_id}/services", response_model=list[ServiceDetail], status_code=200)
def list_services_for_business(business_id: int):
    """
    GET /businesses/id/services
    Returns all services belonging to a specific business.
    """
    con = get_connection()
    return db.get_services_by_business(con, business_id)


@app.get("/categories/{category_id}/services", status_code=200)
def list_services_for_category(category_id: int):
    """
    GET /categories/id/services
    Returns services for one category.
    """
    con = get_connection()
    return db.get_services_for_category(con, category_id)


@app.get("/services/{service_id}/categories", status_code=200)
def list_categories_for_service(service_id: int):
    """
    GET /services/id/categories
    Returns all categories linked to a service.
    """
    con = get_connection()
    return db.get_categories_for_service(con, service_id)


@app.get("/businesses/{business_id}/categories/{category_id}/services", status_code=200)
def list_services_in_category_for_business(business_id: int, category_id: int):
    """
    Returns all services for a business in a category.
    """
    con = get_connection()
    return db.get_services_by_business_and_category(con, business_id, category_id)


@app.get("/businesses/{business_id}/categories", status_code=200)
def list_categories_for_business(business_id: int):
    """
    Returns categories used by a business.
    """
    con = get_connection()
    return db.get_categories_for_business(con, business_id)


# ---------------- BOOKING ENDPOINTS ---------------- #

@app.get("/bookings/{booking_id}", response_model=BookingOut, status_code=200)
def get_booking_endpoint(booking_id: int):
    """
    Returns one booking.
    """
    con = get_connection()
    booking = db.get_booking(con, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.get("/bookings", response_model=list[BookingOut], status_code=200)
def list_bookings():
    """
    Returns all bookings.
    """
    con = get_connection()
    return db.get_bookings(con)


@app.get("/customers/{customer_id}/bookings", response_model=list[BookingOut], status_code=200)
def list_bookings_for_customer(customer_id: int):
    """
    Returns bookings for one customer.
    """
    con = get_connection()
    return db.get_bookings_by_customer(con, customer_id)


@app.get("/businesses/{business_id}/bookings", response_model=list[BookingOut], status_code=200)
def list_bookings_for_business(business_id: int):
    """
    Returns bookings for a business.
    """
    con = get_connection()
    return db.get_bookings_by_business(con, business_id)


@app.get("/staff/{staff_id}/bookings", response_model=list[BookingOut], status_code=200)
def list_bookings_for_staff(staff_id: int):
    """
    Returns bookings for a staff member.
    """
    con = get_connection()
    return db.get_bookings_by_staff(con, staff_id)


@app.get("/services/{service_id}/bookings", response_model=list[BookingOut], status_code=200)
def list_bookings_for_service(service_id: int):
    """
    Returns bookings for one service.
    """
    con = get_connection()
    return db.get_bookings_by_service(con, service_id)


@app.get("/bookings/unpaid", response_model=list[dict], status_code=200)
def list_unpaid_bookings():
    """
    Returns unpaid bookings.
    """
    con = get_connection()
    return db.get_unpaid_bookings(con)


@app.get("/businesses/{business_id}/bookings/unpaid", response_model=list[dict], status_code=200)
def list_unpaid_bookings_for_business(business_id: int):
    """
    Returns unpaid bookings for one business.
    """
    con = get_connection()
    return db.get_unpaid_bookings_for_business(con, business_id)


# ---------------- PAYMENTS ---------------- #

@app.get("/payments", response_model=list[PaymentOut], status_code=200)
def list_payments():
    """
    Returns all payments.
    """
    con = get_connection()
    return db.get_all_payments(con)


@app.get("/payments/{payment_id}", response_model=PaymentOut, status_code=200)
def get_payment(payment_id: int):
    """
    Returns one payment.
    """
    con = get_connection()
    payment = db.get_payment(con, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.get("/bookings/{booking_id}/payments", response_model=list[PaymentOut], status_code=200)
def list_payments_for_booking(booking_id: int):
    """
    Returns payments for one booking.
    """
    con = get_connection()
    return db.get_payments_by_booking(con, booking_id)


# ---------------- REVIEWS ---------------- #

@app.get("/reviews/{review_id}", response_model=ReviewOut, status_code=200)
def get_review_endpoint(review_id: int):
    """
    Returns one review.
    """
    con = get_connection()
    review = db.get_review(con, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.get("/reviews", response_model=list[ReviewOut], status_code=200)
def list_reviews():
    """
    Returns all reviews.
    """
    con = get_connection()
    return db.get_all_reviews(con)


@app.get("/businesses/{business_id}/reviews", response_model=list[ReviewOut], status_code=200)
def list_reviews_for_business(business_id: int):
    """
    Returns reviews for one business.
    """
    con = get_connection()
    return db.get_reviews_by_business(con, business_id)


@app.get("/customers/{customer_id}/reviews", response_model=list[ReviewOut], status_code=200)
def list_reviews_for_customer(customer_id: int):
    """
    Returns reviews by customer.
    """
    con = get_connection()
    return db.get_reviews_by_customer(con, customer_id)


@app.get("/businesses/{business_id}/rating", status_code=200)
def get_business_rating(business_id: int):
    """
    Returns rating and review count.
    """
    con = get_connection()
    return db.get_average_rating_for_business(con, business_id)


@app.get("/businesses/{business_id}/bookings/count", status_code=200)
def total_bookings_for_business(business_id: int):
    """
    Returns total booking count.
    """
    con = get_connection()
    return db.get_total_bookings_for_business(con, business_id)

@app.get("/businesses/{business_id}/services/{service_id}/available-slots", response_model=AvailableSlotsOut)
def get_available_slots(business_id: int, service_id: int, date: str):
    """
    GET /businesses/{id}/services/{id}/available-slots?date=YYYY-MM-DD
    Returns available booking time slots for the given date.
    """
    con = get_connection()

    # Convert weekday: Monday=1 ... Sunday=7
    weekday = datetime.strptime(date, "%Y-%m-%d").isoweekday()

    hours = db.get_business_hours_for_date(con, business_id, weekday)
    if not hours:
        raise HTTPException(status_code=404, detail="Business is closed on this day")

    service = db.get_service(con, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    duration = service["duration_minutes"]

    bookings = db.get_bookings_for_business_and_date(con, business_id, date)

    # Generate raw slots
    slots = db.generate_time_slots(
        hours["open_time"].strftime("%H:%M"),
        hours["closing_time"].strftime("%H:%M"),
        duration
    )

    # Filter out overlapping slots
    available = db.filter_overlapping_slots(slots, duration, bookings)

    return {
        "date": date,
        "service_duration": duration,
        "available_slots": available
    }


@app.get("/categories/{category_id}/children")
def get_category_children(category_id: int):
    """
    GET /categories/{category_id}/children
    Returns all direct child categories of a given category.
    """
    con = get_connection()
    categories = db.get_all_categories(con)
    return [category for category in categories if category["parent_id"] == category_id]

@app.get("/categories/{category_id}/parent")
def get_category_parent(category_id: int):
    """
    GET /categories/{category_id}/parent
    Returns the parent category of a given category.
    Returns null if the category has no parent.
    """
    con = get_connection()
    category = db.get_category_by_id(con, category_id)
    if not category or category["parent_id"] is None:
        return None

    return db.get_category_by_id(con, category["parent_id"])

@app.get("/customers/{customer_id}/bookings/upcoming", response_model=list[BookingOut])
def upcoming_bookings(customer_id: int):
    con = get_connection()
    bookings = db.get_bookings_by_customer(con, customer_id)
    now = datetime.now()
    return [b for b in bookings if b["starttime"] > now]

@app.get("/customers/{customer_id}/bookings/past", response_model=list[BookingOut])
def past_bookings(customer_id: int):
    con = get_connection()
    bookings = db.get_bookings_by_customer(con, customer_id)
    now = datetime.now()
    return [b for b in bookings if b["endtime"] < now]
#-------------------------#
#---------POST------------#
#-------------------------#

@app.post("/businesses/", status_code=201)
def create_business(business: BusinessCreate):
    """
    Creates a business.
    """
    con = get_connection()
    new_id = db.create_business(con, business)
    return {"business_id": new_id}


@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    """
    Creates a user.
    """
    con = get_connection()
    new_id = db.create_user(con, user)
    return {"id": new_id}


@app.post("/categories", status_code=201)
def create_category(data: CategoryCreate):
    """
    Creates a category.
    """
    con = get_connection()
    new_id = db.create_category(con, data)
    return {"id": new_id}


@app.post("/staffmembers", status_code=201)
def create_staffmember(data: StaffMemberCreate):
    """
    Creates a staff member.
    """
    con = get_connection()
    new_id = db.create_staffmember(con, data)
    return {"id": new_id}


@app.post("/business-images", status_code=201)
def create_business_image(data: BusinessImageCreate):
    """
    Creates a business image.
    """
    con = get_connection()
    new_id = db.create_business_image(con, data)
    return {"id": new_id}


@app.post("/services/", status_code=201)
def create_service_endpoint(service: ServiceCreate):
    """
    Creates a service.
    """
    con = get_connection()
    return db.create_service(con, service.dict())


@app.post("/services/{service_id}/categories/{category_id}", status_code=200)
def add_category(service_id: int, category_id: int):
    """
    Adds category to service.
    """
    con = get_connection()
    res = db.add_category_to_service(con, service_id, category_id)
    return {"status": "added" if res else "already exists"}


@app.post("/bookings/", response_model=BookingOut, status_code=201)
def create_booking_endpoint(data: BookingCreate):
    """
    Creates a booking.
    """
    con = get_connection()
    return db.create_booking(con, data.dict())


@app.post("/payments", response_model=PaymentOut, status_code=201)
def create_payment_route(data: PaymentCreate):
    """
    Creates a payment.
    """
    con = get_connection()
    return db.create_payment(con, data)


@app.post("/reviews", response_model=ReviewOut, status_code=201)
def create_review_endpoint(data: ReviewCreate):
    """
    Creates a review.
    """
    con = get_connection()
    return db.create_review(con, data)


@app.post("/staff/{staff_id}/services/{service_id}", status_code=200)
def assign_service_to_staff(staff_id: int, service_id: int):
    """
    Assigns service to staff.
    """
    con = get_connection()
    db.add_service_to_staff(con, staff_id, service_id)
    return {"status": "assigned"}

from fastapi import File, UploadFile


@app.post("/upload-image", status_code=201)
async def upload_business_image(file: UploadFile = File(...)):
    """
    Uploads an image file and stores it locally.
    Returns a URL that the frontend can use.
    """

    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Save file
    file_location = f"static/uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # Return public URL
    return {"image_url": f"/static/uploads/{file.filename}"}


#-------------------------#
#----------PUT------------#
#-------------------------#

@app.put("/businesses/{business_id}", response_model=BusinessOut, status_code=200)
def update_business(business_id: int, data: BusinessUpdate):
    """
    Updates a business.
    """
    con = get_connection()
    updated = db.update_business(con, business_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Business not found")
    return updated


@app.put("/users/{user_id}", response_model=UserOut, status_code=200)
def update_user(user_id: int, data: UserUpdate):
    """
    Updates a user.
    """
    con = get_connection()
    updated = db.update_user(con, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@app.put("/categories/{category_id}", response_model=CategoryOut, status_code=200)
def update_category(category_id: int, data: CategoryUpdate):
    """
    Updates a category.
    """
    con = get_connection()
    updated = db.update_category(con, category_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated


@app.put("/staffmembers/{staff_id}", response_model=StaffMemberOut, status_code=200)
def update_staffmember(staff_id: int, data: StaffMemberUpdate):
    """
    Updates a staff member.
    """
    con = get_connection()
    updated = db.update_staffmember(con, staff_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return updated


@app.put("/businesses/{business_id}/opening-hours", status_code=200)
def update_opening_hours_for_business(business_id: int, opening_hours: OpeningHoursUpdateRequest):
    """
    Replaces opening hours for a business.
    """
    con = get_connection()
    db.replace_opening_hours(con, business_id, opening_hours.hours)
    return {"message": "Opening hours updated successfully"}


@app.put("/services/{service_id}", status_code=200)
def update_service_endpoint(service_id: int, updated: ServiceUpdate):
    """
    Updates a service.
    """
    con = get_connection()
    new_data = db.update_service(con, service_id, updated.dict())
    if not new_data:
        raise HTTPException(status_code=404, detail="Service not found")
    return new_data


@app.put("/bookings/{booking_id}", response_model=BookingOut, status_code=200)
def update_booking_endpoint(booking_id: int, data: BookingUpdate):
    """
    Updates a booking.
    """
    con = get_connection()
    updated = db.update_booking(con, booking_id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated


@app.put("/reviews/{review_id}", response_model=ReviewOut, status_code=200)
def update_review_endpoint(review_id: int, data: ReviewUpdate):
    """
    Updates a review.
    """
    con = get_connection()
    updated = db.update_review(con, review_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated


#-------------------------#
#----------PATCH----------#
#-------------------------#

@app.patch("/bookings/{booking_id}/status", response_model=BookingOut, status_code=200)
def update_booking_status_endpoint(booking_id: int, data: BookingStatusUpdate):
    """
    Updates booking status.
    """
    con = get_connection()
    updated = db.update_booking_status(con, booking_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated


@app.patch("/payments/{payment_id}/status", response_model=PaymentOut, status_code=200)
def update_payment_status_route(payment_id: int, data: PaymentStatusUpdate):
    """
    Updates payment status.
    """
    con = get_connection()
    updated = db.update_payment_status(con, payment_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated

@app.patch("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    con = get_connection()
    updated = db.update_booking_status(con, booking_id, "cancelled")
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"status": "cancelled"}

@app.patch("/bookings/{booking_id}/reschedule")
def reschedule_booking(booking_id: int, start: datetime, end: datetime):
    con = get_connection()
    booking = db.get_booking(con, booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Overlap check can be added here

    updated = db.update_booking(con, booking_id, {
        **booking,
        "starttime": start,
        "endtime": end
    })

    return updated


#-------------------------#
#---------DELETE----------#
#-------------------------#

@app.delete("/businesses/{business_id}", status_code=204)
def delete_business(business_id: int):
    """
    Deletes a business.
    """
    con = get_connection()
    deleted = db.delete_business(con, business_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found")


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """
    Deletes a user.
    """
    con = get_connection()
    deleted = db.delete_user(con, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int):
    """
    Deletes a category.
    """
    con = get_connection()
    deleted = db.delete_category(con, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/staffmembers/{staff_id}", status_code=204)
def delete_staffmember(staff_id: int):
    """
    Deletes a staff member.
    """
    con = get_connection()
    deleted = db.delete_staffmember(con, staff_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Staff member not found")


@app.delete("/business-images/{image_id}", status_code=204)
def delete_business_image(image_id: int):
    """
    Deletes a business image.
    """
    con = get_connection()
    deleted = db.delete_business_image(con, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")


@app.delete("/services/{service_id}", status_code=204)
def delete_service_endpoint(service_id: int):
    """
    Deletes a service.
    """
    con = get_connection()
    deleted = db.delete_service(con, service_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/services/{service_id}/categories/{category_id}", status_code=200)
def remove_category(service_id: int, category_id: int):
    """
    Removes category from service.
    """
    con = get_connection()
    result = db.remove_category_from_service(con, service_id, category_id)
    return {"status": "removed" if result else "not found"}


@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking_endpoint(booking_id: int):
    """
    Deletes a booking.
    """
    con = get_connection()
    deleted = db.delete_booking(con, booking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")


@app.delete("/payments/{payment_id}", status_code=204)
def delete_payment_route(payment_id: int):
    """
    Deletes a payment.
    """
    con = get_connection()
    deleted = db.delete_payment(con, payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")


@app.delete("/reviews/{review_id}", status_code=204)
def delete_review_endpoint(review_id: int):
    """
    Deletes a review.
    """
    con = get_connection()
    deleted = db.delete_review(con, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")


@app.delete("/staff/{staff_id}/services/{service_id}", status_code=200)
def remove_service_from_staff(staff_id: int, service_id: int):
    """
    Removes service from staff.
    """
    con = get_connection()
    result = db.remove_service_from_staff(con, staff_id, service_id)
    return {"status": "removed" if result else "not found"}
