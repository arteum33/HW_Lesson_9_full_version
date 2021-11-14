import random
# формирование колоды из 36 карт
# масти
SPADES = '♠'
HEARTS = '♥'
DIAMS = '♦'
CLUBS = '♣'
# номинал карт
NOMINALS = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# поиск индекса по номиналу
NAME_TO_VALUE = {n: i for i, n in enumerate(NOMINALS)}
# кол-во карт в руке при раздаче
CARDS_IN_HAND_MAX = 6
N_PLAYERS = 2
# полная колода - 36 карт
DECK = [(nom, suit) for nom in NOMINALS for suit in [SPADES, HEARTS, DIAMS, CLUBS]]
print(str(DECK))


'''
#Создаем класс игрока
class Player:
    def __init__(self, index, cards):
        self.index = index
        self.cards = list(map(tuple, cards))  # убедимся, что будет список кортежей

    def take_cards_from_deck(self, deck: list):
        """
        Взять недостающее количество карт из колоды
        Колода уменьшится
        :param deck: список карт колоды
        """
        lack = max(0, CARDS_IN_HAND_MAX - len(self.cards))
        n = min(len(deck), lack)
        self.add_cards(deck[:n])
        del deck[:n]
        return self

    def sort_hand(self):
        """
        Сортирует карты по достоинству и масти
        """
        self.cards.sort(key=lambda c: (NAME_TO_VALUE[c[0]], c[1]))
        return self
# добор карт
    def add_cards(self, cards):
        self.cards += list(cards)
        self.sort_hand()
        return self

    # всякие вспомогательные функции:

    def __repr__(self):
        return f"Player{self.cards!r}"

    def take_card(self, card):
        self.cards.remove(card)

    @property
    def n_cards(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]
'''


# класс Durak – основному классу игровой логики:
class Durak:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()  # генератор случайных чисел

        self.deck = list(DECK)  # копируем колоду
        self.rng.shuffle(self.deck)  # мешаем карты в копии колоды

        # создаем игроков и раздаем им по 6 карт из перемешанной колоды
        self.players = [Player(i, []).take_cards_from_deck(self.deck)
                        for i in range(N_PLAYERS)]

        # козырь - карта сверху
        self.trump = self.deck[0][1]
        # кладем козырь под низ вращая список по кругу на 1 назад
        self.deck = rotate(self.deck, -1)

        # игровое поле: ключ - атакующая карта, значения - защищающаяся или None
        self.field = {}

        self.attacker_index = 0  # индекс атакующего игрока
        self.winner = None  # индекс победителя



# сдвигает циклично список на n позиций влево (n < 0) или вправо (n > 0)
def rotate(l, n):
    return l[n:] + l[:n]


'''
# Игровое поле здесь – это словарь, где ключ – атакующая карта, а значение – отбивающая карта (если игрок отбился) или None (если он пока еще не отбился от конкретно этой атакующей карты).
    # 
    # Для получения списков карт на поле вводим такие свойства:
'''
@property
def attacking_cards(self):
    """
    Список атакующих карт
    """
    return list(filter(bool, self.field.keys()))

@property
def defending_cards(self):
    """
    Список отбивающих карт (фильртруем None)
    """
    return list(filter(bool, self.field.values()))

@property
def any_unbeaten_card(self):
    """
    Есть ли неотбитые карты
    """
    return any(c is None for c in self.defending_cards)

'''
# А эти свойства помогают определить, кто текущий игрок, а кто его соперник:
'''


@property
def current_player(self):
    return self.players[self.attacker_index]


@property
def opponent_player(self):
    return self.players[(self.attacker_index + 1) % N_PLAYERS]

'''
# Рассмотрим теперь методы атаки и защиты:
'''


def attack(self, card):
    assert not self.winner  # игра не должна быть окончена!

    # можно ли добавить эту карту на поле? (по масти или достоинству)
    if not self.can_add_to_field(card):
        return False
    cur, opp = self.current_player, self.opponent_player
    cur.take_card(card)  # уберем карту из руки атакующего
    self.field[card] = None  # карта добавлена на поле, пока не бита
    return True



