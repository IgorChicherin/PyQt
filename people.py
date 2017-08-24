class People:
    def __init__(self, name, patronymic, surname, birthday, phone_number):
        if self.__check(name, 'name'):
            self._name = name
        if self.__check(patronymic, 'patronymic'):
            self._patronymic = patronymic
        if self.__check(surname, 'surname'):
            self._surname = surname
        if self.__check(birthday, 'birthday'):
            self._birthday = birthday
        if self.__check(phone_number, 'phone'):
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
        if self.__check(value, 'name'):
            self._name = value

    @property
    def patronymic(self):
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value):
        if self.__check(value, 'patronymic'):
            self._patronymic = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        if self.__check(value, 'surname'):
            self._surname = value

    @property
    def birthday(self):
        return self._birthday

    @surname.setter
    def surname(self, value):
        if self.__check(value, 'birthday'):
            self._birthday = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if self.__check(value, 'phone'):
            self._phone_number = value

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
