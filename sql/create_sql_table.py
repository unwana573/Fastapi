from database import get_db

create_users_query = """
    CREATE TABLE IF NOT EXISTS users (
        id bigint GENERATED ALWAYS AS IDENTITY,
        first_name  VARCHAR(100),
        last_name  VARCHAR(100),
        email VARCHAR(255) UNIQUE NOT NULL,
        password varchar(255) NOT NULL ,
        role VARCHAR(50) DEFAULT 'user'
    );
"""
        # id BIGSERIAL PRIMARY KEY,

create_task_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        description TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
"""

# alter_query = """
#     ALTER TABLE user
#     ADD COLUMN role VARCHAR(50) DEFAULT 'user';
# """

async def create_tables(db):
    await db.execute(query=create_users_query)
    # await db.execute(query=alter_query)
