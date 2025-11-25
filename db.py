import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

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


#-------------------------#
#----------GET------------#
#-------------------------#
def get_all_businesses(con):
    """
    Return a list of all businesses
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM businesses;")
            businesses = cursor.fetchall()
    return businesses

def get_business_by_id(con, business_id: int):
    """
    Return ONE business by id, or None if it doesn't exist.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM businesses WHERE id = %s;", (business_id,))
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
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories;")
            return cursor.fetchall()

def get_category_by_id(con, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories WHERE id = %s;", (category_id,))
            return cursor.fetchone()
        
def get_all_staffmembers(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM staffmembers;")
            return cursor.fetchall()

def get_staffmember_by_id(con, staff_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM staffmembers WHERE id = %s;", (staff_id,))
            return cursor.fetchone()

def get_staffmembers_by_business(con, business_id: int):
    """
    Get att the staff in one buissness    
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM staffmembers WHERE business_id = %s;",
                (business_id,)
            )
            return cursor.fetchall()

def get_all_business_images(con):
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
                (business_id,)
            )
            return cursor.fetchall()

def get_business_image(con, image_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM business_images WHERE id = %s;",
                (image_id,)
            )
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
                (business_id,)
            )
            return cursor.fetchall()
def get_services_by_business(con, business_id: int):
    """
    Get ALL services for ONE business
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM services WHERE business_id = %s;
            """, (business_id,))
            return cursor.fetchall()
        
def get_service(con, service_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM services WHERE id = %s;
            """, (service_id,))
            return cursor.fetchone()
        
def get_categories_for_service(con, service_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT c.*
                FROM categories c
                JOIN service_categories sc ON c.id = sc.category_id
                WHERE sc.service_id = %s;
                """,
                (service_id,)
            )
            return cur.fetchall()

def get_services_for_category(con, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT s.*
                FROM services s
                JOIN service_categories sc ON s.id = sc.service_id
                WHERE sc.category_id = %s;
                """,
                (category_id,)
            )
            return cur.fetchall()
        
def get_services_by_business_and_category(con, business_id: int, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT s.*
                FROM services s
                JOIN service_categories sc ON s.id = sc.service_id
                WHERE s.business_id = %s
                AND sc.category_id = %s;
            """, (business_id, category_id))
            return cursor.fetchall()
        
def get_categories_for_business(con, business_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT DISTINCT c.*
                FROM categories c
                JOIN service_categories sc ON c.id = sc.category_id
                JOIN services s ON sc.service_id = s.id
                WHERE s.business_id = %s;
            """, (business_id,))
            return cursor.fetchall()
        
def get_services_by_categories(con, category_ids: list[int]):
    placeholders = ",".join(["%s"] * len(category_ids))  # e.g. %s,%s,%s

    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"""
                SELECT DISTINCT s.*
                FROM services s
                JOIN service_categories sc ON s.id = sc.service_id
                WHERE sc.category_id IN ({placeholders});
            """, category_ids)
            return cursor.fetchall()

def get_booking(con, booking_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM bookings WHERE id = %s;", (booking_id,))
            return cursor.fetchone()

def get_bookings(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM bookings;")
            return cursor.fetchall()

def get_bookings_by_customer(con, customer_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM bookings
                WHERE customer_id = %s
                ORDER BY starttime;
            """, (customer_id,))
            return cursor.fetchall()
        
def get_bookings_by_business(con, business_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM bookings
                WHERE business_id = %s
                ORDER BY starttime;
            """, (business_id,))
            return cursor.fetchall()

def get_bookings_by_staff(con, staff_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM bookings
                WHERE staff_id = %s
                ORDER BY starttime;
            """, (staff_id,))
            return cursor.fetchall()

def get_bookings_by_service(con, service_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM bookings
                WHERE service_id = %s
                ORDER BY starttime;
            """, (service_id,))
            return cursor.fetchall()

def get_all_payments(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM payments;")
            return cursor.fetchall()

def get_payment(con, payment_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM payments WHERE id = %s;",
                (payment_id,)
            )
            return cursor.fetchone()
    
def get_payments_by_booking(con, booking_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM payments WHERE booking_id = %s;",
                (booking_id,)
            )
            return cursor.fetchall()

def get_total_revenue_for_business(con, business_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(p.amount), 0) AS total_revenue
                FROM payments p
                JOIN bookings b ON p.booking_id = b.id
                WHERE b.business_id = %s
                AND p.status = 'paid';
            """, (business_id,))
            return cursor.fetchone()

def get_unpaid_bookings(con):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT b.*
                FROM bookings b
                LEFT JOIN payments p ON p.booking_id = b.id
                    AND p.status = 'paid'
                WHERE p.id IS NULL;
            """)
            return cursor.fetchall()

def get_unpaid_bookings_for_business(con, business_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT b.*
                FROM bookings b
                LEFT JOIN payments p 
                    ON p.booking_id = b.id
                    AND p.status = 'paid'
                WHERE b.business_id = %s
                AND p.id IS NULL;
            """, (business_id,))
            return cursor.fetchall()

#-------------------------#
#---------POST------------#
#-------------------------#
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
                    user.phone_number
                )
            )
            return cursor.fetchone()["id"]

def create_category(con, category):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO categories (name, description, parent_id)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (
                    category.name, 
                    category.description, 
                    category.parent_id
                )
            )
            return cursor.fetchone()["id"]

def create_staffmember(con, staff_member):
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
                )
            )
            return cursor.fetchone()["id"]
        
def create_business_image(con, business_image):
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
                    business_image.sort_order
                )
            )
            return cursor.fetchone()["id"]

def replace_opening_hours(con, business_id: int, hours_list):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:

            # delete old hours
            cursor.execute(
                "DELETE FROM business_opening_hours WHERE business_id = %s;",
                (business_id,)
            )
            # insert new hours
            for entry in hours_list:
                cursor.execute(
                    """
                    INSERT INTO business_opening_hours (business_id, weekday, open_time, closing_time)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (business_id, entry.weekday, entry.open_time, entry.closing_time)
                )

            return True

def create_service(con, service: dict):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO services (business_id, name, description, duration_minutes, price, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                service["business_id"],
                service["name"],
                service.get("description"),
                service["duration_minutes"],
                service["price"],
                service.get("is_active", True)
            ))
            return cursor.fetchone()
        
def add_category_to_service(con, service_id: int, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO service_categories (service_id, category_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING *;
            """, (service_id, category_id))
            return cursor.fetchone()

def create_booking(con, booking: dict):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                INSERT INTO bookings (customer_id, business_id, service_id, staff_id, 
                                    starttime, endtime, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                booking["customer_id"],
                booking["business_id"],
                booking["service_id"],
                booking.get("staff_id"),
                booking["starttime"],
                booking["endtime"],
                booking["status"],
                booking.get("notes"),
            ))
            return cursor.fetchone()

def create_payment(con, data):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO payments (booking_id, amount, payment_method, status)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """,
                (data.booking_id, data.amount, data.payment_method, data.status)
            )
            return cursor.fetchone()



#-------------------------#
#----------PUT------------#
#-------------------------#
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
                )
            )
            return cursor.fetchone()

def update_category(con, category_id: int, category):
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
                (
                    category.name, 
                    category.description, 
                    category.parent_id, 
                    category_id
                )
            )
            return cursor.fetchone()

