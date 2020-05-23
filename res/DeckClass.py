import random

class Card:
    _suits = ['♥','♠','♦','♣']
    _vals = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    
    def __init__(self,suit,val):
        self.val = val
        self.suit = self._suits[suit]
        self.num = self._vals[val]

    def show(self):
        uprint(f' {self.num}{self.suit}',' ')

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in range(0,4):
            for v in range(0,13):
                self.cards.append(Card(s,v))

    def show(self):
        if len(self.cards) > 0:
            for i, c in enumerate(self.cards):
                if i%13 == 0:
                    print('<br>')
                c.show()
        else:
            print(' >> emmm... mazo vacio..')
        print('<br><br>')

    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0,i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def cut(self):
        r = random.randint(0,len(self.cards))
        self.cards = self.cards[r:] + self.cards[:r]

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            print(' >> Pero no quedan cartas!')

class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []

    def draw(self,deck):
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        uprint(f'  🃏 Mano del {self.name}:')
        uprint(' '*5,'')
        for card in self.hand:
            card.show()
        print('<br>')


uprint('🃏 Primero creamos un mazo...')
deck = Deck()
uprint('🃏 uy que me costo.... aqui esta:')
deck.show()
uprint('🃏 Luego rewolvemos....')
deck.shuffle()
uprint('🃏 Asi quedo:')
deck.show()

uprint('🃏 Ahora cortamos...')
deck.cut()
uprint('🃏 Y quedamos filamente con:')
deck.show()

uprint('🃏 Ahora creo al UFO, Waylon, Manzana y al Are')

players = ['UFO','Waylon','Manzana','Are']
table = {}
for player in players:
    table[player] = Player(player)

tot_turno = random.randint(1,int(52/len(players)))

uprint(f'🃏 Reparto a cada uno {tot_turno} cartas...')

for i in range(0,tot_turno):
    for name, hand in table.items():
        hand.draw(deck)
uprint('🃏 Y asi quedan!')
print('<p>')
for name, hand in table.items():
    hand.showHand()
print('</p>')

uprint('🃏 Y bueno entonces en el mazo me quedan:')
deck.show()

uprint('🃏 Ah! y por ultimo.. saquemos el triumfo!')
card = deck.draw()
card.show()
uprint('<br>')

uprint('🃏 tonce.. finalmente el mazo queda:')
deck.show()
