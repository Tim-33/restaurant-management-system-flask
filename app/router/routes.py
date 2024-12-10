from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    
class HelloRoutesEnum(Enum):
    HELLO = "/hello"
    HELLO_CREATE = "/hello/create"
    HELLO_CREATED = "/hello/created"
    HELLO_ID = "/hello/<int:id>"
    HELLO_UPDATE = "/hello/<int:id>/update"
    HELLO_UPDATED = "/hello/<int:id>/updated"
    HELLO_DELETE = "/hello/<int:id>/delete"