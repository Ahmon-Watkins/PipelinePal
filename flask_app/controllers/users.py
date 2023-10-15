from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash
# import the class from friend.py


from flask_app.models.user import User
from flask_app.models.contact import Contact
from flask_app.models.task import Task
# from flask_app.models.friend import Friend



@app.route('/')
def index():
    return render_template('login_registration.html')
#Create new users

@app.route("/user/register", methods=["POST"])
def user_register():
    # Validation
    if not User.validate_user(request.form):
        # Redirect back to the registration form if validation fails
        return redirect('/')

    # Hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    # Prepare user data
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    # Create user and store user_id in session
    user_id = User.create(data)
    session['user_id'] = user_id

    # Redirect to the user profile page
    return redirect(f'/dashboard/{user_id}')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    user_id = user_in_db.id
    # never render on a post!!!

    return redirect(f"/dashboard/{user_id}")

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')

    all_the_contacts = Contact.get_all_contacts_with_creator()  # Fetch all contacts with their creators
    all_the_contacts.reverse()

    task_counts = {}  # Dictionary to store task counts for each contact

    for contact in all_the_contacts:
        task_counts[contact.id] = Task.get_task_count(contact.id)
    user_tasks = Task.get_tasks_by_user_id(user_id)

    for task in user_tasks:  # Assuming user_tasks is your list of Task objects
        print(task.contact_name)


    return render_template("dashboard.html", user=user, all_the_contacts=all_the_contacts, all_the_tasks=user_tasks)



