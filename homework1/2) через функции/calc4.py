from functions4 import *

n1 = int(input('Введите первое число: '))
op = input('Введите знак операции: ')
n2 = int(input('Введите второе число: '))

print('Ответ:', end=' ')
if op == '+':
    print(summa(n1, n2))
elif op == '-':
    print(raznost(n1, n2))
elif op == '*':
    print(proizvedenie(n1, n2))
elif op == '/':
    print(delenie(n1, n2))
else:
    print('Введены неверные значения!')
