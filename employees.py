from people import People


class Employees(People):
    def __init__(self, name, patronymic, surname, birthday, phone_number, employee_id, department_id, wages):

        super().__init__(name, patronymic, surname, birthday, phone_number)

        if self._check(employee_id):
            self._employee_id = employee_id
        if self._check(department_id):
            self._department_id = department_id
        if self._check(wages):
            self._wages = wages

    def __str__(self):
        return 'Фамилия: %s \n' \
               'Имя: %s \n' \
               'Отчество: %s \n' \
               'Год рождения: %s \n' \
               'Телефон: %s \n'\
               'ID сотрудника: %s \n' \
               'ID отдела: %s \n' \
               'Оклад: %s' % (self.surname, self.name, self.patronymic, self.birthday, self.phone_number,
                              self._employee_id, self._department_id, self._wages)

    @property
    def id_employee(self):
        return self._employee_id

    @id_employee.setter
    def id_employee(self, value):
        if self._check(value):
            self._employee_id = value

    @property
    def department_id(self):
        return self.department_id

    @department_id.setter
    def department_id(self, value):
        if self._check(value):
            self.department_id = value

    @property
    def wages(self):
        return self.wages

    @wages.setter
    def wages(self, value):
        if self._check(value):
            self._wages = value

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
    newbie = Employees('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 2, 10000)
    print(newbie)
