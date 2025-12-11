from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""


# -------------------------#
# ----------GET------------#
# -------------------------#
def get_all_businesses(con):
    """
    Return a list of all businesses with both IDs and readable names.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    businesses.id,
                    businesses.owner_id,
                    businesses.main_category_id,
                    businesses.name,
                    businesses.description,
                    businesses.street_name,
                    businesses.street_number,
                    businesses.city,
                    businesses.postal_code,
                    businesses.created_at,
                    users.firstname || ' ' || users.lastname AS owner_name,
                    categories.name AS main_category_name
                FROM businesses
                JOIN users ON users.id = businesses.owner_id
                LEFT JOIN categories ON categories.id = businesses.main_category_id
                ORDER BY businesses.name;
            """)
            businesses = cursor.fetchall()
    return businesses


def get_business_by_id(con, business_id: int):
    """
    Return ONE business by id with owner_name and main_category_name. NONE if it dosent exist
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    businesses.id,
                    businesses.owner_id,
                    businesses.main_category_id,
                    businesses.name,
                    businesses.description,
                    businesses.street_name,
                    businesses.street_number,
                    businesses.city,
                    businesses.postal_code,
                    businesses.created_at,
                    users.firstname || ' ' || users.lastname AS owner_name,
                    categories.name AS main_category_name
                FROM businesses
                JOIN users ON users.id = businesses.owner_id
                LEFT JOIN categories ON categories.id = businesses.main_category_id
                WHERE businesses.id = %s;
            """, (business_id,))
            business = cursor.fetchone()
    return business


def get_all_users(con):
    """
    Return a list of all users
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users;")
            return cursor.fetchall()


def get_user_by_id(con, user_id: int):
    """
    Return ONE user by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            return cursor.fetchone()


def get_all_categories(con):
    """
    Returns all categories in the database.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories;")
            return cursor.fetchall()


def get_category_by_id(con, category_id: int):
    """
    Returns one category by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories WHERE id = %s;", (category_id,))
            return cursor.fetchone()


def get_all_staffmembers(con):
    """
    Returns all staff members in the database, including their business names.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    staffmembers.id,
                    staffmembers.business_id,
                    staffmembers.name,
                    staffmembers.email,
                    staffmembers.phone_number,
                    staffmembers.role,
                    staffmembers.is_active,
                    businesses.name AS business_name
                FROM staffmembers
                JOIN businesses ON businesses.id = staffmembers.business_id
                ORDER BY staffmembers.name;
            """)
            return cursor.fetchall()


def get_staffmember_by_id(con, staff_id: int):
    """
    Returns one staff member by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    staffmembers.id,
                    staffmembers.business_id,
                    staffmembers.name,
                    staffmembers.email,
                    staffmembers.phone_number,
                    staffmembers.role,
                    staffmembers.is_active,
                    businesses.name AS business_name
                FROM staffmembers
                JOIN businesses ON businesses.id = staffmembers.business_id
                WHERE staffmembers.id = %s;
            """, (staff_id,))
            return cursor.fetchone()


def get_staffmembers_by_business(con, business_id: int):
    """
    Get all the staff in one business
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM staffmembers WHERE business_id = %s;", (business_id,)
            )
            return cursor.fetchall()


def get_all_business_images(con):
    """
    Returns all business images in the database.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM business_images;")
            return cursor.fetchall()


def get_images_by_business(con, business_id: int):
    """
    Get ALL images for ONE business
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM business_images WHERE business_id = %s ORDER BY sort_order;",
                (business_id,),
            )
            return cursor.fetchall()


def get_business_image(con, image_id: int):
    """
    Returns one business image by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM business_images WHERE id = %s;", (image_id,))
            return cursor.fetchone()


def get_opening_hours_for_business(con, business_id: int):
    """
    Get opening-hours for ONE business
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM business_opening_hours
                WHERE business_id = %s
                ORDER BY weekday;
                """,
                (business_id,),
            )
            return cursor.fetchall()


def get_services_by_business(con, business_id: int):
    """
    Get ALL services for ONE business
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    services.id,
                    services.business_id,
                    services.name,
                    services.description,
                    services.duration_minutes,
                    services.price,
                    services.is_active,
                    businesses.name AS business_name
                FROM services
                JOIN businesses ON businesses.id = services.business_id
                WHERE services.business_id = %s;
                """, (business_id,),)
            services = cursor.fetchall()

    # Attach category names (list) to each service
    for service in services:
        service["categories"] = get_categories_for_service(con, service["id"])
    return services


