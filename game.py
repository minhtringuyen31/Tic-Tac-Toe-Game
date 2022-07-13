import time
from setting import *
import pygame as pg
from pygame.locals import*
from board import board, XAT, player
import sys
import os

"""
    Data structure TicTacToe: logic class
        Logic game tictactoe with methods
    """
class TicTacToe: 

    def __init__(self, game, level, play):
        self.game = game
        self.__level = level
        self.__board = board(self.__level)
        self.play = play
        self.__cell_size = (WIDTH_SCREEN // self.__level)
        self.__cell_center = self.__cell_size / 2
        self.winer = None
        self.game_step = 0
        self.font = pg.font.SysFont('Verdana', self.__cell_size // 4, True)
        self.turn = play
        self.__player = player(float('-inf'))
        self.__botXAT = XAT('inf', self.__player)
        self.switch = False
        if(self.__level == 3):
            self.depth = 5
        elif(self.__level == 5 or self.__level == 7):
            self.depth = 3
    
    # Run game process
    def runGameProcess(self):
        left_click = pg.mouse.get_pressed()[0]         
        current_cell = self.game.vector(pg.mouse.get_pos()) // self.__cell_size
        col, row = map(int, current_cell)
        result = []
        # Assign best sutuation
        best_situation = float("-inf")
        if self.play: 
            if(left_click) and self.__board.matrix[row][col] == INF:
                self.__player.action([row, col], self.__board)
                self.game_step += 1
                is_full = self.__board.isfull()
                print("Board Full: ", is_full)
                self.winState()
                if(is_full == False):
                    start_time = time.time()
                    self.__board.print()
                    self.game_step += 1
                    best_situation = float('-inf') # player win
                    # List of position that can be typed of BOT in the next step
                    result = self.__botXAT.possibleMoves(self.__botXAT.play, self.__board) 
                    print("result: ", result)
                    for r in result:
                        self.__botXAT.action(r, self.__board) # Tick the board
                        # Calculate the evaluation value of all possible move
                        eval = self.__botXAT.minimaxAlgorithm(False, self.depth, best_situation, float('inf'), self.__board) 
                        self.__botXAT.backAction(r, self.__board)
                        print("eval: ", eval)
                        # Assign best situation equal to current evaluation value if eval larger than current best situation
                        if(eval > best_situation):
                            best_situation = eval
                            move = r

                    self.__botXAT.action(move, self.__board) # Found the best move
                    end_time = time.time()
                    print("Time BotXAT do move", move , ": ", end_time - start_time)
                    self.winState()
        else:
            midle = int((self.__level-1 )//2)
            move = [midle,midle, self.__botXAT.play]
            self.__botXAT.action(move, self.__board)
            self.game_step += 1
            self.winState()
            self.play = True

    # Check win state
    def winState(self):    
        self.winer, cell1, cell2 =  self.__board.terminalTest()
        self.winer_line = []
        if(self.winer != None):
            self.winer_line = [(self.__cell_size*cell1[1]+self.__cell_center, self.__cell_size*cell1[0]+self.__cell_center), 
                                (self.__cell_size*cell2[1]+self.__cell_center, self.__cell_size*cell2[0]+self.__cell_center)]

    # Draw objects BOT and player
    def drawObject(self):
        if(self.play == False): 
            self.switch = True

        x_img = self.path(IMAGE_X)
        o_img = self.path(IMAGE_0)
        X_player = self.getScaleIamge(x_img, [self.__cell_size] * 2)
        O_player = self.getScaleIamge(o_img, [self.__cell_size] * 2)
        for y, row in enumerate(self.__board.matrix):
            for x, obj in enumerate(row):
                if obj != INF: # O_player if obj == self.__botXAT.play else X_player
                    if(self.switch == True):
                        if obj == self.__botXAT.play:
                            img =  X_player
                        elif obj == self.__player.play:
                            img =  O_player
                    elif(self.switch == False):
                        if obj == self.__player.play:
                            img =  X_player
                        elif obj == self.__botXAT.play:
                            img =  O_player

                    self.game.screen.blit(
                        img, 
                        self.game.vector(x, y) * self.__cell_size
                    )

    # Draw line and notification box when the match has a winner
    def drawWiner(self): 
        if(self.winer != None):
            self.game.drawLine(
                self.winer_line[0][0], self.winer_line[0][1],
                self.winer_line[1][0], self.winer_line[1][1],
                10,
                "red"
            ) 
            if(self.winer == self.__player.play):
                label = self.font.render(f'YOU WIN', True, 'White', 'black')
                self.game.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
                press = self.font.render(f'ENTER To Restart', True, 'red', 'black')
                self.game.screen.blit(press, (WIDTH // 2 - press.get_width() // 2, WIDTH // 4 + 100))
            elif(self.winer == self.__botXAT.play):
                label = self.font.render(f'YOU LOSE', True, 'White', 'black')
                self.game.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
                press = self.font.render(f'ENTER To Restart', True, 'red', 'black')
                self.game.screen.blit(press, (WIDTH // 2 - press.get_width() // 2, WIDTH // 4 + 100))
        elif(self.game_step == self.__level**2):
            label = self.font.render(f'TIE !!', True, 'White', 'black')
            self.game.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, WIDTH // 4))
            press = self.font.render(f'ENTER To Restart', True, 'red', 'black')
            self.game.screen.blit(press, (WIDTH // 2 - press.get_width() // 2, WIDTH // 4 + 100))
        
    def draw(self):
        self.game.drawBoard(self.__level, 600, 0, 0)
        self.drawObject()
        self.drawWiner()
        
    def setLevel(self, level): # 3 5 7
        self.__level = level

    def path(self, file_name):
        file_name = 'assets\\' + file_name
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".") # Return path name

        return os.path.join(base_path, file_name) # Associate a path with file name

    @staticmethod
    def getScaleIamge(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def run(self):
        self.draw()
        self.runGameProcess()

"""
    Data structure Game class to control game
    """
  
class Game:
    def __init__(self):
        """

            """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT)) # Get window with WIDTH, HEIGHT
        self.tic_tac_toe = None
        self.time   = pg.time.Clock() # Set FPS frame
        self.vector =  pg.math.Vector2
        self.font = pg.font.SysFont('Verdana', 20, True) # set font 
        self.max_option = 0 # Number of option in frame level, 
        self.clicked_yes_no = (0,1)
        self.clicked = 0
        self.enter = 0
        self.lev = 3
        self.caption = pg.display.set_caption('TicTacToe -- XAT')

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if(event.key == pg.K_KP_ENTER):
                    self.run()
                if(event.key == pg.K_SPACE):
                    self.enter = self.clicked
                if(event.key == pg.K_UP):
                    if(self.max_option == 3):
                        if(self.clicked == 0):
                            continue
                        self.clicked -= 1
                if(event.key == pg.K_DOWN):
                    if(self.max_option == 3):
                        if(self.clicked ==3):
                            continue
                        self.clicked += 1
                if(event.key == pg.K_LEFT):
                    if(self.max_option == 2):
                        self.clicked = self.clicked_yes_no[0]
                if(event.key == pg.K_RIGHT):
                    if(self.max_option == 2):
                        self.clicked = self.clicked_yes_no[1]

    # Draw line and draw board are visualize the check board
    def drawLine(self, x_start, y_start, x_end, y_end, line_width, line_color):
        pg.draw.line(
            self.screen, 
            line_color, 
            (x_start, y_start), 
            (x_end, y_end), 
            line_width
        )

    def drawBoard(self, length, width_screen, x, y):
        width_rectange = int(width_screen // length)
        current_x = x + width_rectange
        current_y = y + width_rectange

        for i in range(length - 1):
            
            self.drawLine(
                current_x, y + OFFSET, 
                current_x, width_screen - OFFSET,
                10,
                (70,130,180)
            ) 

            self.drawLine(
                x + OFFSET, current_y,
                width_screen - OFFSET, current_y,
                10,
                (70,130,180)
            ) 

            current_x += width_rectange
            current_y += width_rectange

    def drawButtonOut(self, x, y, width, height, text, color):
        pg.draw.rect(
            self.screen,
            color,
            (x, y, width, height)# (x-5, y-5, width+10, height+10)         
        )
        pg.draw.line(self.screen, "white", (x,y), (x+width, y), 2)
        pg.draw.line(self.screen, "white", (x,y), (x, y+height), 2)
        pg.draw.line(self.screen, "white", (x,y+height), (x+width, y+height), 2)
        pg.draw.line(self.screen, "white", (x+width,y), (x+width, y+height), 2)

        label = self.font.render(text, True, 'white')
        text_rect = label.get_rect(center = (x + width/2, y + height/2))
        self.screen.blit(label, text_rect)
        return pg.Rect(x-5, y-5, width+10, height+10)

    def drawBox(self, x, y, width, height, color, line_width):
        pg.draw.line(self.screen, color, (x,y), (x+width, y), line_width)
        pg.draw.line(self.screen, color, (x,y), (x, y+height), line_width)
        pg.draw.line(self.screen, color, (x,y+height), (x+width, y+height), line_width)
        pg.draw.line(self.screen, color, (x+width,y), (x+width, y+height), line_width)

    def drawText(self, x, y, font, text, color): 
        text_font = pg.font.SysFont('Verdana', font, True)
        text_surface = text_font.render(text, True, color)
        text_rect = text_surface.get_rect(center = (x, y))
        self.screen.blit(text_surface, text_rect)

    def drawRectangle(self, x, y, width, height, color):
        pg.draw.rect(
            self.screen,
            color,
            (x, y, width, height)            
        )

    def path(self, file_name):
        file_name = 'assets\\' + file_name
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".") 

        return os.path.join(base_path, file_name) 

    def drawBG(self, path, x, y):
        img = pg.image.load(self.path(path))
        pg.transform.scale2x(img)
        self.screen.blit(
            img, 
            (x,y))

    #Visulize menu screen
    def frameMenu(self):
        self.max_option = 3
        self.clicked = 0
        self.enter = -1
        while True:
            self.drawBG(IMAGE_BG, 0, 0) # Draw background
            #Draw option of different size board
            self.drawText(300, 250, 20,"Please, Choose your board: ", 'white')
            bt1 = self.drawButtonOut(250, 300, 60, 40, "3x3", LINE_COLOR)
            bt2 = self.drawButtonOut(250, 380, 60, 40, "5x5", LINE_COLOR)
            bt3 = self.drawButtonOut(250, 460, 60, 40, "7x7", LINE_COLOR)
            if(self.clicked == 1):
                self.drawButtonOut(250, 300, 60, 40, "3x3", 'red')
                if(self.enter == self.clicked):
                    self.lev = 3
                    self.frameYourPlay(self.lev)
            
            if(self.clicked == 2):
                self.drawButtonOut(250, 380, 60, 40, "5x5", 'red')
                if(self.enter == self.clicked):
                    self.lev = 5
                    self.frameYourPlay(self.lev)
             

            if(self.clicked == 3):
                self.drawButtonOut(250, 460, 60, 40, "7x7", 'red')
                if(self.enter == self.clicked):
                    self.lev = 7
                    self.frameYourPlay(self.lev)
            
            self.checkEvents()
            pg.display.update()
            self.time.tick(60) # the rendering surface and set number of frame per second

    # Another Screen
    def frameYourPlay(self, lev):
        self.enter = -1
        self.clicked = 0
        self.max_option = 2
        self.screen.fill((0, 0, 0))
        while True:
            self.drawBG(IMAGE_BG, 0, 0)
            self.drawText(300, 250, 40,"Do you go first ?", 'white')
            bt1 = self.drawButtonOut(400, 320, 60, 40, "YES", LINE_COLOR)
            bt2 = self.drawButtonOut(150, 320, 60, 40,"NO" ,LINE_COLOR)
            if(self.clicked == 1):
                self.drawButtonOut(400, 320, 60, 40, "YES", 'red')
                if(self.enter == self.clicked):
                    self.lev = lev
                    play = True
                    if(lev == 3):
                        self.frame3x3(play)
                    elif(lev == 5):
                        self.frame5x5(play)
                    elif(lev == 7):
                        self.frame7x7(play)

            if(self.clicked == 0):
                self.drawButtonOut(150, 320, 60, 40,"NO" , 'red')
                if(self.enter == self.clicked):
                    play = False
                    self.lev = lev
                    if(lev == 3):
                        self.frame3x3(play)
                    elif(lev == 5):
                        self.frame5x5(play)
                    elif(lev == 7):
                        self.frame7x7(play)

            self.checkEvents()
            pg.display.update()
            self.time.tick(60) # the rendering surface and set number of frame per second

    # Game on the board size 3x3 
    def frame3x3(self, play):
        self.screen.fill((0,0,0))
        self.tic_tac_toe = TicTacToe(self, self.lev, play)
        # Game run 
        while True:
            self.tic_tac_toe.run() 
            self.checkEvents()
            pg.display.update()
            self.time.tick(60)
            pg.display.update()

    # Game on the board size 5x5 
    def frame5x5(self, play):
        self.tic_tac_toe = TicTacToe(self, self.lev, play)
        self.screen.fill((0, 0, 0))
        # Game run 
        while True:
            self.tic_tac_toe.run() 
            self.checkEvents()
            pg.display.update()
            self.time.tick(60)
            pg.display.update()

    # Game on the board size 7x7
    def frame7x7(self, play):
        self.tic_tac_toe = TicTacToe(self, self.lev, play)
        self.screen.fill((0, 0, 0))
        # Game run 
        while True: 
            self.tic_tac_toe.run() 
            self.checkEvents()
            pg.display.update()
            self.time.tick(60)
            pg.display.update()
            
    def run(self):
        self.enter = -1
        self.clicked = 0
        self.max_option = 2
        self.screen.fill((0, 0, 0))
        while True:
            self.drawBG(IMAGE_BG, 0, 0)
            self.drawText(300, 250, 40,"Do you want to play ?", 'white')
            bt1 = self.drawButtonOut(400, 320, 60, 40, "YES", LINE_COLOR)
            bt2 = self.drawButtonOut(150, 320, 60, 40,"NO" ,LINE_COLOR)
            if(self.clicked == 1):
                self.drawButtonOut(400, 320, 60, 40, "YES", 'red')
                if(self.enter == self.clicked):
                    self.frameMenu()

            if(self.clicked == 0):
                self.drawButtonOut(150, 320, 60, 40,"NO" , 'red')
                if(self.enter == self.clicked):
                    pg.quit()
                    sys.exit()

            self.checkEvents()
            pg.display.update()
            self.time.tick(60) # The rendering surface and set number of frame per second        