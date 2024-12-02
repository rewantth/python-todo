from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbms import (
    add_todo_item,
    mark_complete,
    get_complete,
    get_incomplete,
    create_user,
    authenticate_user,
    get_todo_by_id,
    update_todo_item,
)
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    incomplete = get_incomplete(session['user_id'])
    complete = get_complete(session['user_id'])
    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    if 'user_id' in session:
        add_todo_item(request.form['todoitem'], session['user_id'])
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/complete/<id>')
def complete(id):
    if 'user_id' in session:
        mark_complete(id)
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            create_user(username, password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists. Please try a different one.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user[0]
            flash('Login successful.')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch the todo item by its ID
    todo_item = get_todo_by_id(id, session['user_id'])

    if not todo_item:
        flash("Todo item not found.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_text = request.form['todoitem']
        update_todo_item(id, new_text)
        flash('Todo item updated successfully.')
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo_item)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
