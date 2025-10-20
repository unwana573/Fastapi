select_data_from_customers_query = "SELECT * FROM tasks WHERE user_id = :user_id;"

add_task_query = '''INSERT INTO tasks(tasks, status, user_id)
                    VALUES (:tasks, :status, :user_id)'''

update_task = '''UPDATE tasks
                SET tasks = :tasks
                WHERE id = :id'''

delete_task_query = '''DELETE FROM tasks 
                 WHERE id = VALUES :id;'''