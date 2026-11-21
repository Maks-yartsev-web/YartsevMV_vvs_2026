import random
from items import make_item, item_str, inventory_str

def get_weapon_damage(pl):
    '''Суммарный бонус урона от оружия в инвентаре'''
    return sum(it.props.get('damage', 0) for it in pl.inventory if it.type == 'weapon')

def get_block(pl):
    '''Суммарный блок от брони в инвентаре'''
    return sum(it.props.get('block', 0) for it in pl.inventory if it.type == 'armor')

def player_has_key(pl):
    '''Есть ли ключ в инвентаре'''
    return any(it.name == 'Ключ' for it in pl.inventory)

def change_room(rm, pl, lab, vis):
    '''Обработать события в комнате при ПЕРВОМ входе'''
    print()
    if rm.type == 'empty':
        print('Пустая комната, ничего интересного')
    elif rm.type == 'start':
        print('Это стартовая комната')
    elif rm.type == 'chest':
        change_chest(rm, pl)
    elif rm.type == 'key':
        change_key_room(rm, pl)
    elif rm.type == 'monster':
        change_monster(rm, pl)
    elif rm.type == 'trap':
        change_trap(rm, pl)
    elif rm.type == 'portal':
        change_portal(rm, pl, lab, vis)
    elif rm.type == 'exit':
        print('Выход! Нужен ключ')

def change_chest(rm, pl):
    '''Сундук: забрать 1 предмет или несколько'''
    if not rm.items:
        print('Сундук пуст')
        return

    print(f'В сундуке лежит: {inventory_str(rm.items)}')
    a = input('Забрать всё? (да/нет): ').lower()
    if a != 'да':
        print('Вы оставили предметы в сундуке')
        return
        
    if len(rm.items) == 1:
        pl.inventory.append(rm.items[0])
        print(f'Добавлено: {item_str(rm.items[0])}')
    else:
        pl.inventory.extend(rm.items)
        print(f'Добавлено предметов: {len(rm.items)}')
    rm.items = []

def change_key_room(rm, pl):
    '''Комната с ключом: забрать ключ'''
    if not rm.items:
        print('Здесь уже пусто')
        return

    print('В комнате находится ключ')
    a = input('Забрать ключ? (да/нет): ').lower()
    if a != 'да':
        print('Ключ остался на месте')
        return
        
    pl.inventory.append(rm.items[0])
    rm.items = []
    print('Ключ добавлен в инвентарь')

def change_monster(rm, pl):
    '''Бой с монстром'''
    if rm.data.get('defeated'):
        print('Здесь лежит побеждённый монстр')
        return
        
    if 'hp' not in rm.data:
        rm.data['hp'] = random.randint(20, 40)
    m_hp = rm.data['hp']
    print(f'Монстр! У него {m_hp} HP')

    while m_hp > 0 and pl.hp > 0:
        print(f'Монстр: {m_hp} HP | Вы: {pl.hp} HP')
        c = input('1 - атака, 2 - предмет, 3 - бег: ')
        
        if c == '1':
            d = random.randint(5, 12) + get_weapon_damage(pl)
            m_hp -= d
            print(f'Вы нанесли {d} урона')
        elif c == '2':
            use_item_in_combat(pl)
        elif c == '3':
            if random.random() < 0.5:
                print('Вы сбежали!')
                rm.data['hp'] = m_hp
                return
            print('Не удалось сбежать!')
        else:
            continue

        if m_hp > 0:
            inc = max(0, random.randint(3, 12) - get_block(pl))
            pl.hp -= inc
            print(f'Монстр бьёт на {inc}')

    if m_hp <= 0:
        print('Монстр побеждён!')
        rm.data['defeated'] = True
        reward = make_item('Золото', 'treasure', {'amount': 25})
        pl.inventory.append(reward)
        print(f'Награда: {item_str(reward)}')

def use_item_in_combat(pl):
    '''Использовать предмет из инвентаря'''
    if not pl.inventory:
        print('Инвентарь пуст!')
        return
        
    print('Инвентарь: ')
    for i in range(len(pl.inventory)):
        print(f' {i}: {item_str(pl.inventory[i])}')
        
    a = input('Индекс предмета (Enter - отмена): ')
    if a == '':
        return
    try:
        ind = int(a)
    except ValueError:
        print('Нужно число!')
        return
        
    if not (0 <= ind < len(pl.inventory)):
        print('Неверный индекс!')
        return
        
    obj = pl.inventory[ind]
    if obj.type == 'potion':
        h = obj.props.get('heal', 0)
        pl.hp += h
        pl.inventory.pop(ind)
        print(f'Использовано: {obj.name}, +{h} HP')
    else:
        print('Этот предмет нельзя использовать в бою!')

def change_trap(rm, pl):
    '''Ловушка: урон, смягчается щитом'''
    if rm.data.get('triggered'):
        print('Ловушка уже сработала')
        return
        
    d = random.randint(10, 25)
    blk = get_block(pl)
    f = max(0, d - blk)
    
    print(f'Ловушка! Урон: {d}, блок: {blk}')
    pl.hp -= f
    rm.data['triggered'] = True
    print(f'Потеряно {f} HP')

def change_portal(rm, pl, lab, vis):
    '''Портал: телепорт в другой портал'''
    h = len(lab)
    w = len(lab[0])
    others = []
    
    for r in range(h):
        for c in range(w):
            if lab[r][c].type == 'portal' and (r, c) != (pl.x, pl.y):
                others.append((r, c))
                
    if not others:
        print('Портал никуда не ведёт - других порталов нет')
        return

    tgt = random.choice(others)
    print(f'Портал! Вас телепортирует в ({tgt[0]}, {tgt[1]})')
    pl.x = tgt[0]
    pl.y = tgt[1]
    vis[tgt[0]][tgt[1]] = True

def use_mana_potion_on_weapon(pl, p_ind, w_ind):
    '''Применить зелье маны к оружию: +урон; меняется свойство предмета'''
    pot = pl.inventory[p_ind]
    wpn = pl.inventory[w_ind]

    if pot.type != 'mana_potion':
        print('Это не зелье маны!')
        return

    if wpn.type != 'weapon':
        print('Маной можно усилить только оружие!')
        return

    bns = pot.props.get('mana', 10)
    prev = wpn.props.get('damage', 0)
    wpn.props['damage'] = prev + bns
    pl.inventory.pop(p_ind)
    print(f'Меч усилен! damage: {prev} -> {prev + bns}')

def use_heal_potion_outside_combat(pl, ind):
    '''Выпить зелье здоровья вне боя'''
    if not (0 <= ind < len(pl.inventory)):
        print('Неверный индекс!')
        return
        
    obj = pl.inventory[ind]
    if obj.type != 'potion':
        print('Это не зелье здоровья!')
        return
        
    h = obj.props.get('heal', 0)
    pl.hp += h
    pl.inventory.pop(ind)
    print(f'Выпито: +{h} HP, теперь HP = {pl.hp}')
