from Tkinter import *
import pygame
from pygame.locals import *
import sys
import pygame.sprite as sprite
import Spriteslib as Sprites
#import joystickLibv2 as Joystick
Console = "PC"


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

#Sprites.init()
FPS = 60
class Game(Frame):
        def __init__(self,master, score, lives):
                Frame.__init__(self,master)

                self.startbutton = Button(master, text = "START", fg = "white",bg = "green",  command = self.play, height = 2)
                self.startbutton.pack(side = TOP,fill = X)

                self.button2 = Button(master, text = "QUIT", fg = "white",bg = "red", command = self.quit, height = 2)
                self.button2.pack(side = TOP, fill = X)

                self.img = PhotoImage(file = "space.gif")

                self.l = Label(master, image = self.img)
                self.l.pack(side = BOTTOM, fill=X)
                self.score = score
                self.lives = lives

        @property
        def score(self):
                return self._score

        @score.setter
        def score(self, value):
                self._score = value

        @property
        def lives(self):
                return self._lives
        
        @lives.setter
        def lives(self, value):
                self._lives = value


        def events(self, Console):
                if (Console == "PC"):
                        keys = pygame.key.get_pressed()

                        if keys[K_RIGHT]:
                                self.player.xVel = 5
                                
                        elif keys[K_LEFT]:
                                self.player.xVel = -5

                        else:
                                self.player.xVel = 0
                                self.player.yVel = 0

                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        global running
                                        running = False  
                                if event.type == pygame.KEYDOWN:
                                        if event.key==pygame.K_SPACE:
                                                Sprites.Bullet(self.player, screen)
                                        if event.key ==pygame.K_e:
                                                Sprites.Enemy1(300, 50, screen)
                elif (Console == "PI"):
                        mstatus = Joystick.readChannel(1)
                        fstatus = Joystick.readChannel(0)
                        pygame.event.pump()									
                        if fstatus == "YES":
                                Sprites.Bullet(self.player, screen)

                        if mstatus == "Right":
                                self.player.xVel = 1
                                
                        elif mstatus == "Left":
                                self.player.xVel = -1

                        else:
                                self.player.xVel = 0
                                self.player.yVel = 0

                        for event in pygame.event.get():
                                if event.type == pygame.QUIT: 
                                        global running
                                        running = False
        





#starts the game
        def play(self):
                theClock = pygame.time.Clock()
                background = pygame.image.load('background_image.gif')
                background_size = background.get_size()
                background_rect = background.get_rect()
                global screen
                screen = pygame.display.set_mode(background_size)
                w,h = background_size

                x = 0
                y = 0
                x1 = 0
                y1 = -h
                #Sprites.init()
                self.player = Sprites.Player(250,430, screen)
                global running
                global Console
                running = True
                while running:
                    #screen.blit(background,background_rect) ---- When the FPS was ramped up this was not needed and actually was the cause of our screen tearing
                    pygame.display.update()
                    y1 += 5
                    y += 5
                    screen.blit(background,(x,y))
                    screen.blit(background,(x1,y1))
                    score_counter(screen, self.score)
                    life_counter(screen, self.lives)
                    self.events(Console)
                    Sprites.GenLevel(screen)
                    self.events(Console)
                    Sprites.players.update()
                    Sprites.bullets.update()
                    Sprites.enemys.update()
                    if y > h:
                        y = -h
                    if y1 > h:
                        y1 = -h
                    pygame.display.flip()
                    pygame.display.update()
                    theClock.tick(FPS)
                pygame.quit()

 
        
#ends and exits the game
        def quit(self):
                self.master.destroy()



def score_counter(screen, score):
        textsurface = myfont.render("Score = {}".format(score), False, (255, 255, 255))
        screen.blit(textsurface,(0,420))

def life_counter(screen, lives):
        textsurface = myfont.render("Lives = {}".format(lives), False, (255, 255, 255))
        screen.blit(textsurface,(700,420))
#########################################################################

#Default window size
WIDTH = 500
HEIGHT = 550
window = Tk()
window.geometry("{}x{}".format(WIDTH,HEIGHT))
window.title("Attack of The Pi !")
menu = Game(window, score= 0, lives= 10)
window.mainloop()






#########################################################################
