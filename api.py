
import string
import random

from peewee import IntegrityError
from peewee import DoesNotExist

from .models import Consumer
from .models import ConsumerRegistration
from .models import ConsumerSession
from .models import User
from .models import UserSession
from .models import PasswordResetRequest
from .models import PendingRegistration

from .exceptions import *

class Emailer:
    # TODO: Construct the emailer instance using
    # sender's email and credentials
    def __init__(self,email:str,password:str,domain:str,**kwargs) -> None:
        pass

    def send_email(self,message:str,destination:str,attachments=[])->bool:
        print(f'Emailer message:\n destination := {destination} \n message := {message}')
        return True

class SMSer:
    # TODO: Create a class for sending SMS
    def __init__(self,**kwargs) -> None:
        pass

    def send_sms(message:str,destination:str):
        print(f'SMSer message:\n destination := {destination} \n message := {message}')
        return True
    
def hash_function(password:str)->str:
    return password

def random_string(length:int)->str:
    result = ''.join(random.choices(string.ascii_letters,k=length))
    return str(result)

smser = SMSer()
emailer = Emailer('example@domain.com','password1234','domain.com',api_key='asdfqwert')

def create_user_session(username,addr):
    session_id = random_string(48)
    print('session_id',session_id)
    session = UserSession.create(
        session_id=session_id,
        username=username,
        address=addr
        )
    session.save()
    return session_id

def create_consumer_session(username, addr):
    session_id = random_string(48)
    session = ConsumerSession.create(
        session_id=session_id,
        username=username,
        address=addr)
    session.save()
    return session_id
class UserMngr:
    def register(username:str,password:str):
        hashed_password = hash_function(password)
        try:
            user = User.create(username=username,password=hashed_password)
        except IntegrityError:
            raise UsernameTaken('The username provided had been used by another user')
        if not user:
            raise UsernameUnavailable('The username provided has already been used')
        user.save()

    def login(username:str,password:str,addr='127.0.0.1:5000'):
        hashed_password = hash_function(password)
        try:
            user = User.get(username==username,password==hashed_password)
        except DoesNotExist:
            raise UserDoesNotExist('The usename provided does not exist')
        if user:
            return create_user_session(username,addr)
        else:
            return False
        
    def change_password(username:str,old:str,new:str):
        if UserMngr.login(username,old):
            user = User.get(User.username==username)
            user.password = hash_function(new)
            return True
        return False
    
    def session_data(session_id:str):
        try:
            session = UserSession.get(session_id==session_id)
            session_data = {}
            session_data['firstname']='Austine'
            session_data['lastname']='Ochieng'
            return session_data

        except DoesNotExist:
            raise InvalidSession
        
    def start_registration(username:str,addr:str)->str:
        password = random_string(8)
        registration = PendingRegistration.create(
            username = username, 
            password=password,
            addr=addr)
        registration.save()
        return password

    def start_email_registration(username:str):
        password = UserMngr.start_registration(username)
        emailer.send_email(f'use {password} as your password ',username )

    def start_phone_registration(username:str):
        password = UserMngr.start_registration(username)
        smser.send_sms(f'use {password} as your password')

    def finish_registration(username:str,password:str)->str:
        registration = PendingRegistration.get(PendingRegistration.username==username, PendingRegistration.password==password)
        try:
            user = User.get(User.username==registration.username)
            user.delete()
        except:
            pass

        user = User.create(username=registration.username,password=registration.password)
        user.save()
        session_id = create_user_session(registration.username)
        return session_id
    
    def start_password_reset(email:str):
        try:
            user = User.get(User.username==email)
        except DoesNotExist:
            raise UserDoesNotExist('User does not exist')
        if user:
            secret = random.randint(100000,1000000)
            password_reset_request = PasswordResetRequest.create(
                PasswordResetRequest.username==email,
                PasswordResetRequest.secret==secret)
            password_reset_request.save()
            emailer.send_email(f'Your password reset code is: {secret}',email)
            return True
        else:
            return False
        
    def finish_password_reset(username,password,secret):
        password_reset_request = PasswordResetRequest.get(
            PasswordResetRequest.username==username
        )
        if password_reset_request:
            if password_reset_request.secret==secret:
                user = User.get(User.username==username)
                user.password=hash_function(password)
                user.save()

            else:
                raise InvalidResetCode('Invalid password reset code')
        else:
            raise UnregisteredUsername('Username not registered')

    
class ConsumerMngr:
    def request_registration(username:str,password:str,email:str):
        registration_id = random_string(48)
        try:
            consumer_registration = ConsumerRegistration.create(
                registration_id=registration_id,
                registrer = 'admin',
                username=username,
                password=password,
                email=email)
            
        except:
            raise UsernameUnavailable('The username provided has already been used')
        else:
            emailer.send_email(
                f'RegistrationRequest: username={username}, registration_id={registration_id}',
                'admin@domain.com')
        consumer_registration.save()
    def register(registry_id:str):
        try:
            registration = ConsumerRegistration.get(ConsumerRegistration.registration_id==registry_id)
        except DoesNotExist:
            raise InvalidRegistrationId('Invalid registration id')
        try:
            consumer = Consumer.create(username=registration.username,
                                       password=registration.password,
                                       email=registration.email )
            registration.delete()
            consumer.save()
            return True
        except IntegrityError:
            raise UsernameTaken('Username has already been used')
        return False
    
    def login(username:str,password:str,addr:str):
        hashed_password = hash_function(password)
        try:
            consumer = Consumer.get(Consumer.username==username,Consumer.password==hashed_password)
        except DoesNotExist:
            raise UserDoesNotExist('Username provided does not exist')
        if consumer:
            session_id = create_consumer_session(username,addr)
            return session_id
        else:
            return False
        
    def logged_in(session_id)->bool:
        consumer_session = ConsumerSession.get(ConsumerSession.session_id==session_id)
        if consumer_session:
            return True
        else:
            return False
        
    def get_user_session(session_id):
        user_session = UserSession.get(UserSession.session_id==session_id)
        if user_session:
            session_data = {}
            session_data['username'] = user_session.username
            session_data['address'] = user_session.address
            session_data['start_time'] = user_session.start_time
            return session_data
            
        raise UnauthorizedUserSession("The session provided is not authorized")
        

