import os
from sqlite3 import connect
from unittest import TestCase

from enterprise import Company, Employee, Enterprise

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


class TestCompany(TestCase):
    def setUp(self):
        self.company = Company(name='ARK Group',
                               adress='some address',
                               inn=12345678912,
                               email='some@email',
                               phone_number=89281546474)

    def test_repr(self):
        self.assertEqual(str(self.company),
                         '<Company name=ARK Group adress=some address inn=12345678912 email=some@email '
                         'phone_number=89281546474>')

    def tearDown(self):
        del self.company


class TestEmployee(TestCase):
    def setUp(self):
        self.employee = Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)

    def test_repr(self):
        self.assertEqual(str(self.employee), '<Employee employee_id=None name=Петр patronymic=Петрович surname=Петров '
                                             'birthday=1989-08-31 00:00:00 phone_number=89284453641org_id=1 '
                                             'department_id=1 wages=1000>')

    def tearDown(self):
        del self.employee


class TestEnterprise(TestCase):
    def setUp(self):
        self._ent = Enterprise('test_enterprise')
        self._ent.add(Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000))
        self._ent.add(Company(name='ARK Group',
                        adress='some address',
                        inn=12345678912,
                        email='some@email',
                        phone_number=89281546474))


    def test_create_session(self):
        self.assertIsInstance(Enterprise('test_enterprise')._session, Session)

    def test_create_base(self):
        pass

    def test_clean_table(self):
        with connect('test_enterprise.db') as conn:
            cur = conn.cursor()
            query = 'SELECT * FROM company ORDER BY id'
            result = cur.execute(query)
            print(str(result))


    def test_get(self):
        pass

    def test_get_all(self):
        pass

    def test_add(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_del(self):
        pass

    def tearDown(self):
        os.remove('test_enterprise.db')
