from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    GET_LOGIN = "/get-login"
    LOGIN = "/login"
    
class ZaposlenikRoutesEnum(Enum):
    ZAPOSLENIK = "/zaposlenici"
    ZAPOSLENIK_CREATE = "/zaposlenici/create"
    ZAPOSLENIK_CREATED = "/zaposlenici/created"
    ZAPOSLENIK_ID = "/zaposlenici/<int:id>"
    ZAPOSLENIK_UPDATE = "/zaposlenici/<int:id>/update"
    ZAPOSLENIK_UPDATED = "/zaposlenici/<int:id>/updated"
    ZAPOSLENIK_DELETE = "/zaposlenici/<int:id>/delete"