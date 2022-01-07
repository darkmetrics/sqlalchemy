# ссылка https://pythonru.com/biblioteki/crud-sqlalchemy-orm

# SQLAlchemy ORM (Object Relational Mapping или «объектно-реляционное отображение»)
# — это способ создания таблиц и отношений между ними с помощью классов в Python.
# Он также предоставляет систему для создания запросов и управления базой данных
# с помощью объектно-ориентированного кода вместо чистого SQL.
# В отличие от SQLAlchemy Core, который сосредоточен на таблицах, строках и колонках,
# во главе угла в случае с ORM стоят объекты и модели.
# ORM построен на базе SQLAlchemy Core

# Чтобы класс был валидной моделью, нужно соответствовать следующим требованиям:
# 1. Наследоваться от декларативного базового класса с помощью вызова функции declarative_base().
# 2. Объявить имя таблицы с помощью атрибута __tablename__.
# 3. Объявить как минимум одну колонку, которая должна быть частью первичного ключа.

# декларативный базовый класс — это оболочка над маппером и MetaData.
# Маппер соотносит подкласс с таблицей, а MetaData сохраняет всю информацию о БД и ее таблицах

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Date, \
    Column, DateTime, ForeignKey, Numeric, Boolean, Text, Index, SmallInteger, \
    PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    # колонки - атрибуты класса
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    content = Column(String(50), nullable=False)
    published = Column(String(200), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# как можно сделать маппинг от Core к ORM
metadata = MetaData()

post = Table('post', metadata,
             Column('id', Integer(), primary_key=True),
             Column('title', String(200), nullable=False),
             Column('slug', String(200), nullable=False),
             Column('content', Text(), nullable=False),
             Column('published', Boolean(), default=False),
             Column('created_on', DateTime(), default=datetime.now),
             Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
             )


class Post(object):
    pass


mapper(Post, post)

# Таким образом у Post сейчас следующие атрибуты:
#     post.id
#     post.title
#     post.slug
#     post.content
#     post.published
#     post.created_on
#     post.updated_on

# При использовании ORM
# ключи и ограничения добавляются с помощью атрибута __table_args__
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('username'),
        UniqueConstraint('email'),
    )


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    content = Column(String(50), nullable=False)
    published = Column(String(200), nullable=False, default=False)
    user_id = Column(Integer(), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id']),
        Index('title_content_index' 'title', 'content'),  # composite index on title and content
    )


# one-to-many
# Отношение один-ко-многим создается за счет передачи внешнего ключа в дочерний класс
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    books = relationship("Book")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    copyright = Column(SmallInteger, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

# Функция relationship() добавляет атрибуты в модели для доступа к связанным данным.
# Как минимум — название класса, отвечающего за одну сторону отношения.
# Имея объект a класса Author, получить доступ к его книгам можно через a.books.
# А если нужно получить автора книги через объект Book?
# Для этого можно определить отдельное отношение relationship() в модели Author:
# author = relationship("Author")
# можно также задать атрибут, который будет использован на другой стороне отношения
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    books = relationship("Book", backref="book")


# Зачем нужен relationship???

# 1. Ответ Stackoverflow
# In SQL, tables are related to each other via foreign keys.
# In an ORM, models are related to each other via relationships.
# You're not required to use relationships,
# just as you are not required to use models (i.e. the ORM).
# Mapped classes give you the ability to work with tables as if they are objects in memory;
# along the same lines, relationships give you the ability
# to work with foreign keys as if they are references in memory.

# 2. Гораздо лучше ясно из официальных доков:
# https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html
# создание связей позволяет, например, автоматически обновлять связанные столбцы
# в разных таблицах


# one-to-one
# нужно просто добавить uselist=False
class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    doj = Column(Date(), nullable=False)
    dl = relationship('DriverLicense', backref='person', uselist=False)


class DriverLicense(Base):
    __tablename__ = 'driverlicense'
    id = Column(Integer(), primary_key=True)
    license_number = Column(String(255), nullable=False)
    renewed_on = Column(Date(), nullable=False)
    expiry_date = Column(Date(), nullable=False)
    person_id = Column(Integer(), ForeignKey('persons.id'))

# many-to-may
# необходима отдельная таблица
# Она создается как экземпляр класса Table и
# затем соединяется с моделью с помощью аргумента secondary функции relationship().

# Один автор может написать одну или несколько книг.
# Так и книга может быть написана одним или несколькими авторами.
# Поэтому здесь требуется отношение многие-ко-многим.
author_book = Table('author_book', Base.metadata,
    Column('author_id', Integer(), ForeignKey("authors.id")),
    Column('book_id', Integer(), ForeignKey("books.id"))
)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    copyright = Column(SmallInteger, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", secondary=author_book, backref="books")


# создание таблиц
# Base.metadata.create_all(engine), по аналогии с Crude
# Также можно удалить все таблицы схожей командой
# Base.metadata.drop_all(engine)



# CRUD - операции
# При использовании SQLAlchemy ORM
# взаимодействие с базой данных происходит через объект Session.
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts")
session = Session(bind=engine)

# Конструктор Session принимает определенное количество аргументов,
# которые определяют режим его работы.
# Если создать сессию таким способом, то в дальнейшем конструктор Session
# будет вызывать с одним и тем же набором параметров.
# Чтобы упростить этот процесс, SQLAlchemy предоставляет класс sessionmaker,
# который создает класс Session с аргументами для конструктора по умолчанию.
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
# Получив доступ к этому классу Session раз,
# можно создавать его экземпляры любое количество раз, не передавая параметры.
session = Session()
# важно, что соединение с БД устанавливается лишь при запросе

# вставка данных
# Для создания новой записи с помощью SQLAlchemy ORM нужно:
# 1. Создать объект
# 2. Добавить его в сессию
# 3. Сохранить сессию
c1 = Customer(
    first_name = 'Dmitriy',
    last_name = 'Yatsenko',
    username = 'Moseend',
    email = 'moseend@mail.com'
)

c2 = Customer(
    first_name = 'Valeriy',
    last_name = 'Golyshkin',
    username = 'Fortioneaks',
    email = 'fortioneaks@gmail.com'
)

print(c1.first_name, c2.last_name)

session.add(c1)
session.add(c2)
# или можно добавить все сразу
session.add_all([c1, c2])

print(session.new)

session.commit()

# получение данных - очень многое из того, что есть в обычном SQL
# можно также удобно обновлять данные

