from network import Network
from time import sleep

pname = input('Nombre: ')

server = Network()
server.PLAYERS.append(pname)

server.connect(pname)

pID = server.id
if pID == -1:
    print('No se pudo conctar al servidor! :(')
    exit()

totPlayers = pID + 1
print(f'Soy {pname} el jugador {totPlayers}... quedo atento!')
if pID > 0:
    data = server.receive()
    print(f'Los jugafores que estaban antes que yo son {data["players"]}')

server.start()

print(' >>> COMENZAMOS CON EL SERVIDOR!')

if pID == 0:
    begin = input('Comenzar?:')

    if begin == 'si':
        server.State = 'BEGIN'
        server.send({'pID': server.id, 'stat': server.State})


#send(DISCON_MESSAGE)
