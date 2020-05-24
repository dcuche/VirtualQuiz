import socket
import threading
import pickle
from time import sleep
from QuizGame import Quiz, GameActions as GA, GameStates as GS

HEADER = 4096
PORT = 8792
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
DISCON_MESSAGE = 'CHAITO'
JOIN_PASS = 'VQ4000'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

quiz = Quiz()

def handle_client(CONN,addr):
    pname = pickle.loads(CONN.recv(HEADER))
    print(f'[CONECCION NUEVA] {pname} conectado desde {addr}!')
    player = quiz.addPlayer(addr,pname)
    CONN.send(pickle.dumps(player.id))
    quiz.addAction(GA.NEW_PLAYER)
    print(f' > Tengo hasta ahora {len(quiz.Players)} jugadores, y mi estado es {quiz.State}')

    connected = True
    while connected:
        try:
            message = {}
            message['subject'] = quiz.getAction(player.id)
            message['lat'] = player.latClick()
            message['state'] = quiz.State
            if message['subject'] == GA.NEW_PLAYER or message['subject'] == GA.NEW_PLAYER_STATUS:
                players, pstats = quiz.getPlayers()
                message['players'] = players
                message['pstatus'] = pstats
            CONN.send(pickle.dumps(message))
            data = pickle.loads(CONN.recv(HEADER))
            if data['action'] != GA.IDLE:
                print(player.id,data)
                quiz.Command(data)
        except:
            print(player.id,'ERROR CONECTING PLAYER')
            quiz.Players.remove(player)
            quiz.addAction('N_PLAYER')
            connected = False


    print(f'[CONECCION TERMINADA] Jugador {player.id} {addr} se fue pa la casa!')
    if len(quiz.Players) == 0:
        quiz.State = 'W_PLAYERS'
        print(f'[CAMBIO ESTADO] a {quiz.State}')
    CONN.close()

print("[COMENZAMOS] el servidor....")
server.listen()
print(f'[ESPERANDO] escuchando en {SERVER}')

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn,addr))
    thread.start()
    print("[CONEXIONES]:", threading.activeCount()-1)
