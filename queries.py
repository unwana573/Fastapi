select_data_from_users_query = "select * from tasks;"

add_task_query = """
    INSERT INTO tasks (user_id, description, status)
    VALUES (:id, :description, :status)
    RETURNING id, description , status
    """


select_user_query = """
        SELECT * FROM tasks 
        WHERE id = :id AND user_id = :user_id 
    """

update_query = """
        UPDATE tasks
        SET description = :description, status = :status
        WHERE id = :id AND user_id = :user_id 
        RETURNING id, description, status, user_id
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

