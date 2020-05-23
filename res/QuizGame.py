from time import time

class GameActions:
    IDLE = 0
    NEW_GAME_STATE = 1
    NEW_PLAYER = 2
    NEW_PLAYER_STATUS = 3
    DROP_PLAYER = 4
    NEW_ROUND = 5
    # PLAYER ACTIONS #
    SHUFFLE = 6
    CUT_DECK = 7
    DEAL_TURN = 8
    PLAYER_BET = 9
    DROP_CARD = 10
    GET_LOT = 11
    
class GameStates:
    WAITING_PLAYERS = 'W_PLAYERS'
    STARTING_GAME = 'S_GAME'
    QUIZING = 'QUIZ'
    GAME_FINISHED = 'G_FINISH'

class Player:
    def __init__(self, name, id, addr):
        self.id = id
        self.addr = addr
        self.name = name
        self.hand = []
        self.latency = 0
        self.s_time = time()
        self.stat = -1  # 0: Waiting, 1: Ready, 2: Playing

    def latClick(self):
        self.latency = time() - self.s_time
        self.s_time = time()
        return int(self.latency * 1000)

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        print(f'  🃏 Mano del {self.name}:')
        print(' ' * 5, end='')
        for card in self.hand:
            card.show()
        print('\n')


class Quiz:
    MAX_PLAYERS = 5

    def __init__(self):
        self.Players = []
        self.Mesa = []
        self.totPlayers = 0
        self.State = GameStates.WAITING_PLAYERS
        self.Actions = {}
        self.Round = 0
        # self.deck = Deck()

    def addPlayer(self, addr, name):
        player = Player(name, self.totPlayers, addr)
        self.Players.append(player)
        self.totPlayers += 1
        self.Actions[player.id] = []
        return player

    def getPlayers(self):
        pnames = []
        pstats = []
        for player in self.Players:
            pnames.append(player.name)
            pstats.append(player.stat)
        return pnames, pstats

    def addAction(self, subject):
        for player in self.Players:
            self.Actions[player.id].append(subject)

    def getAction(self, id):
        return self.Actions[id].pop() if len(self.Actions[id]) else 'IDLE'

    def Command(self, data):
        if data['action'] == NetworkActions.NEW_GAME_STATE:
            self.State = data['state']
            self.addAction(data['action'])
