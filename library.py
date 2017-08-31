from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///Library.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()


association_table = Table('BookAuthor', Base.metadata,
                   Column('author_id', Integer, ForeignKey('Author.AuthorId')),
                   Column('book_id', Integer, ForeignKey('Book.BookId'))
)


# Класс Автор будет выступать первичным классом во взаимодействии Автор-Книга
class Author(Base):
    __tablename__ = 'Author'
    AuthorId = Column(Integer, primary_key=True)
    Name = Column(String)

    def __init__(self, name):
        self.Name = name

    def __repr__(self):
        return "<Author ('%s')>" % self.Name

# Класс Книга - дочерний по отношению к Автору
class Book(Base):
    __tablename__ = 'Book'
    BookId = Column(Integer, primary_key=True)
    Title = Column(String)

    # Создание взаимосвязи на уровне ORM через функцию relationship.
    # Параметр secondary указывает таблицу-связку.
    # Параметр backref указывает ORM использовать аргумент secondary
    #                                     для обратной связи от Автора к Книгам
    Authors = relationship("Author",
                           secondary=association_table, 
                           backref="Books")

    def __init__(self, title, authors):
        self.Title = title
        self.Authors = authors

    def __repr__(self):
        return "<Book ('%s')>" % self.Title

def print_books(session):
    ''' Печать книг в библиотеке
    '''
    print(' -- Книги в библиотеке --')
    for book in session.query(Book):
        print('"{}"'.format(book.Title))
        print(' Authors:', ', '.join(author.Name for author in book.Authors))

journal_association_table = Table('JournalAuthor', Base.metadata,
                                  Column('author_id', Integer, ForeignKey('Author.AuthorId')),
                                  Column('journal_id', Integer, ForeignKey('Journal.JournalId')))

class Journal(Base):
    __tablename__ = 'Journal'
    JournalId = Column(Integer, primary_key=True)
    Title = Column(String)
    Name = Column(String)
    Year = Column(Date)
    Shelve = Column(Integer)
    Publisher = Column(String)
    Authors = relationship("Author",
                           secondary=journal_association_table,
                           backref='Journals')

    def __init__(self, title, authors, name, year, shelve, publisher):
        self.Title = title
        self.Authors = authors
        self.Name = name
        self.Year = year
        self.Shelve = shelve
        self.Publisher = publisher


    def __repr__(self):
        return "<Journal ('%s')>" % self.Title

    def add_journal(self, title, authors, name, year, shelve, publisher):
        session = Session()
        new_journal = Journal(title, authors, name, year, shelve, publisher)
        session.add(new_journal)
        session.commit()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    author = session.query(Author).filter(Author.AuthorId == 1).one()
    Journal.add_journal('Magazine', author, 'weqw', )
