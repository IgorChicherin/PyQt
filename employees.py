from people import People


class Employees(People):
    def __init__(self, name, patronymic, surname, birthday, phone_number, id_employee):
        super().__init__(name, patronymic, surname, birthday, phone_number)
        self._id_emp = id_employee

    def __str__(self):
        return '%s %s' % (self._name, self._id_employee)



if __name__ == '__main__':
    newbie = Employees('Пертр', 'Петрович', 'Петров', '31.08.1989', 89284453641, '123')
    print(newbie.patronymic)

