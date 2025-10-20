import psycopg2
from psycopg2.errors import UniqueViolation
import re
try: 
    connection = psycopg2.connect(
        dbname="todo",
        user="postgres",
        password="#Wgatap01",
        host="localhost",
        port=5432
    )
    print("Connection to database successful")
except:
    print("Connection to database failed")

cur = connection.cursor()

# def query():
#     create_users_query = """
#         CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             username  VARCHAR(100) ,
#             email VARCHAR(255) UNIQUE NOT NULL,
#             password varchar(255) NOT NULL 
#         );
#     """
#     cur.execute(create_users_query)
#     connection.commit()

#     create_task_query = """
#         CREATE TABLE IF NOT EXISTS tasks (
#             id SERIAL PRIMARY KEY,
#             description TEXT,
#             status VARCHAR(50) DEFAULT 'pending',
#             FOREIGN KEY(user_id) REFERENCES users(id)
#         );
#     """
#     cur.execute(create_task_query)
#     connection.commit()
#     # alter_query = """
#     #     ALTER TABLE tasks
#     #     ADD COLUMN status VARCHAR(50) DEFAULT 'pending';
#     # """
#     # cur.execute(alter_query)
#     # connection.commit()

# query()

# def user(): 
#     try: 
#         username = input("Enter your name: ") 
#         useremail = input("Enter your email: ") 
#         pwd = input("Enter password: ") 
#         insert_data_query = """INSERT INTO users(username, email, password)
#         VALUES(%s, %s, %s);"""
#         cur.execute(insert_data_query, (username, useremail, pwd)) 
#         connection.commit() 
#     except UniqueViolation: 
#         print("Welcome back") 
#         menu_handling(id)
#     return useremail         
# # email = user()
            
# def add_task(id):
#     task = input("Add task: ")
#     usd = int(id)
#     insert_add_query = """
#             INSERT INTO tasks(description, user_id)
#             VALUES(%s, %s);
#         """
#     cur.execute(insert_add_query, (task, usd))
#     connection.commit()

# def retrive_id(email):    
#     select_key = "SELECT id FROM users WHERE email = %s;"
#     cur.execute(select_key, (email,))
#     connection.commit()
#     result = cur.fetchone()
#     user_id = int(result[0])
#     if not result:
#         print("User not found. please register")
#     return user_id

# def view_task(id):
#     select_query = "SELECT description, status FROM tasks WHERE user_id = %s;"
#     cur.execute(select_query, (id,))
#     connection.commit()
#     result = cur.fetchall()
#     for task, status in result:
#         print(f"Task: {task} | Status: {status}")

# def delete_task(id):
#     cur.execute("""
#             SELECT t.id, t.description, t.status
#             FROM tasks t
#             JOIN users u ON t.user_id = u.id
#             WHERE u.id = %s;
#         """, (id,))
#     tasks = cur.fetchall()

#     if not tasks:
#         print("⚠️ No tasks found for this user.")
#         return
#     print("\n--- Your Tasks ---")
#     for t in tasks:
#         print(f"ID: {t[0]} | Task: {t[1]} | Status: {t[2]}")
#     task_id = input("\nEnter the ID of the task you want to delete: ")
#     confirm = input(f"Are you sure you want to delete task ID {task_id}? (y/n): ").lower()
#     if confirm != 'y':
#         print(" Deletion cancelled.")
#         return
#     cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
#     connection.commit()
#     print(f"✅ Task with ID {task_id} deleted successfully.")

# def mark_completed(id):
#     update_query = """
#         UPDATE tasks
#         SET status = 'completed' 
#         WHERE user_id = %s
#         """
#     cur.execute(update_query, (id,))
#     connection.commit
#     print("Task is marked as completed")

# def update_task(id):
#     new = input("Enter new task")
#     change = """
#         UPDATE tasks
#         SET description = %s, status = 'pending'
#         WHERE user_id = %s
#         """
#     cur.execute(change, (new, id))
#     connection.commit
#     print("Updated successfully")

# def menu_handling(id):
#     activity = True
#     while activity:
#         activity = input("""What would you like to do? 
#             1 - Add task
#             2 - View task
#             3 - Mark as completed
#             4 - Delete pending task
#             5 - Update task
#             6 - Quit
#             """)
#         activity = int(activity.strip())
#         if activity == 1:
#             add_task(id)
#         elif activity == 2:
#             view_task(id)
#         elif activity == 3:
#             mark_completed(id)
#         elif activity == 4:
#             delete_task(id)
#         elif activity == 5:
#             update_task(id)
#         elif activity == 6:
#             activity = False
#         else:
#             raise ValueError("Select only values from the menu")

# email = user()
# id = retrive_id(email) 
# menu_handling(id)


# connection.close()