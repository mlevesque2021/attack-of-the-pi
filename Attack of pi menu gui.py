from Tkinter import *
import pygame
import sys
import pygame.sprite as sprite
#import Spriteslib as Sprites

class Game(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)

        self.startbutton = Button(master, text = "START", fg = "white",bg = "green",  command = self.play, height = 2)
        self.startbutton.pack(side = TOP,fill = X)

        self.button2 = Button(master, text = "QUIT", fg = "white",bg = "red", command = self.quit, height = 2)
        self.button2.pack(side = TOP, fill = X)

        self.img = PhotoImage(file = "space.gif")

        self.l = Label(master, image = self.img)
        self.l.pack(side = BOTTOM, fill=X)

        
#starts the game
    def play(self):
        stage = Stage()
        
        
#ends and exits the game
    def quit(self):
        self.master.destroy()


class Stage(object):
    def __init__(self):
        theClock = pygame.time.Clock()

        background = pygame.image.load('background_image.gif')

        background_size = background.get_size()
        background_rect = background.get_rect()
        screen = pygame.display.set_mode(background_size)
        w,h = background_size
        x = 0
        y = 0

        x1 = 0
        y1 = -h

        running = True

        while running:
            screen.blit(background,background_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            y1 += 5
            y += 5
            screen.blit(background,(x,y))
            screen.blit(background,(x1,y1))
            if y > h:
                y = -h
            if y1 > h:
                y1 = -h
            pygame.display.flip()
            pygame.display.update()
            theClock.tick(10)
        pygame.quit()

#########################################################################

#Default window size
WIDTH = 500
HEIGHT = 550
window = Tk()
window.geometry("{}x{}".format(WIDTH,HEIGHT))
window.title("Attack of The Pi !")
menu = Game(window)
window.mainloop()

