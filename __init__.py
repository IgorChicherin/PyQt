from enterprise import Enterpise, People, Employee



ark = Enterpise('ARK Group', 'some address', 12345678912, 'some@email', 89281546474)
ppl = People('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
emp = Employee(1, 2, 10000)

print('Enterprise:', ark, 'People:', ppl, 'Employee:', emp)