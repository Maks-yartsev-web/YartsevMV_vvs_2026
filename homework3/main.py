import random
from labirint import generate_labirint, show_labirint
from player import make_player, player_pos, try_move
from items import inventory_str
from events import change_room, player_has_key
from inventory import open_inventory

def main():
    # random.seed(1)
    N, M = 10, 10
    lab, vis = generate_labirint(N, M)
    pl = make_player(0, 0)
    vis[0][0] = True

    while True:
        print()
        show_labirint(lab, vis, player_pos(pl), N, M)
        
        # Вынесли проверку ключа в отдельную переменную для чистоты
        k_stat = 'да' if player_has_key(pl) else 'нет'
        print(f'HP: {pl.hp} | Ключ: {k_stat}')
        print(f'Инвентарь: {inventory_str(pl.inventory)}')
        print('w/a/s/d - идти, i - инвентарь, q - выход')

        c = input('Ваш ход: ').lower()
        
        if c == 'q':
            print('Пока!')
            break
            
        if c == 'i':
            open_inventory(pl)
            continue
            
        if not try_move(pl, c, N, M):
            print('Туда нельзя!')
            continue

        x, y = player_pos(pl)

        # Сравнение координат кортежем
        if (x, y) == (N - 1, M - 1) and player_has_key(pl):
            print()
            print('==========================================')
            print('     ПОБЕДА! Вы открыли выход ключом!')
            print('==========================================')
            break

        if not vis[x][y]:
            vis[x][y] = True
            change_room(lab[x][y], pl, lab, vis)
            
            if pl.hp <= 0:
                print(f'\nВы умерли. HP: {pl.hp}')
                break

main()
