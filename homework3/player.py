class Player:
    '''Игрок в лабиринте'''
    x = 0
    y = 0
    hp = 100
    inventory = None

def make_player(x, y):
    '''Создать игрока'''
    p = Player()
    p.x = x
    p.y = y
    p.hp = 100
    p.inventory = []
    return p

def player_pos(p):
    '''Координаты игрока кортежем'''
    return (p.x, p.y)

def try_move(p, d, N, M):
    '''Попытка сдвинуть игрока'''
    # Словарь, где ключ - направление, а значение - смещение (dx, dy)
    moves = {
        'w': (-1, 0),
        's': (1, 0),
        'a': (0, -1),
        'd': (0, 1)
    }
    
    # Если нажата не та клавиша - сразу выход
    if d not in moves:
        return False
        
    dx, dy = moves[d]
    nx, ny = p.x + dx, p.y + dy

    # Проверка, не вышли ли за границы (0 <= nx < N)
    if not (0 <= nx < N and 0 <= ny < M):
        return False

    p.x, p.y = nx, ny
    return True
