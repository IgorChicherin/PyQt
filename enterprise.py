class Enterpise:
    def __init__(self, name, adress, inn, email, phone_number):
        if self._check(name, 'name'):
            self._name = name
        if self._check(adress, 'adress'):
            self._adress = adress
        if self._check(inn, 'inn'):
            self._inn = inn
        if self._check(email, 'email'):
            self._email = email
        if self._check(phone_number, 'phone'):
            self._phone_number = phone_number

    def __str__(self):
        return 'Название организации: %s \n' \
               'Адрес: %s \n' \
               'ИНН: %s \n' \
               'email: %s \n' \
               'Телефон: %s' % (self.name, self.adress, self.INN, self.email, self.phone_number)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._check(value, 'name'):
            self._name = value

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, value):
        if self._check(value, 'adress'):
            self._adress = value

    @property
    def INN(self):
        return self._inn

    @INN.setter
    def INN(self, value):
        if self._check(value, 'inn'):
            self._inn = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if self._check(value, 'email'):
            self._email = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if self._check(value, 'phone'):
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
        if value_type == 'name':
            if type(value) != str:
                raise Exception('Имя должно быть строкой')
        elif value_type == 'adress':
            if type(value) != str:
                raise Exception('Адрес должен быть строкой')
        elif value_type == 'inn':
            if len(str(value)) != 11:
                raise Exception('ИНН должен содержать 11 цифр')
        elif value_type == 'email':
            if type(value) != str:
                raise Exception('Почтовый ящик должен быть строкой')
            if '@' not in value:
                raise Exception('Почтовый ящик указан без домена')
        elif value_type == 'phone':
            if type(value) != int:
                raise Exception('Телефон должен содержать только цифры')
            if len(str(value)) != 11:
                raise Exception('Телефон должен содержать 11 цифр')
        return True



