from flask_app import app

from flask_app.models.task import Task

from flask import render_template, request, redirect, flash, session


from flask_app.models.user import User  # Import the User model


@app.route('/add_task/<int:contact_id>', methods=['POST'])
def add_task(contact_id):
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to create task.", 'task_error')
        return redirect('/')

    data = {
        "user_id": session["user_id"],
        "contact_id": request.form["contact_id"],
        "task_type": request.form["task_type"],
        "due_date": request.form["due_date"],
        "task_notes": request.form["task_notes"]

    }

    Task.create_task(data)
    flash("You created a task on this contact.", 'task_success')
    print(data)
    return redirect(f"/show/{contact_id}")


@app.route('/remove_task/<int:task_id>', methods=['POST'])
def remove_task(task_id):
    print(f"Received task_id: {task_id}")  # Debugging line
    if 'user_id' not in session:
        flash("Please log in to remove your task.", 'remove_task_error')
        return redirect('/')

    task = Task.get_task_by_id(task_id)
    print(f"Task object: {task}")  # Debugging line
    if task is None:
        flash("Task not found.", 'remove_task_error')
        return redirect('/')
    
    contact_id = task.contact_id  # Get the contact_id associated with the task
    Task.remove_task(task_id)
    flash("Task completed successfully.", 'delete_task_success')

    return redirect(f'/show/{contact_id}')  # Redirect to the correct contact's profile


@app.route('/edit_task/<task_id>', methods= ['GET', 'POST'])
def edit_task(task_id):
    task = Task.get_task_by_id(task_id)
    return render_template("edit_task.html", task=task)

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.get_task_by_id(task_id)
    data = {
        'user_id': session['user_id'],
        'contact_id': request.form['contact_id'],
        'task_type': request.form['task_type'],
        'due_date': request.form['due_date'],
        'task_notes': request.form['task_notes']
    }
    contact_id = task.contact_id
    Task.edit_task(task_id, data)
    flash("Task updated successfully")
    return redirect(f'/show/{contact_id}')