def get_service(con, service_id: int):
    """
    Returns one service by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM services WHERE id = %s;
            """,
                (service_id,),
            )
            return cursor.fetchone()


def get_categories_for_service(con, service_id: int):
    """
    Returns all categories linked to a specific service.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT categories.*
                FROM categories
                JOIN service_categories ON categories.id = service_categories.category_id
                WHERE service_categories.service_id = %s;
                """,
                (service_id,),
            )
            return cursor.fetchall()


def get_services_for_category(con, category_id: int):
    """
    Returns all services linked to a specific category.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT services.*,
                    businesses.name AS business_name
                FROM services
                JOIN service_categories ON services.id = service_categories.service_id
                JOIN businesses ON businesses.id = services.business_id
                WHERE service_categories.category_id = %s;
                """,
                (category_id,),
            )
            return cursor.fetchall()


def get_services_by_business_and_category(con, business_id: int, category_id: int):
    """
    Returns all services for a business within a specific category.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT services.*,
                    businesses.name AS business_name
                FROM services
                JOIN service_categories ON services.id = service_categories.service_id
                JOIN businesses ON businesses.id = services.business_id
                WHERE services.business_id = %s
                    AND service_categories.category_id = %s;
                """,
                (business_id, category_id),
            )
            return cursor.fetchall()


def get_categories_for_business(con, business_id: int):
    """
    Returns all categories associated with a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT DISTINCT categories.*
                FROM categories
                JOIN service_categories ON categories.id = service_categories.category_id
                JOIN services ON service_categories.service_id = services.id
                WHERE services.business_id = %s;
                """,
                (business_id,),
            )
            return cursor.fetchall()


def get_services_by_categories(con, category_ids: list[int]):
    """
    Returns all services that belong to any of the given category IDs.
    """
    placeholders = ",".join(["%s"] * len(category_ids))  # e.g. %s,%s,%s

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                f"""
                SELECT DISTINCT services.*,
                            businesses.name AS business_name
                FROM services
                JOIN service_categories ON services.id = service_categories.service_id
                JOIN businesses ON businesses.id = services.business_id
                WHERE service_categories.category_id IN ({placeholders});
                """,
                category_ids,
            )
            return cursor.fetchall()


def get_booking(con, booking_id: int):
    """
    Returns one booking by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                WHERE bookings.id = %s;
            """, (booking_id,))
            return cursor.fetchone()


def get_bookings(con):
    """
    Returns all bookings in the database.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                ORDER BY bookings.starttime;
            """)
            return cursor.fetchall()


def get_bookings_by_customer(con, customer_id: int):
    """
    Returns all bookings for a specific customer.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                WHERE bookings.customer_id = %s
                ORDER BY bookings.starttime;
                """,
                (customer_id,),
            )
            return cursor.fetchall()


def get_bookings_by_business(con, business_id: int):
    """
    Returns all bookings for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                WHERE bookings.business_id = %s
                ORDER BY bookings.starttime;
                """,
                (business_id,),
            )
            return cursor.fetchall()


def get_bookings_by_staff(con, staff_id: int):
    """
    Returns all bookings assigned to a specific staff member.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                WHERE bookings.staff_id = %s
                ORDER BY bookings.starttime;
                """,
                (staff_id,),
            )
            return cursor.fetchall()


def get_bookings_by_service(con, service_id: int):
    """
    Returns all bookings for a specific service.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    bookings.*,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name,
                    staffmembers.name AS staff_name
                FROM bookings
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                LEFT JOIN staffmembers ON staffmembers.id = bookings.staff_id
                WHERE bookings.service_id = %s
                ORDER BY bookings.starttime;
                """,
                (service_id,),
            )
            return cursor.fetchall()


def get_all_payments(con):
    """
    Returns all payments in the database.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    payments.*,
                    bookings.starttime AS booking_starttime,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name
                FROM payments
                JOIN bookings ON bookings.id = payments.booking_id
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id;
            """)
            return cursor.fetchall()


def get_payment(con, payment_id: int):
    """
    Returns one payment by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    payments.*,
                    bookings.starttime AS booking_starttime,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name
                FROM payments
                JOIN bookings ON bookings.id = payments.booking_id
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                WHERE payments.id = %s;
            """, (payment_id,))
            return cursor.fetchone()


