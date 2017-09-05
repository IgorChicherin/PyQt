import os
from sqlite3 import connect
from unittest import TestCase

from sqlalchemy.orm import Session

from enterprise import Company, Employee, Enterprise, ObjectNotInBase


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
        self.assertTrue(os.path.exists('test_enterprise.db'))

    def test_clean_table(self):
        # Не знаю правильно ли это... может можно как-то проще
        session = self._ent._create_session()
        self._ent._clean_table(Employee, session)
        self._ent._clean_table(Company, session)
        with connect('test_enterprise.db') as conn:
            cur = conn.cursor()
            company_query = 'SELECT * FROM company ORDER BY id'
            company_result = cur.execute(company_query).fetchall()
            employee_query = 'SELECT * FROM employees ORDER BY org_id'
            employee_result = cur.execute(employee_query).fetchall()
        self.assertEqual(len(company_result), 0)
        self.assertEqual(len(employee_result), 0)

    def test_get(self):
        with connect('test_enterprise.db') as conn:
            cur = conn.cursor()
            company_query = 'SELECT name FROM company WHERE id = 1'
            company_result = cur.execute(company_query).fetchone()
            employee_query = 'SELECT name FROM employees WHERE org_id = 1'
            employee_result = cur.execute(employee_query).fetchone()
        self.assertEqual(self._ent.get(Company, 1).name, company_result[0])
        self.assertEqual(self._ent.get(Employee, 1).name, employee_result[0])
        with self.assertRaises(ObjectNotInBase):
            self._ent.get(Enterprise, 4)

    def test_get_all(self):
        cls_result = list()
        for company in self._ent.get_all(Company):
            cls_result.append([company.id, company.name, company.adress, company.inn, company.email,
                               company.phone_number])
        q_result = list()
        with connect('test_enterprise.db') as conn:
            cur = conn.cursor()
            q = 'SELECT * FROM company'
        for company in cur.execute(q).fetchall():
            q_result.append([company[0], company[1], company[2], company[3], company[4], company[5]])
        self.assertEqual(cls_result, q_result)

    def test_add(self):
        self.assertTrue(self._ent.add(Employee('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 1, 1000)))

    def test_update(self):
        emp = self._ent.get(Employee, 1)
        emp.name = '23123'
        self._ent.update(emp)
        self.assertTrue(self._ent.get(Employee, 1).name == '23123')



    def test_delete(self):
        emp = self._ent.get(Employee, 1)
        self._ent.delete(emp)
        self.assertIsNone(self._ent.get(Employee, 1))

    def tearDown(self):
        os.remove('test_enterprise.db')

