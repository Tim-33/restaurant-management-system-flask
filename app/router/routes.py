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
    
class ZaposlenikPlacaRoutesEnum(Enum):
    ZAPOSLENIK_PLACE = "/zaposlenik-place"
    ZAPOSLENIK_PLACE_MONTH = "/zaposlenik-place/month"
    ZAPOSLENIK_PLACE_CREATE = "/zaposlenik-place/create"
    ZAPOSLENIK_PLACE_CREATED = "/zaposlenik-place/created"
    ZAPOSLENIK_PLACE_ID = "/zaposlenik-place/<int:id>"
    ZAPOSLENIK_PLACE_UPDATE = "/zaposlenik-place/<int:id>/update"
    ZAPOSLENIK_PLACE_UPDATED = "/zaposlenik-place/<int:id>/updated"
    ZAPOSLENIK_PLACE_DELETE = "/zaposlenik-place/<int:id>/delete"
    
class RestoranRoutesEnum(Enum):
    RESTORAN = "/restorani"
    RESTORAN_CREATE = "/restorani/create"
    RESTORAN_CREATED = "/restorani/created"
    RESTORAN_ID = "/restorani/<int:id>"
    RESTORAN_UPDATE = "/restorani/<int:id>/update"
    RESTORAN_UPDATED = "/restorani/<int:id>/updated"
    RESTORAN_DELETE = "/restorani/<int:id>/delete"
    
class SkladisteRoutesEnum(Enum):
    SKLADISTE = "/skladista"
    SKLADISTE_CREATE = "/skladista/create"
    SKLADISTE_CREATED = "/skladista/created"
    SKLADISTE_ID = "/skladista/<int:id>"
    SKLADISTE_UPDATE = "/skladista/<int:id>/update"
    SKLADISTE_UPDATED = "/skladista/<int:id>/updated"
    SKLADISTE_DELETE = "/skladista/<int:id>/delete"