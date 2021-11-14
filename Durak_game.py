list_deck_cards = []
from itertools_len import  product
for value, suit in product('6789TJQKA', 'CSDH'):
    # for value,suit in product('23456789TJQKA','shdc'):
    list_deck_cards.append(suit + value)
    # return list_deck_cards
print(list_deck_cards)

cards = list(input().split(" "))
trump = input()
jacket = ["6", "7", "8", "9", "10", "J", "Q", "K", "A" ]
deck = list("CSDH")
if (cards[0][-1] not in deck) or (cards[1][-1] not in deck) or (trump not in deck):
    print("Error")
elif cards[0][-1]==trump and cards[1][-1]!=trump:
    #если масть первой карти соввпадает с мастью козиря,edc
    #а масть второй карти не совпадает с козирем,то виводим первую карту
    print("First")
elif cards[0][-1]!=trump and cards[1][-1]==trump:
    #Если масть второй карти совпадает с козирем а первая масть с козирем не совпадает ,
    #то следует вивести вторую карту.
    print("Second")
elif cards[0][-1]==cards[1][-1]:
    if jacket.index(cards[0][:-1])>jacket.index(cards[1][:-1]):
    # Если инедкс значения первой карти больше за индекс значение второй карти
    # при равних мастях карт,то выводить первую карту
        print("First")
    elif jacket.index(cards[0][:-1])<jacket.index(cards[1][:-1]):
    #Если индекс значения  первой карти меньше за индекс значеня второй карти
    #при одинакових мастях следует вивести вторую карту
        print("Second")
    else:
        print("Error")
else:
    print("Error")