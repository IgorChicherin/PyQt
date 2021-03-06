import json
import threading
import pickle
import os
import hmac
import sys

from datetime import datetime
from socketserver import BaseRequestHandler, TCPServer
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker


class CompanyTCPHandler(BaseRequestHandler):
    def handle(self):
        if self.server_auth(bytes('user', 'utf-8')):
            print('User Authenticated')
            self.data = self.request.recv(1024)
            self.msg = pickle.loads(self.data)
            ent = Enterprise('enterprise')
            if self.msg['command'] == 'add':
                log_msg = "Получил команду {} с параметрами {}".format(self.msg['command'], self.msg)
                print(log_msg)
                del self.msg['command']
                ent.add(Company(**self.msg))
                self.request.sendall(bytes('Done', 'utf-8'))
            elif self.msg['command'] == 'get':
                log_msg = "Получил команду {} с параметрами {}".format(self.msg['command'], self.msg)
                print(log_msg)
                del self.msg['command']
                # TODO как превратить значение словаря в класс???
                res = ent.get(**self.msg)
                print(res)
                # self.request.sendall(bytes(res, 'utf-8'))
            return log_msg
        else:
            self.request.sendall(bytes('You are not our user! Get out here!', 'utf-8'))
            log_msg = 'You are not our user! Get out here!'
            print(log_msg)

    def server_auth(self, secret_key):
        message = os.urandom(32)
        self.request.send(message)
        hash = hmac.new(secret_key, message)
        digest = hash.digest()
        response = self.request.recv(len(digest))
        return hmac.compare_digest(digest, response)


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

    def __str__(self):
        return '<Company name={} adress={} inn={} email={} ' \
               'phone_number={}>'.format(self.name, self.adress, self.inn, self.email, self.phone_number)

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
               'org_id=%s department_id=%s wages=%s>' % (self.id, self.name, self.patronymic, self.surname,
                                                         self.birthday, self.phone_number, self.org_id,
                                                         self.department_id, self.wages)


class ObjectNotInBase(Exception):
    def __str__(self):
        return 'Такой объект не принадлежит к базе'


class Enterprise:
    def __init__(self, name):
        self.engine = create_engine('sqlite:///{}.db?check_same_thread=False'.format(name))
        self._session = self._create_session()
        # self._create_base()

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
        if isinstance(cls, DeclarativeMeta) or cls in (Company, Employee):
            return self._session.query(cls).get(id)
        else:
            raise ObjectNotInBase

    def get_all(self, cls):
        obj = self._session.query(cls).order_by(cls.id)
        return obj

    def add(self, new_obj):
        try:
            self._session.add(new_obj)
            self._session.commit()
            return True
        except Exception:
            return False

    def update(self, obj):
        self._session.commit()

    def delete(self, obj):
        self._session.delete(obj)
        self._session.commit()

    def __del__(self):
        self._session.close()

    def dump(self, cls, file_name):

        def dump_item():
            results = self.get_all(cls)
            json_res = list()
            for result in results:
                result_dict = result.__dict__.copy()
                del result_dict['_sa_instance_state']
                del result_dict['id']
                json_res.append(result_dict)
            with open(file_name, 'w', encoding='utf-8') as file:
                for res_item in json_res:
                    line = json.dumps(res_item) + '\n'
                    file.write(line)

        t = threading.Thread(target=dump_item)
        t.start()

    def load(self, cls, file_name):

        def load_items():
            res = list()
            with open(file_name, 'r', encoding='utf-8') as file:
                for line in file:
                    res.append(json.loads(line))
            self._clean_table(cls, self._session)
            for item in res:
                new_obj = cls(**item)
                self._session.add(new_obj)
                self._session.commit()

        t = threading.Thread(target=load_items)
        t.start()
        t.join()

    def server_mode(self):
        HOST, PORT = 'localhost', 9000
        server = TCPServer((HOST, PORT), CompanyTCPHandler)
        server.serve_forever()


class ServerInterface(QThread):
    # TODO гуя умирают при запуске скорее всего нужна многопоточка
    def __init__(self):
        QThread.__init__(self)
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = uic.loadUi('server.ui')
        self.company = Enterprise('enterprise')
        self.window.exitButton.clicked.connect(self.app.quit)
        self.window.runButton.clicked.connect(self.run)
        self.window.show()
        sys.exit(self.app.exec_())

    def run(self):
        self.company.server_mode()

    def __del__(self):
        self.wait()


if __name__ == '__main__':
    # ServerInterface()
    ark_comp = Enterprise('enterprise')
    ark_comp.server_mode()
    # ark = Company(name='ARK Group',
    #               adress='some address',
    #               inn=12345678912,
    #               email='some@email',
    #               phone_number=89281546474)
    # other = Company(name='Other Group',
    #                 adress='other address',
    #                 inn=12345678912,
    #                 email='other@email',
    #                 phone_number=89281546474)
    # emp = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)
    # ark_comp = Enterprise('enterprise')
    # ark_comp.add(ark)
    # ark_comp.add(other)
    # ark_comp.add(emp)
    # ark_comp.dump(Company, 'company.json')
    # ark_comp.load(Company, 'company.json')
    # empl = ark_comp.get(Employee, 1)
    # empl.name = 'asdasd'
    # ark_comp.update(empl)
    # emp = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)
    # session.add_all([ark, emp])
    # session.commit()
    # print(ark)
