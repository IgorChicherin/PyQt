from enterprise import Enterpise, People, Employee

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from peewee_library import Author, Book, Journal, BookAuthor, JournalAuthor, db

# SQLAlchemy
engine = create_engine('sqlite:///enterprise.db', echo=True)
Base = declarative_base()

Base.metadata.create_all(engine)
Sesson = sessionmaker(bind=engine)
session = Sesson()
ark = Enterpise(name='ARK Group',
                adress='some address',
                inn=12345678912,
                email='some@email',
                phone_number=89281546474)
ppl = People('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
emp = Employee(1, 1, 1000)
session.add_all([ark, ppl, emp])
session.commit()

# Peewee
db.create_tables([Author, Book, Journal, BookAuthor, JournalAuthor])
Author().update_author('qweqqe', 1)
Journal().delete_journal(1)
Journal().add_journal('Magazine', 'weqw', '30.08.1922', 1, 'azxcz', 1)
print(Book().search_book('qwe'))
a = Author(name='asda')
a.save()
