from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    adress = Column(String)
    inn = Column(Integer)
    email = Column(String)
    phone_number = Column(Integer)

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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    patronymic = Column(String)
    surname = Column(String)
    birthday = Column(Date)
    phone_number = Column(Integer)
    department_id = Column(Integer)
    org_id = Column(Integer, ForeignKey('company.id'))
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
        return '<Employee employee_id=%s name=%s patronymic=%s surname=%s birthday=%s phone_number=%s' \
               'org_id=%s department_id=%s wages=%s' % (self.id, self.name, self.patronymic, self.surname,
                                                        self.birthday, self.phone_number, self.org_id,
                                                        self.department_id, self.wages)


class Enterprise:
    def __init__(self):
        self.engine = create_engine('sqlite:///enterprise.db')
        self._session = self._create_session()
        self._create_base()

    def _create_session(self):
        Sesson = sessionmaker(bind=self.engine)
        session = Sesson()
        return session

    def _create_base(self):
        Base.metadata.create_all(self.engine)
        self._clean_table(Company, self._session)
        self._clean_table(Employee, self._session)

    def _clean_table(self, cls, session):
        models = session.query(cls).order_by(cls.id)
        for model in models:
            session.delete(model)
        session.commit()

    def get(self, cls, id):
        return self._session.query(cls).get(id)

    def get_all(self, cls):
        obj = self._session.query(cls).order_by(cls.id)
        return obj

    def add(self, new_obj):
        self._session.add(new_obj)
        self._session.commit()

    def update(self, obj):
        self._session.commit()

    def delete(self, obj):
        self._session.delete(obj)
        self._session.commit()

    def __del__(self):
        self._session.close()

if __name__ == '__main__':
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
    # emp = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)
    # session.add_all([ark, emp])
    # session.commit()
    # print(ark)
