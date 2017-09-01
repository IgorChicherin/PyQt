from peewee import SqliteDatabase, Model, IntegerField, CharField, DateField, ForeignKeyField, DoesNotExist

db = SqliteDatabase('library.db')


class LibraryModel(Model):
    class Meta:
        database = db


class Author(LibraryModel):
    name = CharField()

    def __repr__(self):
        return "<Author ('%s')>" % self.name

    def update_author(self, name, author_id):
        #TODO update, create, delete почему то не работает ссылка на доки
        # http://docs.peewee-orm.com/en/latest/peewee/api.html?highlight=update

        # Author.update(name=name).where(Author.id == id)

        new_author = Author.get(Author.id == author_id)
        new_author.name = name
        new_author.save()


class Book(LibraryModel):
    title = CharField()

    def __repr__(self):
        return "<Book ('%s')>" % self.title

    def delete_book(self, book_id):
        book = Book.get(Book.id == book_id)
        book.delete_instance()

    def search_book(self, book_name):
        try:
            return Book.get(Book.title == book_name)
        except DoesNotExist:
            return 'Такой книги нет'

class BookAuthor(LibraryModel):
    book = ForeignKeyField(Book, related_name='books')
    author = ForeignKeyField(Author, related_name='authors')


class Journal(LibraryModel):
    title = CharField()
    name = CharField()
    year = DateField()
    shelve = IntegerField()
    publisher = CharField()

    def __repr__(self):
        return "<Journal ('%s')>" % self.title

    def add_journal(self, title, name, year, shelve, publisher, author_id):
        JournalAuthor.create(author=Author.select().where(Author.id == author_id),
                             journal=Journal.create(title=title, name=name, year=year,
                                                    shelve=shelve, publisher=publisher))

    def uppdate_journal(self, name, journal_id):
        new_name = Journal.get(Journal.id == journal_id)
        new_name.name = name
        new_name.save()

    def delete_journal(self, journal_id):
        journal = Journal.get(Journal.id == journal_id)
        journal.delete_instance()


class JournalAuthor(LibraryModel):
    author = ForeignKeyField(Author, related_name='journal_authors')
    journal = ForeignKeyField(Journal, related_name='journals')


if __name__ == '__main__':
    db.create_tables([Author, Book, Journal, BookAuthor, JournalAuthor])
    Author().update_author('qweqqe', 1)
    Journal().delete_journal(1)
    Journal().add_journal('Magazine', 'weqw', '30.08.1922', 1, 'azxcz', 1)
    print(Book().search_book('qwe'))
    a = Author(name='asda')
    a.save()