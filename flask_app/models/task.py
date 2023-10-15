from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.user import User


class Task:
    DB = 'pipelinepal_schema'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.contact_id = data['contact_id']
        self.task_type = data['task_type']
        self.due_date = data['due_date']
        self.task_notes = data['task_notes']
        self.contact_name = data.get('name', None)  # Add this line
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_task(cls, data):
        query = "INSERT INTO tasks (user_id, contact_id, task_type, due_date, task_notes) VALUES (%(user_id)s, %(contact_id)s, %(task_type)s, %(due_date)s, %(task_notes)s);"

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_tasks_for_contact(cls, contact_id):
        query = "SELECT * FROM tasks WHERE contact_id = %(contact_id)s;"
        data = {"contact_id": contact_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(result) for result in results]

    @classmethod
    def get_task_by_id(cls, task_id):
        query = "SELECT * FROM tasks WHERE id = %(task_id)s;"
        data = {'task_id': task_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            # Assuming it returns only one task with the given ID
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_tasks_to_contact(cls, contact_id):
        query = "SELECT tasks.* FROM contacts JOIN tasks ON contacts.id = tasks.contact_id WHERE tasks.contact_id = %(contact_id)s;"
        data = {"contact_id": contact_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            return [Task(result) for result in results]
        else:
            return []

    # @classmethod
    # def has_user_tasked(cls, user_id, contact_id):
    #     query = "SELECT * FROM tasks WHERE user_id = %(user_id)s AND contact_id = %(contact_id)s;"
    #     data = {'user_id': user_id, 'contact_id': contact_id}
    #     result = connectToMySQL(cls.DB).query_db(query, data)
    #     return len(result) > 0

    @classmethod
    def remove_task(cls, task_id):
        query = "DELETE FROM tasks WHERE id = %(task_id)s;"
        data = {'task_id': task_id}
        connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def edit_task(cls, task_id, data):
        query = """UPDATE tasks
                    SET user_id=%(user_id)s, 
                        contact_id=%(contact_id)s,
                        task_type=%(task_type)s,
                        due_date=%(due_date)s,
                        task_notes=%(task_notes)s
                    WHERE id = %(task_id)s;"""
        data['task_id'] = task_id
        connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_task_count(cls, contact_id):
        query = "SELECT COUNT(*) AS count FROM tasks WHERE contact_id = %(contact_id)s;"
        data = {'contact_id': contact_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result[0]['count'] if result else 0

    @classmethod
    def get_tasks_by_user_id(cls, user_id):
        query = """SELECT tasks.*, contacts.name 
                FROM tasks 
                JOIN contacts ON tasks.contact_id = contacts.id
                WHERE tasks.user_id = %(user_id)s
                ORDER BY tasks.due_date ASC;"""

        data = {'user_id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return [cls(result) for result in results]
