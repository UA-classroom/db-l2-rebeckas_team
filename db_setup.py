import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")

def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )

def reset_database():
    """Drops all marketplace tables and recreates them."""
    
    connection = get_connection()
    cursor = connection.cursor()
    
    drop_sql = """
    DROP TABLE IF EXISTS reviews CASCADE;
    DROP TABLE IF EXISTS payments CASCADE;
    DROP TABLE IF EXISTS bookings CASCADE;
    DROP TABLE IF EXISTS service_categories CASCADE;
    DROP TABLE IF EXISTS services CASCADE;
    DROP TABLE IF EXISTS business_opening_hours CASCADE;
    DROP TABLE IF EXISTS business_images CASCADE;
    DROP TABLE IF EXISTS staffmembers CASCADE;
    DROP TABLE IF EXISTS businesses CASCADE;
    DROP TABLE IF EXISTS categories CASCADE;
    DROP TABLE IF EXISTS users CASCADE;
    """
    cursor.execute(drop_sql)
    connection.commit()
    cursor.close()
    connection.close()
    print("All tables dropped successfully.")
def create_tables():
    """
    Creates all necessary tables for the BokaDirekt booking system.    
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id BIGSERIAL PRIMARY KEY,
        role VARCHAR(20) NOT NULL CHECK (role IN ('customer', 'provider', 'admin')),
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(50) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone_number VARCHAR(25),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    
    # CATEGORIES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        description TEXT,
        parent_id BIGINT REFERENCES categories(id) ON DELETE SET NULL
    );
    """)
    
    # BUSINESSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id BIGSERIAL PRIMARY KEY,
        owner_id BIGINT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
        main_category_id BIGINT REFERENCES categories(id),
        name VARCHAR(30) NOT NULL,
        description TEXT,
        street_name VARCHAR(50),
        street_number VARCHAR(10),
        city VARCHAR(30),
        postal_code VARCHAR(10),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    
    # STAFF MEMBERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staffmembers (
        id BIGSERIAL PRIMARY KEY,
        business_id BIGINT REFERENCES businesses(id) ON DELETE SET NULL,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone_number VARCHAR(25),
        role VARCHAR(20),
        is_active BOOLEAN DEFAULT TRUE
    );
    """)
    
    # BUSINESS IMAGES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_images (
        id BIGSERIAL PRIMARY KEY,
        business_id BIGINT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
        image_url VARCHAR(255) NOT NULL,
        is_logo BOOLEAN DEFAULT FALSE,
        sort_order INT DEFAULT 0
    );
    """)
    
    # BUSINESS OPENING HOURS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_opening_hours (
        id BIGSERIAL PRIMARY KEY,
        business_id BIGINT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
        weekday SMALLINT NOT NULL CHECK (weekday BETWEEN 1 AND 7),
        open_time TIME NOT NULL,
        closing_time TIME NOT NULL
    );
    """)
    
    # SERVICES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id BIGSERIAL PRIMARY KEY,
        business_id BIGINT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
        name VARCHAR(30) NOT NULL,
        description TEXT,
        duration_minutes INT NOT NULL 
        CHECK (duration_minutes > 0),
        price NUMERIC(10, 2) NOT NULL 
        CHECK (price >= 0),
        is_active BOOLEAN DEFAULT TRUE
    );
    """)
    
    # SERVICE_CATEGORIES (Many-to-Many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service_categories (
        service_id BIGINT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
        category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
        PRIMARY KEY (service_id, category_id)
    );
    """)
    
    # SERVICE - STAFFMEMBERS (Many-to-Many)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff_service (
    staff_id BIGINT NOT NULL REFERENCES staffmembers(id) ON DELETE CASCADE,
    service_id BIGINT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    PRIMARY KEY (staff_id, service_id)
    );
    """)
    
    
    # BOOKINGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id BIGSERIAL PRIMARY KEY,
        customer_id BIGINT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
        business_id BIGINT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
        service_id BIGINT NOT NULL REFERENCES services(id) ON DELETE SET NULL,
        staff_id BIGINT REFERENCES staffmembers(id) ON DELETE SET NULL,
        starttime TIMESTAMP NOT NULL,
        endtime TIMESTAMP NOT NULL,
        status VARCHAR(20) NOT NULL 
        CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')),
        notes TEXT,
        created_at TIMESTAMP DEFAULT NOW(),
        CHECK (endtime > starttime)
    );
    """)
    
    # PAYMENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id BIGSERIAL PRIMARY KEY,
        booking_id BIGINT REFERENCES bookings(id) ON DELETE SET NULL,
        amount NUMERIC(10, 2) NOT NULL 
            CHECK (amount >= 0),
        payment_method VARCHAR(20) NOT NULL 
            CHECK (
                payment_method IN ('card', 'gift_card', 'swish', 'klarna', 'cash')
            ),
        status VARCHAR(20) NOT NULL DEFAULT 'pending' 
            CHECK (
                status IN ('pending', 'paid', 'refunded', 'failed')
            ),
        created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # REVIEWS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id BIGSERIAL PRIMARY KEY,
        booking_id BIGINT NOT NULL REFERENCES bookings(id) ON DELETE SET NULL,
        business_id BIGINT NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
        customer_id BIGINT NOT NULL REFERENCES users(id) ON DELETE SET NULL,
        rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
        title VARCHAR(50),
        comment TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    
    
    connection.commit()
    cursor.close()
    connection.close()
    


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    reset_database()
    create_tables()
    print("Tables created successfully.")
