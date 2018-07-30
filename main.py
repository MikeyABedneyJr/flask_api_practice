import time
import datetime

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)

auth = HTTPBasicAuth()

def current_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

def user_modified():
    time = current_timestamp()
    user = auth.username()
    user_modifying = ("%s by %s" % (time, user))
    return user_modifying

@auth.get_password
def get_password(username):
    if username == 'fakeuser':
        return 'web'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Forbidden'}), 403)

# Throw an error if user chooses an id that doesn't exist
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

contacts = [
    {
        'id': 1,
        'first_name': u'Easter',
        'last_name': u'Bunny',
        'email': u'easter.bunny@alltheeggs.com',
        'last_modified': 'None', 
    },
    {
        'id': 2,
        'first_name': u'Tooth',
        'last_name': u'Fairy',
        'email': u'tooth.fairy@newsmiles.com',
        'last_modified': 'None',
    },
    {
        'id': 3,
        'first_name': u'Santa',
        'last_name': u'Claus',
        'email': u'santa.claus@hohoho.com',
        'last_modified': 'None',
    }
]

# Helper function to return full URIs rather than just the contact id
def make_public_contact(contact):
    new_contact = {}
    for field in contact:
        if field == 'id':
            new_contact['uri'] = url_for('get_contact', contact_id=contact['id'], _external=True)
        else:
            new_contact[field] = contact[field]
    return new_contact

# List all contacts.
@app.route('/contacts', methods=['GET'])
def get_contacts():
    return jsonify({'contacts': [make_public_contact(contact) for contact in contacts]})

# Filter by specific contact id
@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact': contact[0]})

# Add contact to dictionary. ***AUTH REQUIRED***
@app.route('/contacts', methods=['POST'])
@auth.login_required
def create_contact():
    person_modifying = user_modified() 
    if not request.json or not 'first_name' or not 'email' in request.json:
        abort(400)
    contact = {
        'id': contacts[-1]['id'] + 1,
        'first_name': request.json['first_name'],
        'last_name': request.json.get('last_name', ""),
        'email': request.json['email'],
        'last_modified': person_modifying,
    }
    contacts.append(contact)
    return jsonify({'contact': contact}), 201

# Update entry. ***AUTH REQUIRED***
@app.route('/contacts/<int:contact_id>', methods=['PUT'])
@auth.login_required
def update_contact(contact_id):
    person_modifying = user_modified()
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'first_name' in request.json and type(request.json['first_name']) != unicode:
        abort(400)
    if 'last_name' in request.json and type(request.json['last_name']) != unicode:
        abort(400)
    if 'email' in request.json and type(request.json['email']) != unicode:
        abort(400)
    contact[0]['first_name'] = request.json.get('first_name', contact[0]['first_name'])
    contact[0]['last_name'] = request.json.get('last_name', contact[0]['last_name'])
    contact[0]['email'] = request.json.get('email', contact[0]['email'])
    contact[0]['last_modified'] = request.json.get('last_modified', person_modifying)
    return jsonify({'contact': contact[0]})

# Delete entry. ***AUTH REQUIRED***
@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
@auth.login_required
def delete_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    contacts.remove(contact[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
