from people import People


class Employees(People):
    def __init__(self, id_employee):
        # super().__init__(name, patronymic, surname, birthday, phone_number)
        super(People, self).__init__()
        self._id_emp = id_employee

    def __str__(self):
        return '%s %s' % (self._name, self._id_employee)



if __name__ == '__main__':
    ppl = People('Пертр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
    newbie = Employees('123')
    print(newbie.patronymic)

