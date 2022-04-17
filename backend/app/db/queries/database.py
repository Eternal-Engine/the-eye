create_db_tables = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        email VARCHAR(50),
        salt VARCHAR,
        hashed_password VARCHAR,
        created_at TIMESTAMP,
        updated_at TIMESTAMP);
"""

drop_db_tables = """
    DROP TABLE IF EXISTS users;
"""
