import json
import os


class Enterpise:
    def __init__(self, org_id, name, adress, inn, email, phone_number):
        if self._check(org_id, 'id'):
            self._org_id = org_id
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
        self._employees = list()

    def __str__(self):
        return 'Название организации: %s \n' \
               'Адрес: %s \n' \
               'ИНН: %s \n' \
               'email: %s \n' \
               'Телефон: %s' % (self.name, self.adress, self.INN, self.email, self.phone_number)

    @property
    def org_id(self):
        return self._org_id

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
        if value_type == 'id' and type(value) != int:
            raise Exception('ID должен быть числом')
        elif value_type == 'name' and type(value) != str:
            raise Exception('Имя должно быть строкой')
        elif value_type == 'adress' and type(value) != str:
            raise Exception('Адрес должен быть строкой')
        elif value_type == 'inn':
            if type(value) != int:
                raise Exception('ИНН должен быть числом')
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

    def save(self):
        data = list()
        if os.path.exists('enterprises.json'):
            with open('enterprises.json', 'r', encoding='utf-8') as file:
                for item in file:
                    data.append(json.loads(item))
            with open('enterprises.json', 'a', encoding='utf-8') as file:
                if data:
                    ids = [item['id'] for item in data]
                    if self._org_id not in ids:
                        file.write(
                            json.dumps(
                                {
                                    'id': self._org_id, 'name': self._name, 'adress': self.adress, 'inn': self._inn,
                                    'email': self._email, 'phone': self._phone_number,'employee_id': self._employees
                                },
                                ensure_ascii=True) + "\n"
                        )
                    else:
                        raise Exception('Такой ID уже существует')
        else:
            with open('enterprises.json', 'a', encoding='utf-8') as file:
                data.append(
                    {
                        'id': self._org_id, 'name': self._name, 'adress': self.adress, 'inn': self._inn,
                        'email': self._email, 'phone': self._phone_number, 'employee_id': self._employees
                    }
                )
                for item in data:
                    file.write(json.dumps(item, ensure_ascii=True) + "\n")

    def add_employee(self, employee_id):
        data = list()
        ent_data = list()
        with open('employees.json', 'r', encoding='utf-8') as file:
            for item in file:
                data.append(json.loads(item))
        ids = [item['id'] for item in data]
        if employee_id in ids:
            for employee in data:
                if employee['id'] == employee_id:
                    self._employees.append(employee['id'])
                    self.save()
        else:
            raise ('Пользователя с таким ID нет')




if __name__ == '__main__':
    ark = Enterpise(11, 'ARK Group', 'some address', 12345678912, 'some@email', 89281546474)
    ark.add_employee(2)
    # ark.save()
