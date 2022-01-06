import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, MetaData, Table, \
    Integer, String, Column, DateTime, ForeignKey, Numeric, CheckConstraint, \
    insert
from datetime import datetime
from credentials import user, password

# создадим схему базы данных
metadata = MetaData()

customers = Table('customers', metadata,
                  Column('id', Integer(), primary_key=True),
                  Column('first_name', String(100), nullable=False),
                  Column('last_name', String(100), nullable=False),
                  Column('username', String(50), nullable=False),
                  Column('email', String(200), nullable=False),
                  Column('address', String(200), nullable=False),
                  Column('town', String(50), nullable=False),
                  Column('created_on', DateTime(), default=datetime.now),
                  Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
                  )

orders = Table('orders', metadata,
               Column('id', Integer(), primary_key=True),
               Column('customer_id', ForeignKey('customers.id'), nullable=False),
               Column('date_placed', DateTime(), default=datetime.now),
               Column('date_shipped', DateTime()),
               )

items = Table('items', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(), nullable=False),
              Column('cost_price', Numeric(10, 2), nullable=False),
              Column('selling_price', Numeric(10, 2), nullable=False),
              Column('quantity', Integer(), nullable=False),
              CheckConstraint('quantity > 0', name='quantity_check')
              )

order_lines = Table('order_lines', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('order_id', ForeignKey('orders.id')),
                    Column('item_id', ForeignKey('items.id')),
                    Column('quantity', Integer()),
                    )

# создадим базу данных и прогрузим в нее схему
db_name = 'sales'
conn_string = f"postgresql+psycopg2://{user}:{password}@localhost/{db_name}"

connection = psycopg2.connect(user=user, password=password)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
drop_db = cursor.execute(f"drop database if exists {db_name}")
create_database = cursor.execute(f"create database {db_name}")
cursor.close()
connection.close()

engine = create_engine(conn_string, echo=True)
engine.connect()
metadata.create_all(engine)

# CRUD-операции (CRUD - Create, Read, Update, Delete)
# создадим инструкцию для вставки
# можно было бы также импортировать функцию insert из SQLAlchemy,
# тогда код выглядел бы вот так ins = insert(customers).values(...)
ins = customers.insert().values(
    first_name='Dmitriy',
    last_name='Yatsenko',
    username='Moseend',
    email='moseend@mail.com',
    address='Shemilovskiy 2-Y Per., bld. 8/10, appt. 23',
    town=' Vladivostok'
)

# изначально вывод показывает только названия вставляемых параметров
print(ins)
# но можно посмотреть и непосредственно на вставляемые значения
print(ins.compile().params)
# теперь необходимо наконец-то выполнить инструкцию
conn = engine.connect()
r = conn.execute(ins)

# метод execute() позволяет вставить несколько записей как список словарей
ins = insert(customers)
r = conn.execute(ins, [
    {
        "first_name": "Vladimir",
        "last_name": "Belousov",
        "username": "Andescols",
        "email": "andescols@mail.com",
        "address": "Ul. Usmanova, bld. 70, appt. 223",
        "town": " Naberezhnye Chelny"
    },
    {
        "first_name": "Tatyana",
        "last_name": "Khakimova",
        "username": "Caltin1962",
        "email": "caltin1962@mail.com",
        "address": "Rossiyskaya, bld. 153, appt. 509",
        "town": "Ufa"
    },
    {
        "first_name": "Pavel",
        "last_name": "Arnautov",
        "username": "Lablen",
        "email": "lablen@mail.com",
        "address": "Krasnoyarskaya Ul., bld. 35, appt. 57",
        "town": "Irkutsk"
    },
])
# можно посмотреть на размер вставки
print(r.rowcount)

# добавим вручную записи в остальные таблицы
items_list = [
    {
        "name": "Chair",
        "cost_price": 9.21,
        "selling_price": 10.81,
        "quantity": 6
    },
    {
        "name": "Pen",
        "cost_price": 3.45,
        "selling_price": 4.51,
        "quantity": 3
    },
    {
        "name": "Headphone",
        "cost_price": 15.52,
        "selling_price": 16.81,
        "quantity": 50
    },
    {
        "name": "Travel Bag",
        "cost_price": 20.1,
        "selling_price": 24.21,
        "quantity": 50
    },
    {
        "name": "Keyboard",
        "cost_price": 20.12,
        "selling_price": 22.11,
        "quantity": 50
    },
    {
        "name": "Monitor",
        "cost_price": 200.14,
        "selling_price": 212.89,
        "quantity": 50
    },
    {
        "name": "Watch",
        "cost_price": 100.58,
        "selling_price": 104.41,
        "quantity": 50
    },
    {
        "name": "Water Bottle",
        "cost_price": 20.89,
        "selling_price": 25.00,
        "quantity": 50
    },
]

order_list = [
    {
        "customer_id": 1
    },
    {
        "customer_id": 1
    }
]

order_line_list = [
    {
        "order_id": 1,
        "item_id": 1,
        "quantity": 5
    },
    {
        "order_id": 1,
        "item_id": 2,
        "quantity": 2
    },
    {
        "order_id": 1,
        "item_id": 3,
        "quantity": 1
    },
    {
        "order_id": 2,
        "item_id": 1,
        "quantity": 5
    },
    {
        "order_id": 2,
        "item_id": 2,
        "quantity": 5
    },
]

r = conn.execute(insert(items), items_list)
print(r.rowcount)
r = conn.execute(insert(orders), order_list)
print(r.rowcount)
r = conn.execute(insert(order_lines), order_line_list)
print(r.rowcount)

# также можно писать запросы с помощью SQLAlchemy, но мне это уже не очень интересно
# хотя в принципе в документации есть описание, инструментарий запросов близок к обычному SQL
# также можно отправлять и "сырые" запросы в виде текста на SQL
# еще есть возможность выполнять транзакции

# обновление записей
from sqlalchemy import update

s = update(items).where(
    items.c.name == 'Water Bottle'
).values(
    selling_price=30,
    quantity=60,
)

print(s)
rs = conn.execute(s)

# удаление записей
from sqlalchemy import delete

s = delete(customers).where(
    customers.c.username.like('Vladim%')
)

print(s)
rs = conn.execute(s)

# выключим все соединения с БД
engine.dispose()
