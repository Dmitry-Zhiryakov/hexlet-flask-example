import uuid
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.get('/users')
def get_users():
    result = users
    search = request.args.get('term', '')
    if search:
        result = [user for user in users if search in user]
    return render_template(
        'users/index.html',
        users=result,
        search=search
    )


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    if user:
        user['id'] = str(uuid.uuid4())
    with open('templates/users/data.json', 'w') as file:
        json.dump(user, file)
    return redirect('/users', 302)


@app.route('/users/new')
def users_new():
    return render_template(
        'users/new.html'
    )
