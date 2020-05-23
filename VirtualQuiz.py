# -*- coding: utf-8 -*-
# Version 0.055 2020-05-22 HAE test
import pygame
import random
from res.CardClass import CardImg, card_dirs
from res.network import Network, NetworkEvents
from res.QuizGame import GameActions as GA

server = Network()

gameState = ''

cur_lat = 0
Players = []

numEnem = 1

""" ############################################################## """
fpsClock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

from res.Graphs import *

pygame.display.set_caption('VirtualQuiz 4000')
pygame.display.set_icon(pygame.image.load('res/icon16.png'))
screen = pygame.display.set_mode(WIN_DIM)

import res.Intro as Intro

""" ############################################################## """
running = True
logging = True
while logging:
    user, res = Intro.wait(screen, server)

    if res == 'quit':
        running = False
        logging = False
    elif res == 'logged':
        logging = False

    pygame.display.update()
    fpsClock.tick(FPS)

""" ############################################################## """

gamePos = (0, 0)
gameCont = pygame.Surface(WIN_DIM)

for i in range(100):
    gameCont.fill(palete['celeste'])
    gameCont.set_alpha(i)
    screen.blit(gameCont, gamePos)
    pygame.display.update()
    fpsClock.tick(FPS)

gameCont = pygame.Surface(WIN_DIM)

theme = 'res/sfx/intr_f'
pygame.mixer.music.load('res/sfx/mars_full')

Board = getBoard(numEnem)
""" ############################################################## """
cards = []
back = CardImg(card_dirs[0],0)

backCent = back.image.get_rect()
backCent.center = tuple(map(sum, zip(Board['mazo']['surf'].get_rect().center, Board['mazo']['pos'])))
backCent[1] += 2
mazo_start_pos = [MAZO_X+MAZO_W, backCent[1]] # backCent[:2]
back.pos(mazo_start_pos,[WIN_W, backCent[1]])

for i in range(int(len(card_dirs))-1):
    newCard = card_dirs.pop(random.randint(1, len(card_dirs)-1))
    cards.append(CardImg(newCard,i))
    cards[-1].insert(WIN_W,WIN_H)
    cards[-1].pos(mazo_start_pos)

def mazo():
    for card in cards:
        card.move2()
        gameCont.blit(card.image, (card.x, card.y))

gameStart = False
mouse_state = 'arrow'

rollers = []
clickers = []
movers = []

latTimer = 0

latFont = pygame.font.Font('res/8-bit-pusab', 10)

clickers.append(back)
movers.append(back)

pygame.mixer.music.play(-1)

wait_title = Title('Esperando jugadores...', 12, palete['azul'])
wait_title.pos = [mazo_start_pos[0]+6, mazo_start_pos[1]-wait_title.tRect[3]-8]

BlitTexts = []
BlitTexts.append(wait_title)

currMove = False

pTexts = []
pIcons = []
BlitIcons = []
playerStatus = 0
def PlayerList(nPlayers):
    global gameStart
    global pTexts
    global pIcons
    Players = nPlayers
    for pIcon in pIcons:
        BlitIcons.remove(pIcon)
    for pTitle in pTexts:
        BlitTexts.remove(pTitle)
    pTexts = []
    pIcons = []
    allReady = True
    if len(Players) < 3:
        allReady = False
    for i, player in enumerate(Players):
        pstat = server.P_STATUS[i]
        if pstat == 0:
            allReady = False
        if player == server.pname:
            pstat += 1
        pIcon = WaitIcon(pstat)
        pIcon.pos = [mazo_start_pos[0] + backCent[2] + 10, mazo_start_pos[1] + i * wait_title.tRect[3]]
        BlitIcons.append(pIcon)
        pIcons.append(pIcon)
        ptitle = Title(player, 12, palete['azul'])
        ptitle.pos = [mazo_start_pos[0] + backCent[2] + 10 + 30, mazo_start_pos[1] + i * wait_title.tRect[3]]
        pTexts.append(ptitle)
        BlitTexts.append(ptitle)
    if allReady == True and gameStart == False:
        server.State = 'GORILAS'
        server.postAction = GA.NEW_GAME_STATE
        pygame.mixer.music.stop()
        pygame.mixer.music.load(theme)
        pygame.mixer.music.play()
        mouse_state = 'arrow'
        back.mouseRoll(False)
        gameStart = True


