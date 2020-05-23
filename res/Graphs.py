from pygame import Surface, font, image

palete = {'consol_w' : (243,243,243),
          'rojo' : (171,82,54),
          'celeste' : (41,173,255),
          'amarillo' : (255,163,0),
          'claro' : (194,195,199),
          'oscuro' : (95,87,79),
          'piel' : (255,204,170),
          'azul' : (33,44,85) }

CARD_DIM = (70, 94)
WIN_W = 1020
WIN_H = 760
WIN_DIM = (WIN_W, WIN_H)
OL_H = 30
M_SEP = 40

FPS = 60

PLAYER_TITLE = 40
PLAYER_H = 300
ENEMI_H = PLAYER_H 
MAZO_H = WIN_DIM[1] - PLAYER_H - ENEMI_H - PLAYER_TITLE
MAZO_W = int(WIN_DIM[0] / 3)

MAZO_X = int((MAZO_W-4*OL_H-2*CARD_DIM[0]-M_SEP)/2)

f1_s = 'res/8-bit-pusab'


def getBoard(n_enem):
    Board = {}
    for i in range(n_enem):
        Board['player' + str(i + 1)] = {'size': (int(WIN_W / n_enem), PLAYER_H),
                                        'surf': Surface((int(WIN_W / n_enem), ENEMI_H)),
                                        'pos': (i * n_enem, PLAYER_TITLE)}
    Board['player0'] = {'size': (WIN_W, PLAYER_H),
                        'surf': Surface((WIN_W, PLAYER_H)),
                        'pos': (0, WIN_H - PLAYER_H)}
    Board['mazo'] = {'size': (MAZO_W, MAZO_H),
                     'surf': Surface((MAZO_W, MAZO_H)),
                     'pos': (MAZO_W, PLAYER_H + PLAYER_TITLE)}
    return Board


class WaitIcon:

    icons = ['crzn_g.png', 'crzn_h.png', 'crzn_r.png', 'crzn_a.png']
    pos = [0,0]

    def __init__(self, stat):
        self.status = stat
        self.image = image.load('res/img/'+self.icons[stat]).convert_alpha()

    def State(self, state):
        self.status = state
        self.image = image.load('res/img/'+self.icons[state]).convert_alpha()


class Title:

    def __init__(self, cont, size, color):
        tfont = font.Font(f1_s, size)
        self.text = tfont.render(cont, False, color)
        self.tRect = self.text.get_rect()
        self.pos = [0, 0]


class Pointer:

    def __init__(self):
        self.pointer = Surface((16, 8))
        self.pointer.fill(palete['claro'])
        self.alpha = 255
        self.alpha_vel = -10

    def run(self):
        self.pointer.set_alpha(self.alpha)
        self.alpha += self.alpha_vel
        if self.alpha <= 0 or self.alpha >= 255:
            self.alpha_vel *= -1
