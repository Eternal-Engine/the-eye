create_db_tables = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY NOT NULL,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        salt VARCHAR,
        hashed_password VARCHAR,
        is_publisher BOOL,
        is_verified BOOL,
        is_active BOOL,
        created_at TIMESTAMP,
        updated_at TIMESTAMP);

    CREATE TABLE IF NOT EXISTS journalists (
        id SERIAL PRIMARY KEY NOT NULL,
        first_name VARCHAR,
        last_name VARCHAR,
        bio VARCHAR,
        profile_picture VARCHAR,
        banner VARCHAR,
        address VARCHAR,
        postal_code VARCHAR,
        state VARCHAR,
        country VARCHAR,
        office_phone_number VARCHAR,
        mobile_phone_number VARCHAR,
        user_id INTEGER,
        FOREIGN KEY ("user_id") REFERENCES users("id"),
        created_at TIMESTAMP,
        updated_at TIMESTAMP);

    CREATE TABLE IF NOT EXISTS publishers (
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR,
        bio VARCHAR,
        profile_picture VARCHAR,
        banner VARCHAR,
        address VARCHAR,
        postal_code VARCHAR,
        state VARCHAR,
        country VARCHAR,
        office_phone_number VARCHAR,
        mobile_phone_number VARCHAR,
        user_id INTEGER,
        FOREIGN KEY ("user_id") REFERENCES users("id"),
        created_at TIMESTAMP,
        updated_at TIMESTAMP);
"""

drop_db_tables = """
    DROP TABLE IF EXISTS journalists;
    DROP TABLE IF EXISTS publishers;
    DROP TABLE IF EXISTS users CASCADE;
"""
