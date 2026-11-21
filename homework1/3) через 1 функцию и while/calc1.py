import functions1 as fn

while 1:
    try:
        n1 = int(input('Введите первое число: '))
        sgn = input('Введите знак операции: ')
        n2 = int(input('Введите второе число: '))
    except ValueError:
        print('Нужно было ввести число!')
        break
    
    # Change order of checks slightly
    if sgn not in {'+', '-', '*', '/'}:
        print('Введены неверные значения!')
    elif sgn == '/' and n2 == 0:
        print('На ноль делить нельзя!')
    else:
        res = fn.f(n1, n2, sgn)
        print(f'Ответ: {res}')
        
    ans = input('Продолжить? ').strip().lower()
    if ans == 'нет':
        break
