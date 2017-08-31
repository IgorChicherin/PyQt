from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///enterprise.db', echo=True)
Base = declarative_base()


# TODO Foregin Key for Employees
class Enterpise(Base):
    __tablename__ = 'enterprise'

    org_id = Column(Integer, primary_key=True)
    name = Column(String)
    adress = Column(String)
    inn = Column(Integer)
    email = Column(String)
    phone_number = Column(String)

    def __init__(self, name, adress, inn, email, phone_number):
        # Base.metadata.create_all(engine)
        if self._check(name, 'name'):
            self.name = name
        if self._check(adress, 'adress'):
            self.adress = adress
        if self._check(inn, 'inn'):
            self.inn = inn
        if self._check(email, 'email'):
            self.email = email
        if self._check(phone_number, 'phone'):
            self.phone_number = phone_number

    def __repr__(self):
        return '<Company name={} adress={} inn={} email={} ' \
               'phone_number={}>'.format(self.name, self.adress, self.inn, self.email, self.phone_number)

    def _check(self, value, value_type):
        '''
        Callback check correctness input
        :param value: str , int
        :param value_type: str
        :return: boolean, exception
        '''
        if not value and value_type != 'email':
            raise Exception('Параметр не может быть пустым')
        if value_type == 'id' and type(value) != int:
            raise Exception('ID должен быть числом')
        elif value_type == 'name' and type(value) != str:
            raise Exception('Имя должно быть строкой')
        elif value_type == 'adress' and type(value) != str:
            raise Exception('Адрес должен быть строкой')
        elif value_type == 'inn':
            if type(value) != int:
                raise Exception('ИНН должен быть числом')
            if len(str(value)) != 11:
                raise Exception('ИНН должен содержать 11 цифр')
        elif value_type == 'email':
            if type(value) != str:
                raise Exception('Почтовый ящик должен быть строкой')
            if '@' not in value:
                raise Exception('Почтовый ящик указан без домена')
        elif value_type == 'phone':
            if type(value) != int:
                raise Exception('Телефон должен содержать только цифры')
            if len(str(value)) != 11:
                raise Exception('Телефон должен содержать 11 цифр')
        return True


class People(Base):
    __tablename__ = 'people'

    people_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    patronymic = Column(String)
    surname = Column(String)
    birthday = Column(Date)
    phone_number = Column(Integer)
    # employee = relationship('Employee', back_populates='people')

    def __init__(self, name, patronymic, surname, birthday, phone_number):
        # Base.metadata.create_all(engine)
        if self._check(name, 'name'):
            self.name = name
        if self._check(patronymic, 'patronymic'):
            self.patronymic = patronymic
        if self._check(surname, 'surname'):
            self.surname = surname
        if self._check(birthday, 'birthday'):
            self.birthday = datetime.strptime(birthday, '%d.%m.%Y')
        if self._check(phone_number, 'phone'):
            self.phone_number = phone_number

    def __repr__(self):
        return '<People surname=%s  name=%s patronymic=%s birthday=%s ' \
               'phone_number=%s>' % (self.surname, self.name, self.patronymic, self.birthday, self.phone_number)

    def _check(self, value, value_type):
        '''
        Callback check correctness input
        :param value: str , int
        :param value_type: str
        :return: boolean, exception
        '''
        if not value and value_type != 'email':
            raise Exception('Параметр не может быть пустым')
        if value_type == 'name' or value_type == 'patronymic' or value_type == 'surname':
            if type(value) != str:
                raise Exception('Параметр должен быть строкой')
        elif value_type == 'birthday':
            if type(value) != str:
                raise Exception('Параметр должен иметь формат DD.MM.YYYY')
        elif value_type == 'phone':
            if type(value) != int:
                raise Exception('Телефон должен содержать только цифры')
            if len(str(value)) != 11:
                raise Exception('Телефон должен содержать 11 цифр')
        return True


class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    department_id = Column(Integer)
    people_id = Column(Integer, ForeignKey('people.people_id'))
    wages = Column(Integer)
    # People = relationship('People', back_populates='qweqwe')

    def __init__(self, people_id, department_id, wages):
        # Base.metadata.create_all(engine)
        if self._check(people_id):
            self.people_id = people_id
        if self._check(department_id):
            self.department_id = department_id
        self.wages = wages

    def __repr__(self):
        return '<Employee people_id=%s employee_id=%s ' \
               'department_id=%s wages=%s' % (self.people_id, self.employee_id, self.department_id, self.wages)

    def _check(self, value):
        '''
        Callback check correctness input
        :param value: str , int
        :param value_type: str
        :return: boolean, exception
        '''
        if not value:
            raise Exception('Параметр не может быть пустым')
        if type(value) != int:
            print(value)
            raise Exception('Параметр должен быть числом')
        return True


if __name__ == '__main__':

    ark = Enterpise(name='ARK Group',
                    adress='some address',
                    inn=12345678912,
                    email='some@email',
                    phone_number=89281546474)
    ppl = People('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
    emp = Employee(1, 1, 1000)
    Sesson = sessionmaker(bind=engine)
    session = Sesson()
    session.add_all([ark, ppl, emp])
    session.commit()
    # print(ark)
