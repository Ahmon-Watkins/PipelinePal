from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask_app.models.user import User
from flask import flash

class Contact:
    DB = 'pipelinepal_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.notes = data['notes']
        self.last_sentiment = data['last_sentiment']
        self.product_of_interest = data['product_of_interest']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.tasks = None
        #self.comments=None
#Create
    @classmethod
    def create_contact(cls, data):
        query = """
                    INSERT INTO contacts (user_id, name, email, phone_number, notes, last_sentiment, product_of_interest) 
                    VALUES ( %(user_id)s, %(name)s,  %(email)s, %(phone_number)s, %(notes)s, %(last_sentiment)s, %(product_of_interest)s);
        
        """
        # data is a dictionary that will be passed into the save method from server.py
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_contact(data):
        is_valid = True  # We assume this is true
        
        if len(data['name']) < 5:
            flash("First and last name required.")
            is_valid = False
        if len(data['email']) < 2:
            flash("Email is required.")
            is_valid = False
        if len(data['notes']) < 50:
            flash("You must take better notes than that, you would be mad if you missed a sales because you forgot a detail.")
            is_valid = False
        if not data['last_sentiment']:
            flash("Sentiment is required.")
            is_valid = False
        if len(data['product_of_interest']) < 5:
            flash("Product of interest required.")
            is_valid = False

        
        return is_valid
# #READ
#             #This is not a normal one to many route this will select all and is good for posting to a wall.
    @classmethod
    def get_all_contacts_with_creator(cls):
            # Get all tweets, and their one associated User that created it
            query = "SELECT * FROM contacts JOIN users ON contacts.user_id = users.id;"
            results = connectToMySQL(cls.DB).query_db(query)
            all_contacts = []
            for row in results:
                # Create a Tweet class instance from the information from each db row
                one_contact = cls(row)
                # Prepare to make a User class instance, looking at the class in models/user.py
                one_contacts_author_info = {
                    # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                    "id": row['users.id'], 
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                }
                # Create the User class instance that's in the user.py model file
                author = User(one_contacts_author_info)
                # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
                one_contact.creator = author
                # Append the Tweet containing the associated User to your list of tweets
                all_contacts.append(one_contact)
            return all_contacts
    @classmethod
    def get_contact_by_id_with_creator(cls, contact_id):
        query = """
            SELECT * FROM contacts 
            JOIN users ON contacts.user_id = users.id 
            WHERE contacts.id = %(contact_id)s;
        """
        data = {"contact_id": contact_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        if result:
            contact_data = result[0]
            creator_data = {
                "id": contact_data['users.id'],
                "first_name": contact_data['first_name'],
                "last_name": contact_data['last_name'],
                "email": contact_data['email'],
                "password": contact_data['password'],
                "created_at": contact_data['created_at'],
                "updated_at": contact_data['updated_at']
            }
            creator = User(creator_data)
            
            contact = cls(contact_data)  # Create a contact instance
            contact.creator = creator  # Associate the creator User instance with the contact
            return contact
        else:
            return None
    @classmethod
    def get_contacts_by_user_id(cls, user_id):
        query = """
            SELECT * FROM contacts
            WHERE user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        contacts = []
        for contact_data in result:
            contact = cls(contact_data)
            contacts.append(contact)
        
        return contacts

#update
    @classmethod
    def edit_contact(cls, data):
        query = """
            UPDATE contacts
            SET 
                name = %(name)s,
                email = %(email)s,
                phone_number = %(phone_number)s,
                notes = %(notes)s,
                last_sentiment = %(last_sentiment)s,
                product_of_interest = %(product_of_interest)s
            WHERE id = %(id)s;
        """
        
        return connectToMySQL(cls.DB).query_db(query, data)
#delete
    @classmethod
    def delete_contact(cls, contact_id):
        query = "DELETE FROM contacts WHERE id = %(contact_id)s;"
        data = {"contact_id": contact_id}
        return connectToMySQL(cls.DB).query_db(query, data)

