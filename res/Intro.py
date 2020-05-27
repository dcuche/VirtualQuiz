import pygame
import re
from res.Graphs import *
from res.network import  NetworkEvents

MAX_USER_NAME = 20

pausa = 30
intro_pausa = 30
slowpace = 20

pausa = intro_pausa = slowpace = 1

tiping = pygame.mixer.Sound('res/sfx/typed')
deling = pygame.mixer.Sound('res/sfx/deled')
m56k = pygame.mixer.Sound('res/sfx/m56k')
sf2 = pygame.mixer.Sound('res/sfx/sf2')

regex = re.compile('[^a-zA-Z0-9\-\'+@#\"()\[\]_:?!{}$%&\*\\\|=/.,<>; ]')

pointer = Pointer()

caption = 'Nombre: '
user_name = ''
caplen = len(caption)
font = pygame.font.Font('res/8-bit-pusab', 16)
pygame.key.set_repeat(500, 50)
stat = 'tiping'
frame = 0
line = 0
script = ['Conectando con servidor ','. . . . . .','Bienvenido a VirtualQuiz 4000 Services!',
		  '...No hay conexion con el servidor :(']

def wait(screen, server):
	global stat
	global user_name
	global frame
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return (False,'quit')
		if stat == 'tiping':
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and len(user_name.strip()) > 0:
					user_name = user_name.strip()
					stat = 'connecting'
					pygame.display.set_caption('VirtualQuiz 4000 | '+user_name)
					server.pname = user_name
					server.start()
					empty_channel = pygame.mixer.find_channel()
					empty_channel.play(sf2)
				elif event.key == pygame.K_BACKSPACE:
					namelen = len(user_name)
					user_name = user_name[:-1]
					if namelen > len(user_name):
						empty_channel = pygame.mixer.find_channel()
						empty_channel.play(deling)
				elif len(user_name) < MAX_USER_NAME:
					namelen = len(user_name)
					user_name += event.unicode
					user_name = regex.sub('', user_name)
					if namelen < len(user_name):
						empty_channel = pygame.mixer.find_channel()
						empty_channel.play(tiping)
		elif stat == 'connecting':
			if event.type == NetworkEvents.CLIENT_MESSAGE:
				#print('Tengo en INTRO:',event)
				if not event.subject:
					print('> NO HAY CONEXION! :D')
					server.State = False
				elif server.State != event.state:
					server.State = event.state
					server.PLAYERS = event.players
					server.P_STATUS = event.pstatus
					print(event)

	screen.fill((0, 0, 0))
	pointer.run()
	text = font.render(caption + user_name, False, palete['claro'])
	textRect = text.get_rect()
	screen.blit(text, (20, 20))
	if stat == 'tiping':
		screen.blit(pointer.pointer, (20+textRect[2], 37))
	elif stat == 'connecting':
		frame += 1
		line2text = ''
		if frame > intro_pausa and frame < len(script[0])+intro_pausa:
			line2text = script[0][:frame-intro_pausa]
		elif frame >= len(script[0])+intro_pausa:
			line2text = script[0]
			if frame == len(script[0])+pausa*2:
				m56k.play()
			if frame > len(script[0])+pausa*2 and frame < len(script[0])+pausa*2 + slowpace*len(script[1]):
				ind2 = int((frame-len(script[0])-pausa*2)/slowpace)+1
				line2text += script[1][:ind2]
			elif frame >= len(script[0])+pausa*2 + slowpace*len(script[1]):
				line2text += script[1]
				stat = 'starting'
				frame = 0
		line2 = font.render(line2text, False, palete['claro'])
		screen.blit(line2, (20, 20+textRect[3]))
		line2Rect = line2.get_rect()
		screen.blit(pointer.pointer, (20+line2Rect[2], 37 + textRect[3]))
	elif stat == 'starting':
		line2 = font.render(script[0]+script[1], False, palete['claro'])
		line2Rect = line2.get_rect()
		screen.blit(line2, (20, 20 + textRect[3]))
		frame += 1
		pointer_cord =  [20, 37 + textRect[3]+line2Rect[3]]
		if frame > pausa and frame <= 2*pausa:
			pointer_cord = [20, 37 + textRect[3]+2*line2Rect[3]]
		elif frame > 2*pausa:
			# print('>> AQUI ESTAMOS CON:',server.State)
			if server.State != 'W_PLAYERS':
				line3 = font.render(script[3], False, palete['rojo'])
				m56k.stop()
				frame -= 1
			else:
				line3 = font.render(script[2], False, palete['amarillo'])
			line3Rect = line3.get_rect()
			screen.blit(line3, (20, 20 + textRect[3]+2*line2Rect[3]))
			pointer_cord = [20+line3Rect[2], 37 + textRect[3]+2*line2Rect[3]]
		if frame >= 3*pausa:
			pointer_cord = [20 , 37 + textRect[3] + 3 * line2Rect[3]]
			if frame == 4*pausa:
				m56k.stop()
				return user_name, 'logged'
		screen.blit(pointer.pointer,pointer_cord)

	return '', False
