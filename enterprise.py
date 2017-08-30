from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

class Enterpise(Base):

    __tablename__ = 'enterprise'

    org_id = Column(Integer, primary_key=True)
    name = Column(String)
    adress = Column(String)
    inn = Column(Integer)
    email = Column(String)
    phone_number = Column(String)
    # employees = Column(Text)


    def __init__(self, name, adress, inn, email, phone_number):
        Base.metadata.create_all(engine)
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
        # self.employees = list()

    def __repr__(self, name, adress, inn, email, phone_number):
        return '<Company name={} adress={} inn={} email={} phone_number={}'.format(self.name, self.adress, self.inn,
                                                                                   self.email, self.phone_number)

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


if __name__ == '__main__':
    ark = Enterpise(name='ARK Group', adress='some address', inn=12345678912, email='some@email', phone_number=89281546474)
    Sesson = sessionmaker(bind=engine)
    session = Sesson()
    session.add(ark)
    session.commit()


