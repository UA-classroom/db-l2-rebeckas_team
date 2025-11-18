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


#-------------------------#
#---------POST------------#
#-------------------------#
def create_business(con, data):
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
                    data.owner_id,
                    data.main_category_id,
                    data.name,
                    data.description,
                    data.street_name,
                    data.street_number,
                    data.city,
                    data.postal_code,
                ),
            )
            business_id = cursor.fetchone()["id"]
    return business_id

def create_user(con, data):
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
                    data.role,
                    data.firstname,
                    data.lastname,
                    data.username,
                    data.email,
                    data.phone_number
                )
            )
            return cursor.fetchone()["id"]



#-------------------------#
#----------PUT------------#
#-------------------------#
def update_business(con, business_id: int, data):
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
                    data.owner_id,
                    data.main_category_id,
                    data.name,
                    data.description,
                    data.street_name,
                    data.street_number,
                    data.city,
                    data.postal_code,
                    business_id,
                ),
            )
            updated = cursor.fetchone()
            return updated

def update_user(con, user_id: int, data):
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
                    data.role,
                    data.firstname,
                    data.lastname,
                    data.username,
                    data.email,
                    data.phone_number,
                    user_id,
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