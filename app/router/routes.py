from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    GET_LOGIN = "/get-login"
    LOGIN = "/login"
    
class ZaposlenikRoutesEnum(Enum):
    ZAPOSLENIK = "/zaposlenik"
    ZAPOSLENIK_CREATE = "/zaposlenik/create"
    ZAPOSLENIK_CREATED = "/zaposlenik/created"
    ZAPOSLENIK_ID = "/zaposlenik/<int:id>"
    ZAPOSLENIK_UPDATE = "/zaposlenik/<int:id>/update"
    ZAPOSLENIK_UPDATED = "/zaposlenik/<int:id>/updated"
    ZAPOSLENIK_DELETE = "/zaposlenik/<int:id>/delete"