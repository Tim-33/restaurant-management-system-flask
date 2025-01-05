from enum import Enum

class AuthApiRoutesEnum(Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    REGISTER = 'register'

class HelloApiRoutesEnum(Enum):
    HELLO = 'hello'
    HELLO_ID = 'hello/<int:id>'