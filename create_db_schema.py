from sqlalchemy import MetaData, Table, String, Integer, \
    Column, Text, DateTime, Boolean, ForeignKey, \
    PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint
from datetime import datetime
from credentials import user, password

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
# one-to-many
user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('user', String(200), nullable=False))
posts = Table('posts', metadata,
              Column('id', Integer(), primary_key=True),
              Column('post_title', String(200), nullable=False),
              Column('post_slug', String(200), nullable=False),
              Column('content', Text(), nullable=False),
              # альтернативный вариант: ForeignKey(user.c.id)
              # колонка с foreing key должна быть определена до зависимой таблицы
              Column('user_id', ForeignKey("users.id")))

# one-to-one
# одна таблица включает общие сведения о работниках, другая - частные
employees = Table('employees', metadata,
                  Column('employee_id', Integer(), primary_key=True),
                  Column('first_name', String(200), nullable=False),
                  Column('last_name', String(200), nullable=False),
                  Column('dob', DateTime(), nullable=False),
                  Column('designation', String(200), nullable=False),
                  )

employee_details = Table('employee_details', metadata,
                         Column('employee_id', ForeignKey('employees.employee_id'), primary_key=True),
                         Column('ssn', String(200), nullable=False),
                         Column('salary', String(200), nullable=False),
                         Column('blood_group', String(200), nullable=False),
                         Column('residential_address', String(200), nullable=False),
                         )

# many-to-many
posts = Table('posts', metadata,
              Column('id', Integer(), primary_key=True),
              Column('post_title', String(200), nullable=False),
              Column('post_slug', String(200), nullable=False),
              Column('content', Text(), nullable=False),
              )

tags = Table('tags', metadata,
             Column('id', Integer(), primary_key=True),
             Column('tag', String(200), nullable=False),
             Column('tag_slug', String(200), nullable=False),
             )

post_tags = Table('post_tags', metadata,
                  Column('post_id', ForeignKey('posts.id')),
                  Column('tag_id', ForeignKey('tags.id'))
                  )

# можно отдельно добавить PrimaryKey, ForeignKey
# PrimaryKey
parent = Table('parent', metadata,
               Column('acc_no', Integer()),
               Column('acc_type', Integer(), nullable=False),
               Column('name', String(16), nullable=False),
               PrimaryKeyConstraint('acc_no', name='acc_no_pk')
               )
# эквивалентно
parent = Table('parent', metadata,
               Column('acc_no', Integer(), primary=True),
               Column('acc_type', Integer(), nullable=False),
               Column('name', String(16), nullable=False),
               )
# Как правило, это нужно для создания составного первичного ключа
parent = Table('parent', metadata,
               Column('acc_no', Integer, nullable=False),
               Column('acc_type', Integer, nullable=False),
               Column('name', String(16), nullable=False),
               PrimaryKeyConstraint('acc_no', 'acc_type', name='uniq_1')
               )
# но можно было бы сделать это и вот так
parent = Table('parent', metadata,
               Column('acc_no', Integer, nullable=False, primary_key=True),
               Column('acc_type', Integer, nullable=False, primary_key=True),
               Column('name', String(16), nullable=False),
               )

# ForeignKey работает аналогично
parent = Table('parent', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(16), nullable=False)
               )

child = Table('child', metadata,
              Column('id', Integer, primary_key=True),
              Column('parent_id', Integer, nullable=False),
              Column('name', String(40), nullable=False),
              ForeignKeyConstraint(['parent_id'], ['parent.id'])
              )
# опять же, реальное удобство в такой конструкции - при использовании составного ключа
parent = Table('parent', metadata,
               Column('id', Integer, nullable=False),
               Column('ssn', Integer, nullable=False),
               Column('name', String(16), nullable=False),
               PrimaryKeyConstraint('id', 'ssn', name='uniq_1')
               )

child = Table('child', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(40), nullable=False),
              Column('parent_id', Integer, nullable=False),
              Column('parent_ssn', Integer, nullable=False),
              ForeignKeyConstraint(['parent_id', 'parent_ssn'], ['parent.id', 'parent.ssn'])
              )

# CheckConstraint используется для проверки при вставке данных
employee = Table('employee', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('name', String(100), nullable=False),
                 Column('salary', Integer(), nullable=False),
                 CheckConstraint('salary < 100000', name='salary_check')
                 )

# Metadata содержит всю информацию о БД и таблицах внутри нее
# с его помощью можно получать доступ к объектам по двум атрибутам:
# tables возвращает immutabledict вида {'имя таблицы': 'содержимое таблицы'}
# sorted_tables возвращает список объектов Table, отсортированных по порядку зависимости
# внешних ключей - то есть таблицы зависимостей идут перед самими зависимостями
metadata = MetaData()

user = Table('users', metadata,
             Column('id', Integer(), primary_key=True),
             Column('user', String(200), nullable=False),
             )

posts = Table('posts', metadata,
              Column('id', Integer(), primary_key=True),
              Column('post_title', String(200), nullable=False),
              Column('post_slug', String(200), nullable=False),
              Column('content', Text(), nullable=False),
              Column('user_id', Integer(), ForeignKey("users.id")),
              )

for t in metadata.tables:
    print(metadata.tables[t])

print('-------------')

for t in metadata.sorted_tables:
    print(t.name)
# ожидаемый вывод
# users
# posts
# -------------
# users
# posts

# После получения доступа к экземпляру Table можно получать доступ к любым деталям о колонках:
print(posts.columns)         # вернуть список колонок
print(posts.c)               # как и post.columns
print(posts.foreign_keys)    # возвращает множество, содержащий внешние ключи таблицы
print(posts.primary_key)     # возвращает первичный ключ таблицы
print(posts.metadata)        # получим объект MetaData из таблицы
print(posts.columns.post_title.name)     # возвращает название колонки
print(posts.columns.post_title.type)     # возвращает тип колонки

# вывод
# ImmutableColumnCollection(posts.id, posts.post_title, posts.post_slug, posts.content, ImmutableColumnCollection(posts.id, posts.post_title, posts.post_slug, posts.content, posts.user_id)
# ImmutableColumnCollection(posts.id, posts.post_title, posts.post_slug, posts.content, posts.user_id)
# {ForeignKey('users.id')}
# PrimaryKeyConstraint(Column('id', Integer(), table=<posts>, primary_key=True, nullable=False))
# MetaData()
# post_title
# VARCHAR(200)

# создать таблицы из Metadata можно с помощью команды с использованием объекта Engine
metadata.create_all(engine)
# Этот метод создает таблицы только в том случае, если они не существуют в базе данных.
# Это значит, что его можно вызвать безопасно несколько раз.
# Удалить все таблицы можно с помощью MetaData.drop_all()
