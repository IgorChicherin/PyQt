class Enterpise:
    def __init__(self, name, adress, inn, email, phone_number):
        #if self._check(name, 'name') is True:
        self._name = name
        self._adress = adress
        self._inn = inn
        self._email = email
        self._phone_number = phone_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise Exception('Имя не может быть пустым')
        else:
            if type(value) != str:
                raise Exception('Имя должно быть строкой')
        self._name = value

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, value):
        if not value:
            raise Exception('Адрес не может быть пустым')
        else:
            if type(value) != str:
                raise Exception('Адрес должен быть строкой')
        self._adress = value

    @property
    def INN(self):
        return self._inn

    @INN.setter
    def INN(self, value):
        if type(value) != int:
            raise Exception('ИНН должен содержать только цифры')
        if len(str(value)) < 11 or len(str(value)) > 11:
            raise Exception('ИНН должен содержать 11 цифр')
        self._inn = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if type(value) != str:
            raise Exception('Почтовый ящик должен быть строкой')
        if '@' not in value:
            raise Exception('Почтовый ящик указан без домена')
        self._email = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if type(value) != int:
            raise Exception('Телефон должен содержать только цифры')
        if len(str(value)) < 11 or len(str(value)) > 11:
            raise Exception('Телефон должен содержать 11 цифр')
        self._phone_number = value

    def __str__(self):
        return 'Название организации: %s \n' \
               'Адрес: %s \n' \
               'ИНН: %s \n' \
               'email: %s \n' \
               'Телефон: %s' % (self.name, self.adress, self.INN, self.email, self.phone_number)
    #
    # def _check(self, value, value_type):
    #     '''
    #     Callback check correctness input
    #     :param value:
    #     :return: boolean, exception
    #     '''
    #     if not value:
    #         raise Exception('Параметр не может быть пустым')
    #     if value_type == 'name':
    #         if type(value) != str:
    #             raise Exception('Имя должно быть строкой')
    #     elif value_type == ''
    #     return True


ark = Enterpise('ARK Group', 'some address', 'some inn', 'some@email', 'some p.num')
# ark = Enterpise(1, 'some address', 'some inn', 'some@email', 'some p.num')

print(ark)