def get_payments_by_booking(con, booking_id: int):
    """
    Returns all payments for a specific booking.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    payments.*,
                    bookings.starttime AS booking_starttime,
                    users.firstname || ' ' || users.lastname AS customer_name,
                    businesses.name AS business_name,
                    services.name AS service_name
                FROM payments
                JOIN bookings ON bookings.id = payments.booking_id
                JOIN users ON users.id = bookings.customer_id
                JOIN businesses ON businesses.id = bookings.business_id
                JOIN services ON services.id = bookings.service_id
                WHERE payments.booking_id = %s;
            """, (booking_id,)
            )
            return cursor.fetchall()


def get_total_revenue_for_business(con, business_id: int):
    """
    Returns the total paid revenue for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT COALESCE(SUM(payments.amount), 0) AS total_revenue
                FROM payments
                JOIN bookings ON payments.booking_id = bookings.id
                WHERE bookings.business_id = %s
                    AND payments.status = 'paid';
                """,
                (business_id,),
            )
            return cursor.fetchone()


def get_unpaid_bookings(con):
    """
    Returns all bookings that have no associated paid payment.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT bookings.*
                FROM bookings
                LEFT JOIN payments ON payments.booking_id = bookings.id
                    AND payments.status = 'paid'
                WHERE payments.id IS NULL;
            """)
            return cursor.fetchall()


def get_unpaid_bookings_for_business(con, business_id: int):
    """
    Returns all unpaid bookings for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT bookings.*
                FROM bookings
                LEFT JOIN payments
                    ON payments.booking_id = bookings.id
                    AND payments.status = 'paid'
                WHERE bookings.business_id = %s
                    AND payments.id IS NULL;
                """,
                (business_id,),
            )
            return cursor.fetchall()


def get_review(con, review_id: int):
    """
    Returns one detailed review by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT reviews.*,
                    services.name AS service_name,
                    businesses.name AS business_name,
                    users.firstname || ' ' || users.lastname AS customer_name
                FROM reviews
                JOIN users ON users.id = reviews.customer_id
                JOIN businesses ON businesses.id = reviews.business_id
                JOIN bookings ON bookings.id = reviews.booking_id
                JOIN services ON services.id = bookings.service_id
                WHERE reviews.id = %s;
                """,
                (review_id,),
            )
            return cursor.fetchone()


def get_all_reviews(con):
    """
    Returns all reviews in the database.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT reviews.*,
                    services.name AS service_name,
                    businesses.name AS business_name,
                    users.firstname || ' ' || users.lastname AS customer_name
                FROM reviews
                JOIN users ON users.id = reviews.customer_id
                JOIN businesses ON businesses.id = reviews.business_id
                JOIN bookings ON bookings.id = reviews.booking_id
                JOIN services ON services.id = bookings.service_id
                ORDER BY reviews.created_at DESC;
                """)
            return cursor.fetchall()


def get_reviews_by_business(con, business_id: int):
    """
    Returns all reviews for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT reviews.*,
                    services.name AS service_name,
                    businesses.name AS business_name,
                    users.firstname || ' ' || users.lastname AS customer_name
                FROM reviews
                JOIN users ON users.id = reviews.customer_id
                JOIN businesses ON businesses.id = reviews.business_id
                JOIN bookings ON bookings.id = reviews.booking_id
                JOIN services ON services.id = bookings.service_id
                WHERE reviews.business_id = %s
                ORDER BY reviews.created_at DESC;
                """,
                (business_id,),
            )
            return cursor.fetchall()


def get_reviews_by_customer(con, customer_id: int):
    """
    Returns all reviews written by a specific customer.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT reviews.*,
                    services.name AS service_name,
                    businesses.name AS business_name,
                    users.firstname || ' ' || users.lastname AS customer_name
                FROM reviews
                JOIN users ON users.id = reviews.customer_id
                JOIN businesses ON businesses.id = reviews.business_id
                JOIN bookings ON bookings.id = reviews.booking_id
                JOIN services ON services.id = bookings.service_id
                WHERE reviews.customer_id = %s
                ORDER BY reviews.created_at DESC;
                """,
                (customer_id,),
            )
            return cursor.fetchall()


def get_average_rating_for_business(con, business_id: int):
    """
    Returns the average rating and total review count for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    COALESCE(AVG(rating), 0) AS average_rating,
                    COUNT(*) AS review_count
                FROM reviews
                WHERE business_id = %s;
                """,
                (business_id,),
            )
            return cursor.fetchone()


