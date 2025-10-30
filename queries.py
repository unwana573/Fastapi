select_task_query = """SELECT * FROM tasks
                        WHERE LOWER(status) = :status;
"""
select_empty_task_query = """SELECT * from tasks;
"""

add_task_query = """
    INSERT INTO tasks (user_id, task, status)
    VALUES (:user_id, :task, :status)
    RETURNING id, task , status
    """

select_user_query = """
        SELECT * FROM tasks 
        WHERE id = :id AND user_id = :user_id 
    """

update_query = """
        UPDATE tasks
        SET task = :task, status = :status
        WHERE id = :id AND user_id = :user_id 
        RETURNING id, task, status, user_id
    """

delete_query = """
            DELETE FROM tasks 
            WHERE id = :id AND user_id = :user_id  
        """

check_email_query= """
        SELECT * 
        FROM users 
        WHERE email = :email
    """

insert_user_query = """
        INSERT INTO users (first_name, last_name, email, password, role)
        VALUES (:first_name, :last_name, :email, :password, :role)
        RETURNING id, first_name, last_name, email, role
    """

blacklist_token_query = """
    INSERT INTO blacklist (tokens)
    VALUES (:tokens)
    """

get_token_query = """
    SELECT id FROM blacklist
    WHERE tokens = :tokens;
"""

check_admin_query = """
    SELECT id, first_name, last_name, email, role
    FROM users; """