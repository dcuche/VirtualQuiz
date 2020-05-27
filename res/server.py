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
    connect_resp = pickle.loads(CONN.recv(HEADER))
    c_pass = connect_resp['JOIN_PASS'] if 'JOIN_PASS' in connect_resp else ''
    if c_pass != JOIN_PASS:
        CONN.send(pickle.dumps({'result':False, 'mess':-1}))
        print(f'[RECHAZO] {addr} - NO PASSWORD')
        CONN.close()
        return
    if quiz.State != GS.WAITING_PLAYERS:
        CONN.send(pickle.dumps({'result':False, 'mess':quiz.State}))
        print(f'[RECHAZO] {addr} - GAME STATE: {quiz.State}')
        CONN.close()
        return

    pname = connect_resp['USER_NAME']
    player = quiz.addPlayer(addr,pname)

    print(f'[CONECCION NUEVA] ({player.id}) "{pname}" conectado desde {addr}!')
    CONN.send(pickle.dumps({'result':True, 'mess':player.id}))

    quiz.addAction(GA.NEW_PLAYER)
    print(f' > Tengo {len(quiz.Players)} jugadores, y mi estado es {quiz.State}')

    connected = True
    while connected:
        try:
            message = quiz.CurrentMessage(player)
            CONN.send(pickle.dumps(message))
            data = pickle.loads(CONN.recv(HEADER))
            if data['action'] != GA.IDLE:
                print(player.id,data)
                quiz.Command(data)
        except:
            print(player.id,'ERROR CONECTING PLAYER')
            quiz.Players.remove(player)
            quiz.addAction(GA.NEW_PLAYER)
            connected = False

    print(f'[CONECCION TERMINADA] Jugador ({player.id}) "{player.name}" de {addr}!')
    if len(quiz.Players) == 0:
        quiz.State = GS.WAITING_PLAYERS
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
