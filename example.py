import uuid
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def read_file(file_path):
    with open(file_path, 'r') as input_file:
        file_data = input_file.read()
        return file_data


def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(json.dumps(data, indent=2))


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    data = read_file('templates/users/data.json')

    if request.method == 'GET':
        all_users= json.loads(data)['users']
        search_query = request.args.get('term', '')
        if search_query:
            found_users = [user for user in all_users if search_query in user["nickname"]]
            return render_template(
                'users/index.html',
                users=found_users,
                search_query=search_query
            )
        return render_template(
                'users/index.html',
                users=all_users,
                search_query=search_query
            )

    if request.method == 'POST':
        user = request.form.to_dict()
        user['id'] = str(uuid.uuid4())
        users = json.loads(data)
        users['users'].append(user)
        write_file('templates/users/data.json', users)
        return redirect('/users', 302)


@app.route('/users/new')
def users_new():
    return render_template(
        'users/new.html'
    )
