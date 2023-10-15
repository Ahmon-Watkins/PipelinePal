from flask_app import app


from flask import render_template, request, redirect, flash, session


from flask_app.models.contact import Contact
from flask_app.models.user import  User
from flask_app.models.task import Task
#Create
@app.route('/new/contact')
def new_contact():

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    return render_template('new_contact.html', user=user )

@app.route('/create/contact', methods=["POST"])
def create_contact():
    if 'user_id' not in session:
        flash("Please log in to create_contact", 'contact_post_error')
        return redirect('/')
    print("Session user_id:", session["user_id"])
    data = {
        "user_id": session["user_id"],
        "name": request.form["name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "notes": request.form["notes"],
        "last_sentiment": request.form["last_sentiment"],
        "product_of_interest": request.form["product_of_interest"],

    }

    if not Contact.validate_contact(data):
        return redirect("/new/contact")
    
    Contact.create_contact(data)
    flash("Contact created", 'contact_creation_success')
    print('working')
    print(data)
    
    return redirect("/new/contact")
#read
@app.route('/show/<int:contact_id>', methods=['GET'])
def view_contact(contact_id):
    contact = Contact.get_contact_by_id_with_creator(contact_id)
    if not contact:
        flash("Contact not found.", 'view_contact_error')
        return redirect(f"/dashboard/{session['user_id']}")

    # Fetch the creator of the contact
    creator = contact.creator

    # Fetch the tasks for the contact
    tasks = Task.get_tasks_to_contact(contact_id)
    print("Tasks:", tasks)
    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    
    return render_template('show_contact.html', contact=contact, session_user=session, creator=creator, tasks=tasks, user=user)





#edit contact

@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    if 'user_id' not in session:
        flash("Please log in to edit a contact.", 'edit_contact_error')
        return redirect('/')

    user_id = session['user_id']
    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    contact = Contact.get_contact_by_id_with_creator(contact_id)
    if contact is None:
        flash("Contact not found.", 'edit_contact_error')
        return redirect('/dashboard')

    if contact.user_id != session['user_id']:
        flash("You can only edit your own contacts.", 'edit_contact_error')
        return redirect('/dashboard')

    if request.method == 'POST':
        data = {
            "id": contact_id,
            "user_id": session["user_id"],
            "name": request.form["name"],
            "email": request.form["email"],
            "phone_number": request.form["phone_number"],
            "last_sentiment": request.form["last_sentiment"],
            "product_of_interest": request.form["product_of_interest"],
            "notes": request.form["notes"]
        }

        if not contact.validate_contact(data):
            return redirect(f'/edit/{contact_id}')

        Contact.edit_contact(data)
        flash("Contact updated successfully.", 'edit_contact_success')
        return redirect(f"/show/{contact_id}")

    return render_template('edit_contact.html', user=user, contact=contact)

# Delete
@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    if 'user_id' not in session:
        flash("Please log in to delete a contact.", 'delete_contact_error')
        return redirect('/')

    contact = Contact.get_contact_by_id_with_creator(contact_id)
    if not contact:
        flash("Contact not found.", 'delete_contact_error')
        return redirect(f"/dashboard/{session['user_id']}")

    if contact.user_id != session['user_id']:
        flash("You can only delete your own contacts.", 'delete_contact_error')
        return redirect(f"/dashboard/{session['user_id']}")

    Contact.delete_contact(contact_id)
    flash("Contact deleted successfully.", 'delete_contact_success')
    return redirect(f"/dashboard/{session['user_id']}")

    
