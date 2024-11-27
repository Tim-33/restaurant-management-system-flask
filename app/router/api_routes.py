from enum import Enum

class HelloApiRoutesEnum(Enum):
    HELLO = 'hello'
    HELLO_ID = 'hello/<int:id>'