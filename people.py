from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base(bind=engine)

class People(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    patronymic = Column(String)
    surname = Column(String)
    birthday = Column(Date)
    phone_number = Column(Integer)


    def __init__(self, name, patronymic, surname, birthday, phone_number):
        Base.metadata.create_all(engine)
        if self.__check(name, 'name'):
            self.name = name
        if self.__check(patronymic, 'patronymic'):
            self.patronymic = patronymic
        if self.__check(surname, 'surname'):
            self.surname = surname
        if self.__check(birthday, 'birthday'):
            self.birthday = datetime.strptime(birthday, '%d.%m.%Y')
        if self.__check(phone_number, 'phone'):
            self.phone_number = phone_number

    def __repr__(self):
        return '<People surname=%s  name=%s patronymic=%s birthday=%s ' \
               'phone_number=%s>' % (self.surname, self.name, self.patronymic, self.birthday, self.phone_number)

    def __check(self, value, value_type):
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


if __name__ == '__main__':
    emp = People('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
    Sesson = sessionmaker(bind=engine)
    session = Sesson()
    session.add(emp)
    session.commit()
    res = session.query(People).filter(People.name=='Петр').first()
    print(res)