def get_top_rated_businesses(con, limit: int = 10):
    """
    Returns the top-rated businesses, limited by the given number.
    Only businesses with at least one review are included.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    businesses.id AS business_id,
                    businesses.name,
                    COALESCE(AVG(reviews.rating), 0) AS average_rating,
                    COUNT(reviews.id) AS review_count
                FROM businesses
                LEFT JOIN reviews ON reviews.business_id = businesses.id
                GROUP BY businesses.id
                HAVING COUNT(reviews.id) > 0
                ORDER BY average_rating DESC, review_count DESC
                LIMIT %s;
                """,
                (limit,),
            )
            return cursor.fetchall()


def get_total_bookings_for_business(con, business_id: int):
    """
    Returns the total number of bookings for a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS total_bookings
                FROM bookings
                WHERE business_id = %s;
                """,
                (business_id,),
            )
            return cursor.fetchone()

def get_services_for_staff(con, staff_id: int):
    """
    Returns all services assigned to a specific staff member.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT services.*
                FROM services
                JOIN staff_service ON staff_service.service_id = services.id
                WHERE staff_service.staff_id = %s;
            """, (staff_id,))
            return cursor.fetchall()

def get_staff_for_service(con, service_id: int):
    """
    Returns all staff members who are assigned to a specific service.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT staffmembers.*
                FROM staffmembers
                JOIN staff_service ON staff_service.staff_id = staffmembers.id
                WHERE staff_service.service_id = %s;
            """, (service_id,))
            return cursor.fetchall()
        
def get_business_categories(con, business_id: int):
    """
    Returns all category names associated with a specific business.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT DISTINCT categories.name
                FROM categories
                JOIN service_categories ON service_categories.category_id = categories.id
                JOIN services ON services.id = service_categories.service_id
                WHERE services.business_id = %s
                ORDER BY categories.name;
            """, (business_id,))
            return [row["name"] for row in cursor.fetchall()]

def get_businesses_by_category(con, category_id: int):
    """
    Returns all businesses associated with a specific category.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT DISTINCT businesses.*
                FROM businesses
                JOIN services ON services.business_id = businesses.id
                JOIN service_categories ON service_categories.service_id = services.id
                WHERE service_categories.category_id = %s
                ORDER BY businesses.name;
            """, (category_id,))
            return cursor.fetchall()



# -------------------------#
# ---------POST------------#
# -------------------------#
def create_business(con, business):
    """
    Insert a new business into the database and return its id.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO businesses (
                    owner_id,
                    main_category_id,
                    name,
                    description,
                    street_name,
                    street_number,
                    city,
                    postal_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    business.owner_id,
                    business.main_category_id,
                    business.name,
                    business.description,
                    business.street_name,
                    business.street_number,
                    business.city,
                    business.postal_code,
                ),
            )
            business_id = cursor.fetchone()["id"]
    return business_id


def create_user(con, user):
    """
    Insert a new user into the database and return its id.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (
                    role, firstname, lastname, username, email, phone_number
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    user.role,
                    user.firstname,
                    user.lastname,
                    user.username,
                    user.email,
                    user.phone_number,
                ),
            )
            return cursor.fetchone()["id"]


def create_category(con, category):
    """
    Creates a new category and returns its id.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO categories (name, description, parent_id)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (category.name, category.description, category.parent_id),
            )
            return cursor.fetchone()["id"]


def create_staffmember(con, staff_member):
    """
    Creates a new staff member and returns its id.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO staffmembers (
                    business_id,
                    name,
                    email,
                    phone_number,
                    role,
                    is_active
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    staff_member.business_id,
                    staff_member.name,
                    staff_member.email,
                    staff_member.phone_number,
                    staff_member.role,
                    staff_member.is_active,
                ),
            )
            return cursor.fetchone()["id"]


def create_business_image(con, business_image):
    """
    Creates a new business image and returns its id.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO business_images (business_id, image_url, is_logo, sort_order)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    business_image.business_id,
                    business_image.image_url,
                    business_image.is_logo,
                    business_image.sort_order,
                ),
            )
            return cursor.fetchone()["id"]


def replace_opening_hours(con, business_id: int, hours_list):
    """
    Replaces all opening hours for a business with the provided list.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            # delete old hours
            cursor.execute(
                "DELETE FROM business_opening_hours WHERE business_id = %s;",
                (business_id,),
            )
            # insert new hours
            for entry in hours_list:
                cursor.execute(
                    """
                    INSERT INTO business_opening_hours (business_id, weekday, open_time, closing_time)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (business_id, entry.weekday, entry.open_time, entry.closing_time),
                )

            return True


def create_service(con, service: dict):
    """
    Creates a new service and returns the created service record.
    """

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO services (business_id, name, description, duration_minutes, price, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
            """,
                (
                    service["business_id"],
                    service["name"],
                    service.get("description"),
                    service["duration_minutes"],
                    service["price"],
                    service.get("is_active", True),
                ),
            )
            return cursor.fetchone()