'''
# Ходить можно с любой карты, если игровое поле пусто. Но подбрасывать можно только, если карта соответствует по
# достоинству или масти – этой проверкой заведует метод can_add_to_field:
'''


def can_add_to_field(self, card):
    if not self.field:
        # на пустое поле можно ходить любой картой
        return True

    # среди всех атакующих и отбивающих карт ищем совпадения по достоинствам
    for attack_card, defend_card in self.field.items():
        if self.card_match(attack_card, card) or self.card_match(defend_card, card):
            return True
    return False


def card_match(self, card1, card2):
    if card1 is None or card2 is None:
        return False
    n1, _ = card1
    n2, _ = card2
    return n1 == n2  # равны ли достоинства карт?

'''
# Переходим к защите:
'''
def defend(self, attacking_card, defending_card):
    """
    Защита
    :param attacking_card: какую карту отбиваем
    :param defending_card: какой картой защищаемя
    :return: bool - успех или нет
    """
    assert not self.winner  # игра не должна быть окончена!

    if self.field[attacking_card] is not None:
        # если эта карта уже отбита - уходим
        return False
    if self.can_beat(attacking_card, defending_card):
        # еслии можем побить, то кладем ее на поле
        self.field[attacking_card] = defending_card
        # и изымаем из руки защищающегося
        self.opponent_player.take_card(defending_card)
        return True
    return False


'''
# Метод, который определяет бьет ли первая карта вторую выглядит так. Обратите внимание, что предварительно надо
# преобразовать название достоинства карты в числовую характеристику – индекс в массиве достоинств по возрастанию
# (индекс шестерки – 0, семерки – 1, а у туза – 8).
'''


def can_beat(self, card1, card2):
    """
    Бьет ли card1 карту card2
    """
    nom1, suit1 = card1
    nom2, suit2 = card2

    # преобразуем строку-достоинство в численные характеристики
    nom1 = NAME_TO_VALUE[nom1]
    nom2 = NAME_TO_VALUE[nom2]

    if suit2 == self.trump:
        # если козырь, то бьет любой не козырь или козырь младше
        return suit1 != self.trump or nom2 > nom1
    elif suit1 == suit2:
        # иначе должны совпадать масти и номинал второй карты старше первой
        return nom2 > nom1
    else:
        return False

'''
# Метод завершающий ход finish_turn возвращает результат хода. В зависимости от ситуации на столе могут быть такие
# варианты. 1) Отбиты все карты. Тогда ход переходит к игроку, который защищался. Оба добирают из колоды недостающее число
#  карт. 2) Не отбил что-то, тогда право хода не меняется, атакующий добирает карты, а защищающийся собирает со стола все
#  карты к себе в руку. 3) Игра завешена, так как карт в колоде больше нет, и один из соперников тоже избавился от всех
#  карт. Тот, кто остался с картами на руках в конце игры – ДУРАК 😉
'''
# константы результатов хода
NORMAL = 'normal'
TOOK_CARDS = 'не отблися и забрал карты'
GAME_OVER = 'game_over'


@property
def attack_succeed(self):
    return any(def_card is None for def_card in self.field.values())


def finish_turn(self):
    assert not self.winner

    took_cards = False
    if self.attack_succeed:
        # забрать все карты, если игрок не отбился в момент завершения хода
        self._take_all_field()
        took_cards = True
    else:
        # бито! очищаем поле (отдельного списка для бито нет, просто удаляем карты)
        self.field = {}

    # очередность взятия карт из колоды определяется индексом атакующего (можно сдвигать на 1, или нет)
    for p in rotate(self.players, self.attacker_index):
        p.take_cards_from_deck(self.deck)

    # колода опустела?
    if not self.deck:
        for p in self.players:
            if not p.cards:  # если у кого-то кончились карты, он победил!
                self.winner = p.index
                return self.GAME_OVER

    if took_cards:
        return self.TOOK_CARDS
    else:
        # переход хода, если не отбился
        self.attacker_index = self.opponent_player.index
        return self.NORMAL


