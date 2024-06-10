import requests as re
from json import loads
from .exceptions import *

BASE_URL ='http://127.0.0.1:5000/api'

def handle_response(response)->dict:
    if response.status_code == 200:
        response = loads(response.text)
        if 'error' in response.keys():
            error = response['error']-1000
            raise ERRORS[error]
    else:
        raise Exception(f'Error {response.status_code}')

    return response


class Consumer:
    @staticmethod
    def request_register(username:str,password:str, email:str):
        data = {}
        data['username'] = username
        data['password'] = password
        data['email'] = email
        response = re.post(BASE_URL+'/consumer/request_registration',data)
        response = handle_response(response)
        return True
    
    def register(registration_id):
        data = {}
        data['registration_id'] = registration_id
        response = re.post(BASE_URL+'/consumer/register',data)
        response = handle_response(response)
        return True

    def __init__(self,username:str,password:str,server_url:str=BASE_URL+'/consumer'):
        data = {}
        self.server_url = server_url
        data['username']=username 
        data['password']=password
        response = re.post(self.server_url+'/login',data)
        response = handle_response(response)
        self.session_id = response.get('session')

    def get_session_data(self, session_id):
        data = {}
        data['consumer_session'] = self.session_id
        data['user_session']=session_id
        response = re.post(self.server_url+'/session_data',data)
        response = handle_response(response)
        return response['response']

class User:
    def register(username, password ):
        data = {}
        data['username'] = username
        data['password'] = password
        response = re.post(BASE_URL+'/user/register',data)
        response = handle_response(response)
        return True

    def login(username, password)->str:
        data = {}
        data['username'] = username
        data['password'] = password
        response = re.post(BASE_URL+'/user/login',data)
        response = handle_response(response)
        return response['session_id']

    def change_password():
        pass