def update_staffmember(con, staff_id: int, staff_member):
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
                )
            )
            return cursor.fetchone()

def update_service(con, service_id: int, service: dict):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                UPDATE services
                SET business_id = %s, name = %s, description = %s,
                    duration_minutes = %s, price = %s, is_active = %s
                WHERE id = %s
                RETURNING *;
            """, (
                service["business_id"],
                service["name"],
                service.get("description"),
                service["duration_minutes"],
                service["price"],
                service.get("is_active", True),
                service_id
            ))
            return cursor.fetchone()

def update_booking(con, booking_id: int, booking: dict):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                UPDATE bookings
                SET customer_id=%s, business_id=%s, service_id=%s,
                    staff_id=%s, starttime=%s, endtime=%s, 
                    status=%s, notes=%s
                WHERE id=%s
                RETURNING *;
            """, (
                booking["customer_id"],
                booking["business_id"],
                booking["service_id"],
                booking.get("staff_id"),
                booking["starttime"],
                booking["endtime"],
                booking["status"],
                booking.get("notes"),
                booking_id
            ))
            return cursor.fetchone()

        

#-------------------------#
#----------PATCH----------#
#-------------------------#

def update_booking_status(con, booking_id: int, status: str):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                UPDATE bookings
                SET status = %s
                WHERE id = %s
                RETURNING *;
            """, (status, booking_id))
            return cursor.fetchone()

def update_payment_status(con, payment_id: int, status: str):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                UPDATE payments
                SET status = %s
                WHERE id = %s
                RETURNING *;
            """, (status, payment_id))
            return cursor.fetchone()


#-------------------------#
#---------DELETE----------#
#-------------------------#
def delete_business(con, business_id: int):
    """
    Deletes an existing business based on business_id.
    Returns the deleted business_id if the deletion was successful.
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM businesses WHERE id = %s RETURNING id;",
                (business_id,)
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
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id;",
                (user_id,)
            )
            return cursor.fetchone()

def delete_category(con, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM categories WHERE id = %s RETURNING id;",
                (category_id,)
            )
            return cursor.fetchone()

def delete_staffmember(con, staff_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM staffmembers WHERE id = %s RETURNING id;",
                (staff_id,)
            )
            return cursor.fetchone()

def delete_business_image(con, image_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM business_images WHERE id = %s RETURNING id;",
                (image_id,)
            )
            return cursor.fetchone()
        
def delete_service(con, service_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                DELETE FROM services WHERE id = %s RETURNING id;
            """, (service_id,))
            return cursor.fetchone()
        
def remove_category_from_service(con, service_id: int, category_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                DELETE FROM service_categories
                WHERE service_id = %s AND category_id = %s
                RETURNING service_id;
            """, (service_id, category_id))
            return cursor.fetchone()
        
def delete_booking(con, booking_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM bookings WHERE id = %s RETURNING id;",
                (booking_id,)
            )
            return cursor.fetchone()

def delete_payment(con, payment_id: int):
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM payments WHERE id = %s RETURNING id;",
                (payment_id,)
            )
            return cursor.fetchone()
        