def add_category_to_service(con, service_id: int, category_id: int):
    """
    Adds a category to a service. Returns the inserted row, or None if it already exists.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO service_categories (service_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING *;
            """,
                (service_id, category_id),
            )
            return cursor.fetchone()


def create_booking(con, booking: dict):
    """
    Creates a new booking and returns the created booking record.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO bookings (customer_id, business_id, service_id, staff_id, 
                                    starttime, endtime, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """,
                (
                    booking["customer_id"],
                    booking["business_id"],
                    booking["service_id"],
                    booking.get("staff_id"),
                    booking["starttime"],
                    booking["endtime"],
                    booking["status"],
                    booking.get("notes"),
                ),
            )
            return cursor.fetchone()


def create_payment(con, data):
    """
    Creates a new payment and returns the created payment record.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO payments (booking_id, amount, payment_method, status)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """,
                (data.booking_id, data.amount, data.payment_method, data.status),
            )
            return cursor.fetchone()


def create_review(con, review):
    """
    Creates a new review and returns the created review record.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reviews (
                    booking_id, business_id, customer_id, rating, title, comment
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
            """,
                (
                    review.booking_id,
                    review.business_id,
                    review.customer_id,
                    review.rating,
                    review.title,
                    review.comment,
                ),
            )
            return cursor.fetchone()

def add_service_to_staff(con, staff_id: int, service_id: int):
    """
    Assigns a service to a staff member. Returns the inserted row, or None if it already exists.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO staff_service (staff_id, service_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING *;
            """, (staff_id, service_id))
            return cur.fetchone()


# -------------------------#
# ----------PUT------------#
# -------------------------#
def update_business(con, business_id: int, business):
    """
    Update an existing business based on business_id.
    The updated business is returned as a dictionary
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE businesses
                SET owner_id = %s,
                    main_category_id = %s,
                    name = %s,
                    description = %s,
                    street_name = %s,
                    street_number = %s,
                    city = %s,
                    postal_code = %s
                WHERE id = %s
                RETURNING *;
                """,
                (
                    business.owner_id,
                    business.main_category_id,
                    business.name,
                    business.description,
                    business.street_name,
                    business.street_number,
                    business.city,
                    business.postal_code,
                    business_id,
                ),
            )
            updated = cursor.fetchone()
            return updated


def update_user(con, user_id: int, user):
    """
    Update an existing user based on user_id.
    The updated user is returned as a dictionary
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE users
                SET role = %s,
                    firstname = %s,
                    lastname = %s,
                    username = %s,
                    email = %s,
                    phone_number = %s
                WHERE id = %s
                RETURNING *;
                """,
                (
                    user.role,
                    user.firstname,
                    user.lastname,
                    user.username,
                    user.email,
                    user.phone_number,
                    user_id,
                ),
            )
            return cursor.fetchone()


def update_category(con, category_id: int, category):
    """
    Updates a category and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE categories
                SET name = %s,
                    description = %s,
                    parent_id = %s
                WHERE id = %s
                RETURNING *;
                """,
                (category.name, category.description, category.parent_id, category_id),
            )
            return cursor.fetchone()


def update_staffmember(con, staff_id: int, staff_member):
    """
    Updates a staff member and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE staffmembers
                SET business_id = %s,
                    name = %s,
                    email = %s,
                    phone_number = %s,
                    role = %s,
                    is_active = %s
                WHERE id = %s
                RETURNING *;
                """,
                (
                    staff_member.business_id,
                    staff_member.name,
                    staff_member.email,
                    staff_member.phone_number,
                    staff_member.role,
                    staff_member.is_active,
                    staff_id,
                ),
            )
            return cursor.fetchone()


