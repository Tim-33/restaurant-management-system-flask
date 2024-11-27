from enum import Enum

class HelloSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/hello/select-all.sql'
    SELECT_ONE = 'sql/hello/select-one.sql'
    INSERT = 'sql/hello/insert.sql'
    UPDATE = 'sql/hello/update.sql'
    DELETE = 'sql/hello/delete.sql'