from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    GET_LOGIN = "/get-login"
    LOGIN = "/login"
    
class HelloRoutesEnum(Enum):
    HELLO = "/hello"
    HELLO_CREATE = "/hello/create"
    HELLO_CREATED = "/hello/created"
    HELLO_ID = "/hello/<int:id>"
    HELLO_UPDATE = "/hello/<int:id>/update"
    HELLO_UPDATED = "/hello/<int:id>/updated"
    HELLO_DELETE = "/hello/<int:id>/delete"
    
class ZaposlenikRoutesEnum(Enum):
    ZAPOSLENIK = "/zaposlenik"
    ZAPOSLENIK_CREATE = "/zaposlenik/create"
    ZAPOSLENIK_CREATED = "/zaposlenik/created"
    ZAPOSLENIK_ID = "/zaposlenik/<int:id>"
    ZAPOSLENIK_UPDATE = "/zaposlenik/<int:id>/update"
    ZAPOSLENIK_UPDATED = "/zaposlenik/<int:id>/updated"
    ZAPOSLENIK_DELETE = "/zaposlenik/<int:id>/delete"