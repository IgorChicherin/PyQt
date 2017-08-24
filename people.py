class People:
    def __init__(self, name, patronymic, surname, birthday, phone_number):
        if self._check(name, 'name') is True:
            self._name = name
        if self._check(patronymic, 'patronymic') is True:
            self._patronymic = patronymic
        if self._check(surname, 'surname') is True:
            self._surname = surname
        if self._check(birthday, 'birthday') is True:
            self._birthday = birthday
        if self._check(phone_number, 'phone') is True:
            self._phone_number = phone_number

    def __str__(self):
        return 'Фамилия: %s \n' \
               'Имя: %s \n' \
               'Отчество: %s \n' \
               'Год рождения: %s \n' \
               'Телефон: %s' % (self.surname, self.name, self.patronymic, self.birthday, self.phone_number)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._check(value, 'name') is True:
            self._name = value

    @property
    def patronymic(self):
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value):
        if self._check(value, 'patronymic') is True:
            self._patronymic = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        if self._check(value, 'surname'):
            self._surname = value

    @property
    def birthday(self):
        return self._birthday

    @surname.setter
    def surname(self, value):
        if self._check(value, 'birthday') is True:
            self._birthday = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if self._check(value, 'phone') is True:
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
    emp = People('Пертр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
    print(emp)
