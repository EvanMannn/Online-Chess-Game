'''
the main game
author:@techwithtim
requirements:see requirements.txt
'''

import subprocess
import sys
import get_pip

def install(package):
    '''
    Installs pip
    '''
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")


import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()

board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))

origin = (113, 113)
boardSize = (525,525)

turn = "w"


def menu_screen(win):
    '''
    Display the menu screen\n
    \t - win (pygame window object): window that the menu is displayed in
    '''
    global bo, chessbg

    menuFontSize = 50
    menuFontColour = (255, 0, 0)
    menuTextHeight = 500

    run = True
    offline = False

    while run:
        win.blit(chessbg, (0,0))
        small_font = pygame.font.SysFont("comicsans", menuFontSize)
        
        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, menuFontColour)
            win.blit(off, (width / 2 - off.get_width() / 2, menuTextHeight))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True


    
def redraw_gameWindow(win, bo, p1, p2, color, ready):
    '''
    Function to redraw the current state of the pygame window\n
    \t\n - win (pygame Window object): Window showing the game itself
    \t\n - bo (Board object): Chess board object holding references to all the pieces
    \t\n - p1 (int): Time left for player 1 in seconds
    \t\n - p2 (int): Time left for player 2 in seconds
    \t\n - color (char): Color of piece whos turn it is
    \t\n - ready (bool): Whether or not both players are ready for the game to begin
    '''
    #Font sizes
    fontSize = 30
    largeFontSize = 80

    #Font colours
    timerFontColour = (255, 255, 255)
    quitTextFontColour = (255, 255, 255)
    spectatorLabelFontColour = (255, 0, 0)
    playerFontColour = (255, 0, 0)

    #Text positions
    p1TimerPos = (520,10)
    p2TimerPos = (520, 700)
    quitTextPos = (10, 20)

    #Center alligned text hieghts
    playerModeTextHeight = 10
    playerTurnTextHeight = 700
    waitingTextHeight = 300


    win.blit(board, (0, 0))
    bo.draw(win, color)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", fontSize)
    try:
        txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, timerFontColour)
        txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, timerFontColour)
    except Exception as e:
        print("EXCEPTION: Error rendering the fonts for the time remaining for each player")
        print(e)
    win.blit(txt, p1TimerPos)
    win.blit(txt2, p2TimerPos)

    txt = font.render("Press q to Quit", 1, quitTextFontColour)
    win.blit(txt, quitTextPos)

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, spectatorLabelFontColour)
        win.blit(txt3, (width/2-txt3.get_width()/2, playerModeTextHeight))

    if not ready:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", largeFontSize)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, waitingTextHeight))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", fontSize)
        if color == "w":
            txt3 = font.render("YOU ARE WHITE", 1, playerFontColour)
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, playerModeTextHeight))
        else:
            txt3 = font.render("YOU ARE BLACK", 1, playerFontColour)
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, playerModeTextHeight))

        if bo.turn == color:
            txt3 = font.render("YOUR TURN", 1, playerFontColour)
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, playerTurnTextHeight))
        else:
            txt3 = font.render("THEIR TURN", 1, playerFontColour)
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, playerTurnTextHeight))

    pygame.display.update()


def end_screen(win, text):
    '''
    Function to display the end screen after the game finishes\n
    \t - text (string): Text to display showing who won
    '''
    fontSize = 80
    fontColour = (255, 0, 0)
    timeOut = 3000
    textHeight = 300

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", fontSize)
    txt = font.render(text,1, fontColour)
    win.blit(txt, (width / 2 - txt.get_width() / 2, textHeight))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, timeOut)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    """
    Function handling a click somewhere on the board to detect which sqaure was selected\n
    \t - pos (int tuple): 2D tuple containing the position in the window that was clicked\n
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if origin[0] < x < origin[0] + boardSize[0]:
        if origin[1] < y < origin[1] + boardSize[1]:
            divX = x - origin[0]
            divY = y - origin[1]
            i = int(divX / (boardSize[0]/8))
            j = int(divY / (boardSize[1]/8))
            return i, j

    return -1, -1


def connect():
    '''
    :returns: Board object shared by the network hosting the chess game
    '''
    global n
    n = Network()
    return n.board


def main():
    '''
    Main function for running the game itself
    '''
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print("EXCEPTION: A player has left the game \nEnding the game...")
            print(e)
            end_screen(win, "Other player left")
            run = False
            break

        if not color == "s":
            if p1Time <= 0:
                bo = n.send("winner b")
            elif p2Time <= 0:
                bo = n.send("winner w")

            if bo.check_mate("b"):
                bo = n.send("winner b")
            elif bo.check_mate("w"):
                bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(win, "White is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "Black is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    # quit game
                    if color == "w":
                        bo = n.send("winner b")
                    else:
                        bo = n.send("winner w")

                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")


            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
    
    n.disconnect()
    bo = 0
    menu_screen(win)


width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
menu_screen(win)
