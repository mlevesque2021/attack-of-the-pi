from Tkinter import *
import pygame

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
        self.background_colour = (255,255,255)
        (self.width, self.height) = (500,500)

        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Attack of The Pi")
        self.screen.fill(self.background_colour)

        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
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