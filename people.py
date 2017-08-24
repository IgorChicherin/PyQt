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

    def _check(self, value, value_type):
        pass