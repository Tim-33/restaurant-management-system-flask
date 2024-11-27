from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    
class HelloRoutesEnum(Enum):
    HELLO = "/hello"
    HELLO_ID = "/hello/<int:id>"