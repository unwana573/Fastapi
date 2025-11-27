from database import get_db

create_users_query = """
    CREATE TABLE IF NOT EXISTS users (
        id bigint GENERATED ALWAYS AS IDENTITY UNIQUE,
        first_name  VARCHAR(100),
        last_name  VARCHAR(100),
        email VARCHAR(255) UNIQUE NOT NULL,
        password varchar(255) NOT NULL,
        role VARCHAR(50) DEFAULT 'user'
    );
"""
        # id BIGSERIAL PRIMARY KEY,

create_task_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        description TEXT,
        user_id bigint, 
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
"""

create_token_query = """
    CREATE TABLE IF NOT EXISTS blacklist (
        id bigint GENERATED ALWAYS AS IDENTITY UNIQUE,
        token TEXT
    );
"""
alter_query = """
    CREATE TABLE IF NOT EXISTS token (
        id bigint GENERATED ALWAYS AS IDENTITY UNIQUE,
        token TEXT
    );
"""



async def create_tables(db):
    await db.execute(query=create_users_query)
    await db.execute(query=create_task_query)
    await db.execute(query=create_token_query)