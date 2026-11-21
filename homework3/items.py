class Item:
    '''Предмет в инвентаре'''
    name = ''
    type = ''
    props = None

def make_item(n, t, p):
    '''Создать предмет'''
    x = Item()
    x.name = n
    x.type = t
    x.props = p
    return x

def item_str(it):
    '''Печать одного предмета строкой'''
    if not it.props:
        return f'{it.name} [{it.type}]'
    
    # Генератор списка внутри join() вместо цикла с append
    p_str = ', '.join(f'{k}={v}' for k, v in it.props.items())
    return f'{it.name} [{it.type}] ({p_str})'

def inventory_str(lst):
    '''Печать всего инвентаря одной строкой'''
    if not lst:
        return '[]'
        
    # Аналогично, генератор внутри join()
    return f"[{', '.join(item_str(x) for x in lst)}]"
