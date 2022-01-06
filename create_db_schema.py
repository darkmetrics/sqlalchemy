from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

# информация о всей БД и таблицах, используется для создания или удаления таблиц в БД
metadata = MetaData()

blog = Table('blog', metadata,
             # первичный ключ, для создания составного нужно проставить True в неск. столбцах
             Column('id', Integer(), primary_key=True),
             Column('post_title', String(200), nullable=False),
             Column('post_slug', String(200), nullable=False),
             Column('content', Text(), nullable=False),
             # значения по умолчанию - default
             Column('published', Boolean(), default=True),
             Column('created_on', DateTime(), default=datetime.now),
             # onupdate - значение по умолчанию, если при обновлении ничего не передали
             Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
             )

# дополнительные параметры: unique, index, auto_increment

# SQLAlchemy	Python	            SQL
# BigInteger	int	                BIGINT
# Boolean	    bool	            BOOLEAN или SMALLINT
# Date	        datetime.date	    DATE
# DateTime	    datetime.datetime	DATETIME
# Integer	    int	                INTEGER
# Float	        float	            FLOAT или REAL
# Numeric	    decimal.Decimal	    NUMERIC
# Text	        str	                TEXT

# реляционные связи
# one-to
