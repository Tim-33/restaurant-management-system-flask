from enum import Enum

class HelloSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/hello/select-all.sql'
    SELECT_ONE = 'sql/hello/select-one.sql'
    INSERT = 'sql/hello/insert.sql'
    UPDATE = 'sql/hello/update.sql'
    DELETE = 'sql/hello/delete.sql'
    
class AuthSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/auth/select-all.sql'
    SELECT_ONE = 'sql/auth/select-one.sql'
    INSERT = 'sql/auth/insert.sql'
    UPDATE = 'sql/auth/update.sql'
    DELETE = 'sql/auth/delete.sql'