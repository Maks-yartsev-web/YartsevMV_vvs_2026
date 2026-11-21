import random
import copy
from items import make_item

class Room:
    '''Одна клетка лабиринта'''
    type = ''
    items = None
    data = None

def make_room(t, it, d):
    '''Создать комнату'''
    r = Room()
    r.type = t
    r.items = it
    r.data = d
    return r

# Легенда карты
icons = {
    'start': 'S', 'exit': 'E', 'empty': '.', 'chest': 'C',
    'monster': 'M', 'trap': 'T', 'key': 'K', 'portal': 'P',
}
p_icon = '@'
u_icon = '?'
r_types = ['empty', 'chest', 'monster', 'trap', 'portal']

lt = [
    ('Золото', 'treasure', {'amount': 50}),
    ('Зелье здоровья', 'potion', {'heal': 30}),
    ('Зелье маны', 'mana_potion', {'mana': 10}),
    ('Меч', 'weapon', {'damage': 10}),
    ('Щит', 'armor', {'block': 5}),
    ('Свиток', 'scroll', {}),
]

def generate_labirint(n, m):
    '''Сгенерировать лабиринт n*m'''
    
    # Создаем матрицу комнат через генератор списка
    l = [[make_room(random.choice(r_types), [], {}) for _ in range(m)] for _ in range(n)]

    # Создаем матрицу посещений через генератор
    v = [[False] * m for _ in range(n)]

    l[0][0].type = 'start'
    l[n-1][m-1].type = 'exit'

    # Находим свободные клетки для ключа (кроме старта и выхода) через генератор
    free = [(i, j) for i in range(n) for j in range(m) 
            if (i, j) != (0, 0) and (i, j) != (n-1, m-1)]
            
    kx, ky = random.choice(free)
    l[kx][ky].type = 'key'
    l[kx][ky].items = [make_item('Ключ', 'key', {})]

    for i in range(n):
        for j in range(m):
            if l[i][j].type == 'chest':
                if random.random() < 0.3:
                    l[i][j].items = []
                else:
                    cnt = random.randint(1, 3)
                    ch = random.sample(lt, cnt)
                    # Собираем предметы через генератор списка
                    l[i][j].items = [make_item(nm, tp, copy.deepcopy(pr)) for nm, tp, pr in ch]
    
    return l, v

def show_labirint(l, v, p, n, m):
    '''Нарисовать лабиринт'''
    for i in range(n):
        # Собираем строку из символов через join и тернарные операторы
        row = [
            p_icon if (i, j) == p else 
            icons[l[i][j].type] if v[i][j] else 
            u_icon 
            for j in range(m)
        ]
        # Выводим строку, разделяя символы пробелом
        print(' '.join(row))
