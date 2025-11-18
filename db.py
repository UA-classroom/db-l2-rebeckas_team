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