def _take_all_field(self):
    """
    Соперник берет все катры со стола себе.
    """
    cards = self.attacking_cards + self.defending_cards
    self.opponent_player.add_cards(cards)
    self.field = {}

'''
# Вот и вся логика. Один атакует attack, другой отбивается defend. В любой момент может быть вызван finish_turn, чтобы
# завершить ход. Смотрим на результат хода, и если игра окончена, то в поле winner будет индекс игрока-победителя.
#
# Теперь реализуем локальную игру в консоли, как будто бы оба играют за одним компьютером. Функции по отрисовке состояния
#  игры в консоль собраны в файле _render.py. Не буду их разбирать подробно, так как они не так важны, а в будущем мы
#  прикрутим графическую оболочку и консольные функции потеряют актуальность.
'''
'''

'''
from _render import ConsoleRenderer
from durak import Durak
import random

def local_game():
    # rng = random.Random(42)  # игра с фиксированным рандомом (для отладки)
    rng = random.Random()  # случайная игра

    g = Durak(rng=rng)
    renderer = ConsoleRenderer()

    renderer.help()

    while not g.winner:
        renderer.render_game(g, my_index=0)

        renderer.sep()
        choice = input('Ваш выбор: ')
        # разбиваем на части: команда - пробел - номер карты
        parts = choice.lower().split(' ')
        if not parts:
            break

        command = parts[0]

        try:
            if command == 'f':
                r = g.finish_turn()
                print(f'Ход окончен: {r}')
            elif command == 'a':
                index = int(parts[1]) - 1
                card = g.current_player[index]
                if not g.attack(card):
                    print('Вы не можете ходить с этой карты!')
            elif command == 'd':
                index = int(parts[1]) - 1
                new_card = g.opponent_player[index]

                # варианты защиты выбранной картой
                variants = g.defend_variants(new_card)

                if len(variants) == 1:
                    def_index = variants[0]
                else:
                    def_index = int(input(f'Какую позицию отбить {new_card}? ')) - 1

                old_card = list(g.field.keys())[def_index]
                if not g.defend(old_card, new_card):
                    print('Не можете так отбиться')
            elif command == 'q':
                print('QUIT!')
                break
        except IndexError:
            print('Неправильный выбор карты')
        except ValueError:
            print('Введите число через пробел после команды')

        if g.winner:
            print(f'Игра окончена, победитель игрок: #{g.winner + 1}')
            break

if __name__ == '__main__':
    local_game()


'''
'''
render
'''
from durak import Durak


class GameRenderer:
    def render_game(self, durak: Durak, my_index=None):
        ...

    def sep(self):
        ...

    def help(self):
        ...


class ConsoleRenderer(GameRenderer):
    @classmethod
    def card_2_str(cls, card):
        return '[' + ''.join(card) + ']' if card is not None else '[  ]'

    @classmethod
    def cards_2_str(cls, cards, enum=True):
        if enum:
            cards = (f"{i}. {cls.card_2_str(c)}" for i, c in enumerate(cards, start=1))
        else:
            cards = (cls.card_2_str(c) for c in cards)
        return ", ".join(cards)

    def render_game(self, durak: Durak, my_index=None):
        print('-' * 100)

        print(f'Козырь – [{durak.trump}], {len(durak.deck)} карт в колоде осталось.')

        for player in durak.players:
            marker = " <-- ходит" if player.index == durak.attacker_index else ""
            me_marker = " (это я) " if player.index == my_index else ""
            print(f"{player.index + 1}: {self.cards_2_str(player.cards)}{marker}{me_marker}")

        if durak.field:
            print()

            pairs = list(durak.field.items())
            for i, (ac, dc) in enumerate(pairs, start=1):
                print(f'{i}. Ходит: {self.card_2_str(ac)} - отбиться: {self.card_2_str(dc)}')

    def sep(self):
        print('-' * 100)

    def help(self):
        self.sep()
        print('Помощь')
        print('  1. a [номер] -- атаковать картой')
        print('  2. d [номер] -- отбиваться картой')
        print('  3. f -- завершить ход, (если не отбился - берет все карты)')
        print('  3. q -- выход')
        self.sep()
'''