import time
import datetime

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__) 

auth = HTTPBasicAuth()

def CurrentTimestamp(): 
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
    return st

def UserModified(): 
    time = CurrentTimestamp()
    user = auth.username()
    user_modifying = ('%s by %s' % (time, user)) 
    return user_modifying

@auth.get_password
def GetPassword(username): 
    if username == 'fakeuser': 
        return 'web'
    return None

@auth.error_handler
def Unauthorized(): 
    return make_response(jsonify({'error': 'Forbidden'}), 403) 

# Throw an error if user chooses an id that doesn't exist
@app.errorhandler(404)
def NotFoundError(error): 
    return make_response(jsonify({'error': 'Not found'}), 404) 


contacts = [ 
    { 
        'id': 1, 
        'first_name': 'Easter', 
        'last_name': 'Bunny', 
        'email': 'easter.bunny@alltheeggs.com', 
        'last_modified': 'None', 
    }, 
    { 
        'id': 2, 
        'first_name': 'Tooth', 
        'last_name': 'Fairy', 
        'email': 'tooth.fairy@newsmiles.com', 
        'last_modified': 'None', 
    }, 
    { 
        'id': 3, 
        'first_name': 'Santa', 
        'last_name': 'Claus', 
        'email': 'santa.claus@hohoho.com', 
        'last_modified': 'None', 
    } 
] 


# Helper function to return full URIs rather than just the contact id
def MakePublicContact(contact): 
    new_contact = {}
    for field in contact: 
        if field == 'id': 
            new_contact['uri'] = url_for('GetContact', contact_id=contact['id'], _external=True) 
        else: 
            new_contact[field] = contact[field]
    return new_contact

# List all contacts.
@app.route('/contacts', methods=['GET']) 
def GetAllContacts(): 
    return jsonify({'contacts': [MakePublicContact(contact) for contact in contacts]}) 

# Filter contacts by last name
@app.route('/contacts/<string:contact_last_name>', methods=['GET']) 
def SearchAllContacts(contact_last_name):
    contact = [contact for contact in contacts if contact['last_name'] == contact_last_name]
    if len(contact) == 0: 
        abort(404) 
    return jsonify({'contact': contact[0]}) 

# Add contact to dictionary. ***AUTH REQUIRED***
@app.route('/contacts', methods=['POST'])
@auth.login_required
def CreateContact(): 
    person_modifying = UserModified() 
    if not request.json or not 'first_name' or not 'email' in request.json:
        abort(400) 
    contact = { 
        'id': contacts[-1]['id'] + 1, 
        'first_name': request.json['first_name'], 
        'last_name': request.json.get('last_name', ''), 
        'email': request.json['email'], 
        'last_modified': person_modifying, 
    } 
    contacts.append(contact)
    return jsonify({'contact': contact}), 201

# Update entry. ***AUTH REQUIRED***
@app.route('/contacts/<int:contact_id>', methods=['PUT'])
@auth.login_required
def UpdateContact(contact_id): 
    person_modifying = UserModified()
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
def DeleteContact(contact_id): 
    contact = [contact for contact in contacts if contact['id'] == contact_id] 
    if len(contact) == 0: 
        abort(404) 
    contacts.remove(contact[0]) 
    return jsonify({'result': True}) 


if __name__ == '__main__': 
    app.run(debug=True) 