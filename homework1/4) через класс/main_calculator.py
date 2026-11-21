from calculator import Calculator

c = Calculator()

while True:
    try:
        x = int(input('Введите первое число: '))
        op = input('Введите знак операции: ')
        y = int(input('Введите второе число: '))
    except ValueError:
        print('Нужно было ввести число!')
        break

    if op not in ('+', '-', '*', '/'):
        print('Введены неверные значения!')
    elif op == '/' and y == 0:
        print('На ноль делить нельзя!')
    else:
        print(f'Ответ: {c.calculate(x, y, op)}')

    ans = input('Продолжить? ')
    if ans.strip().lower() == 'нет':
        break
