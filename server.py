from flask import Flask, request, jsonify, render_template
from .api import UserMngr
from .api import ConsumerMngr
from .exceptions import PasswordMismatch
from .exceptions import UserDoesNotExist
from .exceptions import UsernameTaken
from .exceptions import InvalidSession

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user/register',methods=['POST'])
def register():
    username = request.form.get('username')
    print('username:',username)
    password = request.form.get('password')
    print('password:',password)
    response = {}
    if username and password:
        try:
            UserMngr.register(username,password)
            response['registered']=True

        except UsernameTaken as e:
            response['error'] = e.CODE
    else:
        response['error']='Please provide both username and password'
    return jsonify(response)

@app.route('/api/user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    response = {}
    if username and password:
        try:
            addr = request.remote_addr
            session = UserMngr.login(username,password,addr=addr)
            response['session_id']=session
        except PasswordMismatch as e:
            response['error'] = e.CODE

        except UserDoesNotExist as e:
            response['error'] = e.CODE
    else:
        response['error']='Please provide both username and password'

    return jsonify(response)

@app.route('/api/user/session_data', methods=['POST'])
def get_session_data():
    session_id = request.form.get('session')
    response = {}
    if session_id:
        try:
            session_data = UserMngr.session_data(session_id)
            response['data']=session_data
        except InvalidSession as e:
            response['error']=e.CODE
    else:
        response['error']='Please provide the session id'

    return jsonify(response)

@app.route('/api/consumer/request_registration',methods=['POST'])
def request_registration():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    response = {}
    if username and password and email: 
        try:
            ConsumerMngr.request_registration(username,password,email)
            response['registration_requested']=True

        except:
            response['error']='Error occured in registration request'
    return jsonify(response)

@app.route('/api/consumer/register', methods=['POST'])
def consumer_register():
    registration_id = request.form.get('registration_id')
    response = {}
    if registration_id:
        try:
            ConsumerMngr.register(registration_id)
            response['registered']=True

        except UsernameTaken as e:
            response['error'] = e.CODE
    else:
        response['error']='Please provide both username and password'
    return jsonify(response)

@app.route('/api/consumer/login',methods=['POST'])
def consumer_login():
    username = request.form.get('username')
    password = request.form.get('password')
    response = {}
    if username and password:
        try:
            addr = request.remote_addr
            session = ConsumerMngr.login(username,password,addr)
            response['session']=session
        except PasswordMismatch as e:
            response['error'] = e.CODE

        except UserDoesNotExist as e:
            response['error'] = e.CODE
    else:
        response['error'] = 'Please provide both username and password'

    return jsonify(response)

@app.route('/api/consumer/session_data',methods =['POST'])
def session_data():
    consumer_session = request.form.get('consumer_session')
    user_session = request.form.get('user_session')
    response = {}
    if consumer_session and user_session:
        if ConsumerMngr.logged_in(consumer_session):
            results = ConsumerMngr.get_user_session(user_session)
            response['response']=results
        else:
            response['error']='You are not logged in'
    else:
        response['error']='Please provide both consumer session and user session'

    return jsonify(response)

if __name__ == '__main__':
    app.run()