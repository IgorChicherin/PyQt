import json

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
# metadata = MetaData()
# enterprise_table = Table('entrprise', metadata, Column('org_id', )
# )


class Enterpise(Base):
    __tablename__ = 'enterprise'

    org_id = Column(Integer, primary_key=True)
    name = Column(String)
    adress = Column(String)
    INN = Column(Integer)
    email = Column(String)
    phone_number = Column(String)

    def __init__(self, name, adress, inn, email, phone_number):
        if self._check(name, 'name'):
            self._name = name
        if self._check(adress, 'adress'):
            self._adress = adress
        if self._check(inn, 'inn'):
            self._inn = inn
        if self._check(email, 'email'):
            self._email = email
        if self._check(phone_number, 'phone'):
            self._phone_number = phone_number
        self._employees = list()

    def __str__(self):
        return 'Название организации: %s \n' \
               'Адрес: %s \n' \
               'ИНН: %s \n' \
               'email: %s \n' \
               'Телефон: %s' % (self._name, self._adress, self._inn, self._email, self._phone_number)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._check(value, 'name'):
            self._name = value

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, value):
        if self._check(value, 'adress'):
            self._adress = value

    @property
    def INN(self):
        return self._inn

    @INN.setter
    def INN(self, value):
        if self._check(value, 'inn'):
            self._inn = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if self._check(value, 'email'):
            self._email = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if self._check(value, 'phone'):
            self._phone_number = value

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

    def save(self):
        pass

    def add_employee(self, employee_id):
        data = list()
        ent_data = list()
        with open('employees.json', 'r', encoding='utf-8') as file:
            for item in file:
                data.append(json.loads(item))
        ids = [item['id'] for item in data]
        if employee_id in ids:
            for employee in data:
                if employee['id'] == employee_id:
                    self._employees.append(employee['id'])
                    self.save()
        else:
            raise ('Пользователя с таким ID нет')


if __name__ == '__main__':
    ark = Enterpise('ARK Group', 'some address', 12345678912, 'some@email', 89281546474)
    Sesson = sessionmaker(bind=engine)
    session = Sesson()
    session.add(ark)
    session.commit()
    # q = session.query(Enterpise).filter_by(org_id='1').first()
    # print(q)
    # ark.INN = 12348617893
    # print(ark.INN)
    # ark.add_employee(2)
    # ark.save()
