from enterprise import Enterpise
from people import People
from employees import Employees


ark = Enterpise(1, 'ARK Group', 'some address', 12345678912, 'some@email', 89281546474)
ppl = People('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641)
emp = Employees('Петр', 'Петрович', 'Петров', '31.08.1989', 89284453641, 1, 2, 10000)

print('Enterprise:', ark, 'People:', ppl, 'Employee:', emp)