def update_service(con, service_id: int, service: dict):
    """
    Updates a service and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE services
                SET business_id = %s, name = %s, description = %s,
                    duration_minutes = %s, price = %s, is_active = %s
                WHERE id = %s
                RETURNING *;
            """,
                (
                    service["business_id"],
                    service["name"],
                    service.get("description"),
                    service["duration_minutes"],
                    service["price"],
                    service.get("is_active", True),
                    service_id,
                ),
            )
            return cursor.fetchone()


def update_booking(con, booking_id: int, booking: dict):
    """
    Updates a booking and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE bookings
                SET customer_id=%s, business_id=%s, service_id=%s,
                    staff_id=%s, starttime=%s, endtime=%s, 
                    status=%s, notes=%s
                WHERE id=%s
                RETURNING *;
            """,
                (
                    booking["customer_id"],
                    booking["business_id"],
                    booking["service_id"],
                    booking.get("staff_id"),
                    booking["starttime"],
                    booking["endtime"],
                    booking["status"],
                    booking.get("notes"),
                    booking_id,
                ),
            )
            return cursor.fetchone()


def update_review(con, review_id: int, review):
    """
    Updates a review and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE reviews
                SET booking_id=%s, business_id=%s, customer_id=%s,
                    rating=%s, title=%s, comment=%s
                WHERE id=%s
                RETURNING *;
            """,
                (
                    review.booking_id,
                    review.business_id,
                    review.customer_id,
                    review.rating,
                    review.title,
                    review.comment,
                    review_id,
                ),
            )
            return cursor.fetchone()


# -------------------------#
# ----------PATCH----------#
# -------------------------#


def update_booking_status(con, booking_id: int, status: str):
    """
    Updates the status of a booking and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE bookings
                SET status = %s
                WHERE id = %s
                RETURNING *;
            """,
                (status, booking_id),
            )
            return cursor.fetchone()


def update_payment_status(con, payment_id: int, status: str):
    """
    Updates the status of a payment and returns the updated record, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE payments
                SET status = %s
                WHERE id = %s
                RETURNING *;
            """,
                (status, payment_id),
            )
            return cursor.fetchone()


# -------------------------#
# ---------DELETE----------#
# -------------------------#
def delete_business(con, business_id: int):
    """
    Deletes an existing business based on business_id.
    Returns the deleted business_id if the deletion was successful.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM businesses WHERE id = %s RETURNING id;", (business_id,)
            )
            deleted = cursor.fetchone()
            return deleted


def delete_user(con, user_id: int):
    """
    Deletes an existing user based on user_id.
    Returns the deleted user_id if the deletion was successful.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
            return cursor.fetchone()


def delete_category(con, category_id: int):
    """
    Deletes a category and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM categories WHERE id = %s RETURNING id;", (category_id,)
            )
            return cursor.fetchone()


def delete_staffmember(con, staff_id: int):
    """
    Deletes a staff member and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM staffmembers WHERE id = %s RETURNING id;", (staff_id,)
            )
            return cursor.fetchone()


def delete_business_image(con, image_id: int):
    """
    Deletes a business image and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM business_images WHERE id = %s RETURNING id;", (image_id,)
            )
            return cursor.fetchone()


def delete_service(con, service_id: int):
    """
    Deletes a service and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM services WHERE id = %s RETURNING id;
            """,
                (service_id,),
            )
            return cursor.fetchone()


def remove_category_from_service(con, service_id: int, category_id: int):
    """
    Removes a category from a service and returns the service_id, or None if not found.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM service_categories
                WHERE service_id = %s AND category_id = %s
                RETURNING service_id;
            """,
                (service_id, category_id),
            )
            return cursor.fetchone()


def delete_booking(con, booking_id: int):
    """
    Deletes a booking and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM bookings WHERE id = %s RETURNING id;", (booking_id,)
            )
            return cursor.fetchone()


def delete_payment(con, payment_id: int):
    """
    Deletes a payment and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM payments WHERE id = %s RETURNING id;", (payment_id,)
            )
            return cursor.fetchone()


def delete_review(con, review_id: int):
    """
    Deletes a review and returns the deleted id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM reviews WHERE id = %s RETURNING id;", (review_id,)
            )
            return cursor.fetchone()
        
def remove_service_from_staff(con, staff_id: int, service_id: int):
    """
    Removes a service assignment from a staff member and returns the staff_id, or None if not found.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                DELETE FROM staff_service
                WHERE staff_id = %s AND service_id = %s
                RETURNING staff_id;
            """, (staff_id, service_id))
            return cur.fetchone()
