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

    org_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    adress = Column(String)
    inn = Column(Integer)
    email = Column(String)
    phone_number = Column(String)

    def __init__(self, name, adress, inn, email, phone_number):
        self.name = name
        self.adress = adress
        self.inn = inn
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return '<Company name={} adress={} inn={} email={} ' \
               'phone_number={}>'.format(self.name, self.adress, self.inn, self.email, self.phone_number)


class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    patronymic = Column(String)
    surname = Column(String)
    birthday = Column(Date)
    phone_number = Column(Integer)
    department_id = Column(Integer)
    org_id = Column(Integer, ForeignKey('enterprise.org_id'))
    wages = Column(Integer)
    # org = relationship('Enterpise', back_populates='name')

    def __init__(self, name, patronymic, surname, birthday, phone_number, org_id, department_id, wages):
        self.name = name
        self.patronymic = patronymic
        self.surname = surname
        self.birthday = datetime.strptime(birthday, '%d.%m.%Y')
        self.phone_number = phone_number
        self.org_id = org_id
        self.department_id = department_id
        self.wages = wages

    def __repr__(self):
        return '<Employee employee_id=%s name=%s patronymic=%s surname=% birthday=%s phone_number=%s' \
               'org_id=%s department_id=%s wages=%s' % (self.employee_id, self.name, self.patronymic, self.surname,
                                                        self.birthday, self.phone_number, self.org_id,
                                                        self.department_id, self.wages)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Sesson = sessionmaker(bind=engine)
    session = Sesson()
    ark = Enterpise(name='ARK Group',
                    adress='some address',
                    inn=12345678912,
                    email='some@email',
                    phone_number=89281546474)
    emp = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)
    session.add_all([ark, emp])
    session.commit()
    # print(ark)
