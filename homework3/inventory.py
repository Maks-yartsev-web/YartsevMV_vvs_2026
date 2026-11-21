import copy
from items import item_str, inventory_str
from events import use_mana_potion_on_weapon, use_heal_potion_outside_combat

t_order = {
    'weapon': 0,
    'armor': 1,
    'potion': 2,
    'mana_potion': 3,
    'key': 4,
    'scroll': 5,
    'treasure': 6,
}

def sort_key(x):
    '''Критерий сортировки: сначала по типу, потом по имени'''
    return (t_order.get(x.type, 99), x.name)

def find_index_by_name(pl, nm):
    '''Позиция предмета по имени через index(); -1, если нет'''
    return next((i for i, x in enumerate(pl.inventory) if x.name == nm), -1)

def open_inventory(pl):
    '''Меню инвентаря, возвращает None'''
    while True:
        print()
        print('=== ИНВЕНТАРЬ ===')
        if not pl.inventory:
            print('Пусто')
            print('0 - назад')
            if input('> ') == '0':
                return
            continue

        for i in range(len(pl.inventory)):
            print('  ' + str(i) + ': ' + item_str(pl.inventory[i]))
        
        print('Действия:')
        print('  1 - выбросить по имени')
        print('  2 - выбросить по индексу')
        print('  3 - сортировать по типу и имени')
        print('  4 - сортировать по убыванию')
        print('  5 - перевернуть порядок')
        print('  6 - найти предмет')
        print('  7 - копия и срез')
        print('  8 - ДЕМОНСТРАЦИЯ: copy() VS deepcopy()')
        print('  9 - применить предмет к предмету')
        print('  0 - назад')

        c = input('> ')
        if c == '0':
            return

        elif c == '1':
            nm = input('Имя предмета: ')
            i = find_index_by_name(pl, nm)
            if i != -1:
                print('Удалено: ' + item_str(pl.inventory.pop(i)))
            else:
                print('Нет такого предмета')

        elif c == '2':
            a = input('Индекс: ')
            try:
                i = int(a)
            except ValueError:
                print('Нужно число!')
                continue
            if not (0 <= i < len(pl.inventory)):
                print('Неверный индекс!')
                continue
            print('Удалено: ' + item_str(pl.inventory.pop(i)))

        elif c == '3':
            pl.inventory.sort(key=sort_key)
            print('Отсортировано по типу и имени')

        elif c == '4':
            pl.inventory.sort(key=sort_key, reverse=True)
            print('Отсортировано по убыванию')

        elif c == '5':
            pl.inventory.reverse()
            print('Порядок перевёрнут')

        elif c == '6':
            nm = input('Что ищем? ')
            i = find_index_by_name(pl, nm)
            if i == -1:
                print('Не найдено')
            else:
                print('Найдено на позиции ' + str(i) + ': ' + item_str(pl.inventory[i]))

        elif c == '7':
            inv_c = pl.inventory.copy()
            print()
            print('Копия: ' + str(len(inv_c)) + ' предметов')
            print('  ' + inventory_str(inv_c))

            f3 = inv_c[:3]
            print('Первые три:')
            print('  ' + inventory_str(f3))

            print()
            print('ВНИМАНИЕ: copy() — поверхностное!')
            print('Предметы в копии — те же объекты, что в оригинале.')
            print('Команда 8 покажет, почему это проблема.')

        elif c == '8':
            demo_copy_problem(pl)

        elif c == '9':
            print('Что применяем?')
            for i in range(len(pl.inventory)):
                print('  ' + str(i) + ': ' + item_str(pl.inventory[i]))
            a1 = input('Индекс: ')
            try:
                i1 = int(a1)
            except ValueError:
                print('Нужно число!')
                continue
            if not (0 <= i1 < len(pl.inventory)):
                print('Неверный индекс!')
                continue
            
            it_a = pl.inventory[i1]

            if it_a.type == 'potion':
                use_heal_potion_outside_combat(pl, i1)
                continue

            if it_a.type == 'mana_potion':
                a2 = input('К какому оружию? индекс: ')
                try:
                    i2 = int(a2)
                except ValueError:
                    print('Нужно число!')
                    continue
                if not (0 <= i2 < len(pl.inventory)):
                    print('Неверный индекс!')
                    continue
                use_mana_potion_on_weapon(pl, i1, i2)
                continue
            
            print('Этот предмет нельзя применить')
        
        else:
            print('Нет такой команды')

def demo_copy_problem(pl):
    '''Показать разницу между copy() и deepcopy() на практике'''
    if not pl.inventory:
        print('Инвентарь пуст — нечего копировать')
        return

    # Ищем первый предмет, у которого есть свойства (props)
    i = next((j for j, x in enumerate(pl.inventory) if x.props), -1)

    if i == -1:
        print('Нет предметов со свойствами — не на чем демонстрировать')
        return

    # Получаем первый ключ из словаря свойств
    p_k = next(iter(pl.inventory[i].props))
    old_v = pl.inventory[i].props[p_k]

    print()
    print('=== ДЕМОНСТРАЦИЯ: copy() VS deepcopy() ===')
    print('Работаем с предметом: ' + item_str(pl.inventory[i]))
    print('Свойство: ' + p_k + ' (сейчас ' + str(old_v) + ')')

    print()
    print('--- copy() (поверхностное) ---')
    sh = pl.inventory.copy()
    print('Создана копия: .copy()')
    sh[i].props[p_k] = old_v + 100
    print('У копии поменяли ' + p_k + ': ' + str(old_v) + ' -> ' + str(old_v + 100))
    print()
    print('Что стало:')
    print('  Копия:    ' + inventory_str(sh))
    print('  Оригинал: ' + inventory_str(pl.inventory))

    if pl.inventory[i].props[p_k] == old_v + 100:
        print()
        print('!!! ПРОБЛЕМА: оригинал ТОЖЕ изменился!')
        print('copy() копирует только список, а предметы внутри - те же объекты')
        print('Поменяли в копии - поменяли и в оригинале')
        pl.inventory[i].props[p_k] = old_v
        print('(восстановили оригинал на ' + str(old_v) + ')')

    print()
    print('--- deepcopy() (глубокое) ---')
    dp = copy.deepcopy(pl.inventory)
    print('Создана копия: copy.deepcopy()')
    dp[i].props[p_k] = old_v + 100
    print('У копии поменяли ' + p_k + ': ' + str(old_v) + ' -> ' + str(old_v + 100))
    print()
    print('Что стало:')
    print('  Копия:    ' + inventory_str(dp))
    print('  Оригинал: ' + inventory_str(pl.inventory))

    if pl.inventory[i].props[p_k] == old_v:
        print()
        print('Хмм, оригинал НЕ изменился - deepcopy скопировал и предметы тоже.')

    print()
    print('Вывод: в игре используем deepcopy, чтобы предметы в копиях были независимы')
    print('Именно так мы делаем в labirint.py при создании предметов из loot_pool')
