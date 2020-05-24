import time

class GameActions:
    IDLE = 1
    NEW_GAME_STATE = 2
    NEW_PLAYER = 3
    NEW_PLAYER_STATUS = 4
    DROP_PLAYER = 5
    NEW_ROUND = 6
    # PLAYER ACTIONS #
    SHUFFLE = 7
    CUT_DECK = 8
    DEAL_TURN = 9
    PLAYER_BET = 10
    DROP_CARD = 11
    GET_LOT = 11

class GameStates:
    WAITING_PLAYERS = 'W_PLAYERS'
    STARTING_GAME = 'S_GAME'
    QUIZING = 'QUIZ'
    GAME_FINISHED = 'G_FINISH'

class Player:
    def __init__(self,name,id,addr):
        self.id = id
        self.addr = addr
        self.name = name
        self.hand = []
        self.latency = 0
        self.s_time = time.time()
        self.stat = 0 # 0: Waiting, 1: Ready, 2: Playing

    def latClick(self):
        self.latency = time.time() - self.s_time
        self.s_time = time.time()
        return int(self.latency*1000)

    def draw(self,deck):
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        print(f'  🃏 Mano del {self.name}:')
        print(' '*5,end='')
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

    def addPlayer(self,addr,name):
        player = Player(name,self.totPlayers,addr)
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

    def playerMove(self,id,data):
        for player in self.Players:
            if player.id == id:
                player.stat = data['pstatus']

    def addAction(self,subject):
        for player in self.Players:
            self.Actions[player.id].append(subject)


    def getAction(self,id):
        return self.Actions[id].pop() if len(self.Actions[id]) else GameActions.IDLE

    def Command(self,data):
        self.addAction(data['action'])
        if data['action'] == GameActions.NEW_GAME_STATE:
            self.State = data['state']
        elif data['action'] == GameActions.NEW_PLAYER_STATUS:
            self.playerMove(data['pID'],data['mess'])