PlayerList(server.PLAYERS)

while running:
    gameCont.fill(palete['celeste'])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            server.stop()
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            for card in clickers:
                if card.image.get_rect(topleft=card.rol_pos[:2]).collidepoint(pygame.mouse.get_pos()) and gameStart == False:
                    mouse_state = 'back'
                    card.mouseRoll(True)
                    if card not in rollers:
                        rollers.append(card)
                elif mouse_state == 'back':
                    card.mouseRoll(False)
                    if card not in rollers:
                        rollers.append(card)
                    mouse_state = 'arrow'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_state == 'back' and gameStart == False:
                ## INTRO VERSION ###
                # gameStart = True
                server.postAction = GA.NEW_PLAYER_STATUS
                playerStatus = 2 if playerStatus == 0 else 0
                server.Message = {'pstatus': playerStatus}
                server.State = 'GORILAS'
                #server.send({'pID': server.id, 'state': server.State, 'orig': 'INPUT'})
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load(theme)
                #pygame.mixer.music.play()
                #mouse_state = 'arrow'
                #back.mouseRoll(False)
                back.press()
                if back not in rollers:
                    rollers.append(back)
                #tomove = back.dest([MAZO_X+MAZO_W,back.des_pos[1]])
                #if tomove == True and back not in movers:
                #    movers.append(back)

        if event.type == NetworkEvents.CLIENT_MESSAGE:
            cur_lat = event.lat

            if event.subject != 'IDLE':
                print('VQ:', event)

            if event.subject in ('N_PLAYER', 'N_PSTAT'):
                server.P_STATUS = event.pstats
                PlayerList(event.players)       # AGREGO NUEVOS JUGADORES!
            elif event.subject == 'N_PSTAT':
                pass
            elif event.subject == 'D_PLAYER':
                pass
            elif event.subject == 'N_STATE':
                server.State = event.state

            if event.state == 'GORILAS' and gameStart == False:
                gameStart = True
                server.State = 'GORILAS'
                #pygame.mixer.music.stop()
                #pygame.mixer.music.load(theme)
                #pygame.mixer.music.play()
                #mouse_state = 'arrow'
                back.mouseRoll(False)
                if back not in rollers:
                    rollers.append(back)
                #tomove = back.dest([MAZO_X+MAZO_W,back.des_pos[1]])
                #if tomove == True and back not in movers:
                #    movers.append(back)

        # Key Strokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               running = False
            else:
                if event.key == pygame.K_LEFT:
                    vel_x -= 100
                if event.key == pygame.K_RIGHT:
                    vel_x += 100

    for key, piece in Board.items():
        if key == currMove:
            piece['surf'].fill(palete['rojo'])
            piece['surf'].set_alpha(100)
            gameCont.blit(piece['surf'], piece['pos'])
            #pygame.draw.rect(gameCont, palete['rojo'], pygame.Rect(piece['pos'], piece['size']))

    for rollable in rollers:
        stat = rollable.rollOver()
        if stat == False:
            rollers.remove(rollable)
            #print('Saco el Rolero!',rollers)

    for card in movers:
        stat = card.move()
        if stat == False:
            movers.remove(card)
            #print('Fin Movimiento',movers)

    if gameStart == True:
        mazo()

    gameCont.blit(back.image, back.cur_pos)
    ltext1 = latFont.render(f'lat: {cur_lat}', False, palete['claro'])

    gameCont.blit(ltext1, (WIN_W-80, 2))

    for Text in BlitTexts:
        gameCont.blit(Text.text, Text.pos)
    for Icon in BlitIcons:
        gameCont.blit(Icon.image, Icon.pos)

    if mouse_state == 'arrow':
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    screen.blit(gameCont, gamePos)
    pygame.display.update()
    fpsClock.tick(FPS)
