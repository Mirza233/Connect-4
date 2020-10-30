#!/usr/bin/env python3

import pygame as py
import numpy as np

py.init()
font = py.font.Font("freesansbold.ttf", 18)
grey, white, blue = (100, 100, 100), (255, 255, 255), (0, 0, 255)

player, w, h = 1, 805, 600
window = py.display.set_mode((w, h+80))

color = [(255, 255, 255), (139, 0, 0), (255, 255, 0)]
#board = np.zeros((6,7), int)

new_game_button = py.Rect(0,0, 120, 75)
win_button = py.Rect(120, 0, w-120, 75)
bl = py.Rect(120, 0, w-120, 75)
buttons =[py.Rect(i*w//7 + 7, h+10, 100, 60) for i in range(7)]

new_game_button_text = font.render("New GAME", True, white)
win_disp = new_game_button_text.get_rect(center = (120+(w-120)//2, 37))
new_game_disp = new_game_button_text.get_rect(center = (60, 37))

screen = py.Rect(0, 75, w, h-75)

game_over = False

def draw():
    """
        Draw the new game button
    """
    py.draw.rect(window, grey, new_game_button)
    window.blit(new_game_button_text, new_game_disp)
    py.draw.rect(window, blue, screen)

    py.draw.rect(window, (0, 0, 0), bl)
    """
        Draw the game screen
    """
    py.draw.rect(window, blue, screen)
    for i in range(6):
        py.draw.line(window, (0, 0, 0), ((i+1)*(w//7), 75), ((i+1)*(w//7), h))
    for i in range(5):
        py.draw.line(window, (0, 0, 0), (0, (i+1)*(h-75)//6+75), (w, (i+1)*(h-75)//6+75))
    for i in range(7):
        for j in range(6):
            draw_circle(color[board[j][i]], (int((i+0.5)*(w//7)),int((j+0.5)*((h-75)//6))+75))

    for button in buttons:
        py.draw.rect(window, grey, button)

    py.display.update()


def win(wld, player):
    global game_over
    game_over = True
    py.draw.rect(window, grey, new_game_button)
    window.blit(new_game_button_text, new_game_disp)
    py.draw.rect(window, blue, screen)

    win_message = "DRAW" if wld == -1 else "{} wins!!".format(["", "RED", "YELLOW"][player])
    win_text = font.render(win_message, True, (0, 0, 0))
    py.draw.rect(window, color[player] if wld != -1 else grey, win_button)
    window.blit(win_text, win_disp)
    py.draw.rect(window, blue, screen)

    py.draw.rect(window, blue, screen)
    for i in range(6):
        py.draw.line(window, (0, 0, 0), ((i+1)*(w//7), 75), ((i+1)*(w//7), h))
    for i in range(5):
        py.draw.line(window, (0, 0, 0), (0, (i+1)*(h-75)//6+75), (w, (i+1)*(h-75)//6+75))
    for i in range(7):
        for j in range(6):
            draw_circle(color[board[j][i]], (int((i+0.5)*(w//7)),int((j+0.5)*((h-75)//6))+75))
    py.display.update()

def newGame():
    global board
    global game_over
    game_over = False
    board = np.zeros((6, 7), dtype = int)
    player = 1
    draw()
def update(ind, igrac):
    i = 5
    changed = False
    while i >= 0:
        if board[i][ind] == 0:
            board[i][ind] = igrac
            changed = True
            break
        i-=1
    if not changed:
        return False
    draw()
    return True

def draw_circle(color, center):
    py.draw.circle(window, color, center, w//7-80)


def checkWin(player):
    zerofound = False
    for i in range(7):
        for j in range(6):
            if board[j][i] == 0:
                zerofound = True
    for i in range(6):
        for j in range(7):
            if board[i][j] == player:
                k = 0
                while k <= 3 and (i+k < 6 and board[i+k][j] == player):
                    k+=1
                if k == 4: return 1
                k = 0
                while k <= 3 and (j+k < 7 and board[i][j+k] == player):
                    k+=1
                if k == 4: return 1
                k = 0
                while k <= 3 and (j+k < 7 and i+k<6 and board[i+k][j+k] == player):
                    k+=1
                if k == 4: return 1
                k = 0
                while k <= 3 and (j+k < 7 and i-k >= 0 and board[i-k][j+k] == player):
                    k+=1
                if k == 4: return 1
                k = 0
                while k <= 3 and (i+k < 6 and j-k >= 0 and board[i+k][j-k] == player):
                    k+=1
                if k == 4: return 1
    if not zerofound: return -1
    return 0

def main():
    player = 1
    pl = [0, "RED", "YELLOW"]
    newGame()
    while True:
        mouseClicked = False
        for event in py.event.get():
            if event.type == py.QUIT:
                return
            if event.type == py.MOUSEBUTTONUP:
                mouseClicked = True
                pos_click = event.pos
        if mouseClicked:
            if new_game_button.collidepoint(pos_click):
                newGame()
            elif not game_over:
                for i, button in enumerate(buttons):
                    if button.collidepoint(pos_click):
                        if update(i, player):
                            wld = checkWin(player)
                            if wld == 1:
                                win(wld, player)
                                break
                            elif wld == -1:
                                win(wld, player)
                                break
                            player = 1 if player == 2 else 2
                            break


if __name__ == '__main__':
    main()
