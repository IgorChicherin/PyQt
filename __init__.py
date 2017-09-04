from enterprise import Enterprise, Employee, Company

from sqlalchemy.ext.declarative import declarative_base

from peewee_library import Author, Book, Journal, BookAuthor, JournalAuthor, db

# SQLAlchemy
Base = declarative_base()
ark = Company(name='ARK Group',
              adress='some address',
              inn=12345678912,
              email='some@email',
              phone_number=89281546474)
emp = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)
ark_comp = Enterprise()
ark_comp.add(ark)
ark_comp.add(emp)
empl = ark_comp.get(Employee, 1)
empl.name = 'asdasd'
ark_comp.update(empl)

# Peewee
db.create_tables([Author, Book, Journal, BookAuthor, JournalAuthor])
Author().update_author('qweqqe', 1)
Journal().delete_journal(1)
Journal().add_journal('Magazine', 'weqw', '30.08.1922', 1, 'azxcz', 1)
print(Book().search_book('qwe'))
a = Author(name='asda')
a.save()
