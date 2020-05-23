import pygame.image
import random

card_dirs = ['0_MAZO','1_SPAD_02','1_SPAD_03','1_SPAD_04','1_SPAD_05','1_SPAD_06','1_SPAD_07','1_SPAD_08','1_SPAD_09','1_SPAD_10','1_SPAD_14_A','1_SPAD_11_J','1_SPAD_12_Q','1_SPAD_13_K',
           '2_DIAM_02','2_DIAM_03','2_DIAM_04','2_DIAM_05','2_DIAM_06','2_DIAM_07','2_DIAM_08','2_DIAM_09','2_DIAM_10','2_DIAM_14_A','2_DIAM_11_J','2_DIAM_12_Q','2_DIAM_13_K',
           '3_CLUB_02','3_CLUB_03','3_CLUB_04','3_CLUB_05','3_CLUB_06','3_CLUB_07','3_CLUB_08','3_CLUB_09','3_CLUB_10','3_CLUB_14_A','3_CLUB_11_J','3_CLUB_12_Q','3_CLUB_13_K',
           '4_HEART_02','4_HEART_03','4_HEART_04','4_HEART_05','4_HEART_06','4_HEART_07','4_HEART_08','4_HEART_09','4_HEART_10','4_HEART_14_A','4_HEART_11_J','4_HEART_12_Q','4_HEART_13_K',
           '5_JOCK_R','5_JOCK_B']

c_back = '0_MAZO'

t = 1/15
g = 9.8*30

class CardImg:
    _suits = ['♥', '♠', '♦', '♣']
    _vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    pos = ()
    rolld = 8
    rolling = False
    moving = False
    rol_pos = (0, 0)
    cur_pos = (0, 0)
    des_por = (0, 0)
    CARD_H = 90
    CARD_W = 70
    moving = 0

    def __init__(self,cimg,ind,flipped = False):
        self.img = cimg
        self.flipped = flipped
        self.cont = 0
        self.indice = ind
        if flipped:
            self.image = pygame.image.load('res/mz/0_MAZO.png').convert_alpha()
        else:
            self.image = pygame.image.load('res/mz/'+cimg+'.png').convert_alpha()
        self.origImage = self.image

    def pos(self, cord, cur=False, ref=(0,0), scale = (1,1)):
        self.rol_pos = cord.copy()
        self.des_pos = cord.copy()
        self.x = cord[0]
        self.y = cord[1]
        if cur == False:
            self.cur_pos = cord.copy()
        else:
            self.cur_pos = cur.copy()
            self.moving = True
        self.ref = ref
        self.scale = scale

    def getPos(self):
        return (self.pos[0] + self.ref[0],self.pos[1]+self.ref[1])

    def insert(self,WIN_W,WIN_H):
        self.WIN_W = WIN_W
        self.WIN_H = WIN_H
        self.vel_x = random.randint(-400,400)
        self.vel_y = -random.randint(0,150)-350

    def press(self):
        self.cur_pos = [self.cur_pos[0], self.cur_pos[1]+10]

    def flip(self):
        pass

    def mouseRoll(self,roll):
        self.rolling = roll

    def rollOver(self):
        if self.rolling == True:
            if abs(self.cur_pos[1]-(self.des_pos[1]-self.rolld)) > 2:
                self.cur_pos[1] += round(((self.des_pos[1]-self.rolld)-self.cur_pos[1])/4)
                return True
            else:
                self.cur_pos[1] = self.des_pos[1]-self.rolld
                self.rolls = 0
                return True
        else:
            if abs(self.des_pos[1]-self.cur_pos[1]) > 2:
                self.cur_pos[1] += round((self.des_pos[1]-self.cur_pos[1])/3)
                return True
            else:
                self.cur_pos[1] = self.des_pos[1]
                self.rolls = 0
                return False

    def dest(self,cords):
        if self.cur_pos == cords:
            print(self,'No me muevo nada!')
            return False

        self.des_pos = cords.copy()
        self.rol_pos = cords.copy()
        self.moving = True
        return True

    def move(self):
        if not self.moving:
            return False
        moved = False

        spd = 4

        if abs(self.des_pos[0]-self.cur_pos[0]) > 2:
            self.cur_pos[0] += round((self.des_pos[0]-self.cur_pos[0])/spd)
            moved = True
        else:
            self.cur_pos[0] = self.des_pos[0]

        if  abs(self.des_pos[1]-self.cur_pos[1]) > 2:
            self.cur_pos[1] += round((self.des_pos[1]-self.cur_pos[1])/spd)
            moved = True
        else:
            self.cur_pos[1] = self.des_pos[1]

        if moved == False:
            self.moving = 0
            return False
        return True

    def move2(self):
        self.cont +=1
        
        if self.cont > self.indice*25/2+20/2:
            self.moving = 1
        
        if not self.moving:
            return
        #self.angle = -(self.y - 800 + self.card_h)/5
        #self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.x += self.vel_x * t

        if self.x > self.WIN_W - self.CARD_W:
            self.x = self.WIN_W - self.CARD_W
            self.vel_x *= -1
            self.vel_y *= 0.9
        elif self.x < -4:
            self.x = -4
            self.vel_x *= -1
            self.vel_y *= 0.9

        self.vel_y += g * t
        self.y += self.vel_y * t + 0.5 * g * t * t

        if self.y > self.WIN_H - self.CARD_H:
            self.y = self.WIN_H - self.CARD_H
            self.vel_y = -self.vel_y * 0.95
            self.vel_x *= 0.95
        elif self.y < 0:
            self.y = 0
            self.vel_y = -self.vel_y * 0.95
            self.vel_x *= 0.95
        self.y = round(self.y)
        self.x = round(self.x)