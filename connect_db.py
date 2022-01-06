# источник: https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from credentials import user, password

# создадим саму БД sqlalchemy_tuts - ее еще пока не существует
connection = psycopg2.connect(user=user, password=password)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# создадим курсор для работы с БД и саму БД
cursor = connection.cursor()
sql_create_database = cursor.execute('create database sqlalchemy_tuts')
# закроем соединение
cursor.close()
connection.close()

# теперь собственно подключение
conn_string = f"postgresql+psycopg2://{user}:{password}@localhost/sqlalchemy_tuts"
engine = create_engine(conn_string)
print(engine)
engine.dispose()
# базу данных, разумеется, я удалил
