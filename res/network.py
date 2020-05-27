import threading
from pygame import event, USEREVENT
import enum
import socket
from time import sleep
import pickle
from res.QuizGame import GameActions as GA, GameStates as GS

class NetworkEvents(enum.IntEnum):
    CLIENT_CONNECTED = USEREVENT + 1
    CLIENT_HANGUP = USEREVENT + 2
    CLIENT_MESSAGE = USEREVENT + 3

class Network(threading.Thread):
    HEADER = 4096
    SERVERS = [
                '175.193.206.200',  # ROBOTO KOREA
                '69.163.163.192'    # DREAMHOST USA
              ]
    ACTIVE_SERVER = 1
    PORT = 8792
    DISCON_MESSAGE = 'CHAITO'
    JOIN_PASS = 'VQ4000'
    MIN_LAT = 10

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER = self.SERVERS[self.ACTIVE_SERVER]
        self.ADDR = (self.SERVER, self.PORT)
        self.id = -1
        self.State = ''
        self.pname = ''
        self.PLAYERS = []
        self.P_STATUS = {}
        self.postAction = GA.IDLE
        self.Message = ''

    def run(self):
        self.id = self.connect()
        if self.id == -1:
            self.pgPost({"subject": False})
            return
        print(f'[COENCTADO] id: {self.id}')
        while self.id > -1:
            data = self.receive()
            self.pgPost(data)
            self.MIN_LAT = (100 - data['lat']) if (100 - data['lat']) > 10 else 10
            # INFLATED LATENCY
            sleep(self.MIN_LAT/1000)

            self.send({'pID': self.id, 'action': self.postAction, 'state': self.State, 'mess': self.Message})
            self.postAction = GA.IDLE

        self.stop()

    def pgPost(self, mess):
        n_event = event.Event(NetworkEvents.CLIENT_MESSAGE, mess)
        event.post(n_event)

    def connect(self):
        try:
            self.client.connect(self.ADDR)
            self.client.send(pickle.dumps({'JOIN_PASS':self.JOIN_PASS,'USER_NAME':self.pname}))
            print('> Conectandose a VirtualQuiz Services...')
            resp = pickle.loads(self.client.recv(self.HEADER))
            print('[RESPUESTA SERVIDOR]',resp)
            if not resp['result']:
                if resp['mess'] < 0:
                    return -2
                else:
                    self.State = resp['mess']
                    return -3
            self.id = resp['mess']
            return self.id
        except socket.error as e:
            print(e)
            return -1

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)
            self.State = None
            return False

    def receive(self):
        try:
            return pickle.loads(self.client.recv(self.HEADER))
        except socket.error as e:
            print(e)
            self.State = None
            return False

    def close(self):
        try:
            self.client.send(pickle.dumps({self.DISCON_MESSAGE: 0}))
            return True
        except socket.error as e:
            print(e)

    def stop(self):
        self.id = -1
        self.State = None
