class UsernameUnavailable(Exception):
    CODE = 1001

class PasswordMismatch(Exception):
    CODE = 1002

class UnauthorizedConsumerSession(Exception):
    CODE = 1003

class UnauthorizedUserSession(Exception):
    CODE = 1004

class InvalidResetCode(Exception):
    CODE = 1005

class UnregisteredUsername(Exception):
    CODE = 1006

class UsernameTaken(Exception):
    CODE = 1007

class UserDoesNotExist(Exception):
    CODE = 1008

class InvalidRegistrationId(Exception):
    CODE = 1009

class InvalidSession(Exception):
    CODE = 1010

ERRORS =[
    UsernameUnavailable,
    PasswordMismatch,
    UnauthorizedConsumerSession,
    UnauthorizedUserSession,
    InvalidResetCode,
    UnregisteredUsername,
    UsernameTaken,
    UserDoesNotExist,
    InvalidRegistrationId,
    InvalidSession
]