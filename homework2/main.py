from functions import *
while True:
    print('Введите номер уровня: ', end = '')
    try:
        lvl = int(input())
    except ValueError:
        print('Данные некорректны!')
        continue
    if lvl == 1:
        def1()
    elif lvl == 2:
        def2()
    elif lvl == 3:
        def3()
    elif lvl == 4:
        def4()
    elif lvl == 5:
        def5()
    else:
        print('Такого уровня не существует!')
    ans = input('Продолжить? Введите "да" или "нет": ')
    if ans.strip().lower() == 'нет':
        break
