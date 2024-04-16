import sys
import math, random, time
import pygame
from pygame.locals import QUIT

pygame.init()
surface = pygame.display.set_mode((850, 600))
pygame.display.set_caption('2048')

# main grid
mgrid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# back-up grid
bgrid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# 字型及大小
font = [pygame.font.Font('my_font.TTF', 200),   # logo
        pygame.font.Font('my_font.TTF', 80),    # text
        pygame.font.Font('my_font.TTF', 100),   # 0, 2, 4, 8
        pygame.font.Font('my_font.TTF', 80),    # 16, 32, 64
        pygame.font.Font('my_font.TTF', 60),    # 128, 256, 512
        pygame.font.Font('my_font.TTF', 40),    # 1024, 2048
        pygame.font.Font(None, 25)] # help

# 文字顏色
f_color = [ '#000000', '#FFFFFF', '#000000', '#000000', '#000000', '#000000', '#000000',
            '#000000', '#000000', '#000000', '#000000', '#000000', '#000000']
# [null, 0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

# 背景顏色
b_color = [ '#00FF00', '#000000', '#00F8FF', '#00FFDB', '#00FFAF', '#00FF83', '#00FF57',
            '#00FF00', '#83FF00', '#AFFF00', '#DBFF00', '#FFF800', '#FFCC00']
# [logo/text, 0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

# 微調數字在方塊的位置
xx = [0, 0, 25, 8, 10, 10]
yy = [0, 0, 0, 12, 20, 20]

mscore = 0 # score
bscore = 0 # back up

mode = 0 # 0 >> start, 1 >> playing, 2 >> win, 3 >> lose

# 顯示畫面
class screen:
    def start():
        logo = font[0].render('2048', True, b_color[0])    
        text = font[1].render('tap to start', True, b_color[0])
        surface.blit(logo, (225, 100))
        surface.blit(text, (205, 350))

    def win():
        global mscore
        score = 'score: ' + str(mscore)
        logo = font[0].render('you win', True, b_color[0])    
        text = font[1].render('tap to restart', True, b_color[0])
        score = font[5].render(score, True, (0, 255, 0))    
        surface.blit(logo, (105, 100))
        surface.blit(text, (165, 400))
        surface.blit(score, (320, 330))

    def lose():
        global mscore
        score = 'score: ' + str(mscore)
        logo = font[0].render('you lose', True, b_color[0])    
        text = font[1].render('tap to restart', True, b_color[0])
        score = font[5].render(score, True, (0, 255, 0))    
        surface.blit(logo, (55, 100))
        surface.blit(text, (165, 400))
        surface.blit(score, (320, 320))

# 方塊動作
class move:
    def undo():
        global mscore, bscore
        mscore = bscore
        for i in range(4):
            for j in range(4):
                mgrid[i][j] = bgrid[i][j]
    def back_up():
        global mscore, bscore
        bscore = mscore
        for i in range(4):
            for j in range(4):
                bgrid[i][j] = mgrid[i][j]
    def spawn():
        b = 0
        while(b == 0):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            t = random.randint(1, 2)
            if(mgrid[x][y] == 0):
                mgrid[x][y] = 2 * t
                b = 1
    def spin(n):
        for k in range(n):
            tmp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            for i in range(4):
                for j in range(4):
                    tmp[4 - j - 1][i] = mgrid[i][j]
            for i in range(4):
                for j in range(4):
                    mgrid[i][j] = tmp[i][j]
    def left():
        # [0, 2, 0, 0] >> [2, 0, 0, 0]
        for i in range(4):
            for j in range(4):
                if(mgrid[i][j] == 0):
                    mgrid[i].remove(mgrid[i][j])
                    mgrid[i].append(0)
        # [2, 2, 0, 0] >> [4, 0, 0, 0]
        for i in range(4):
            for j in range(3):
                if(mgrid[i][j] == mgrid[i][j + 1]):
                    mgrid[i][j] *= 2
                    global mscore
                    mscore += mgrid[i][j]
                    mgrid[i].remove(mgrid[i][j + 1])
                    mgrid[i].append(0)
                    break
    def right():
        move.spin(2)
        move.left()
        move.spin(2)
    def up():
        move.spin(1)
        move.left()
        move.spin(3)
    def down():
        move.spin(3)
        move.left()
        move.spin(1)

# 檢查狀態
class check:
    def isMove():
        for i in range(4):
            for j in range(4):
                if(mgrid[i][j] != bgrid[i][j]):
                    return True
        return False
    
    def canMove():
        # 1. 是否有空方塊
        for i in mgrid:
            for j in i:
                if(j == 0):
                    return True
        # 2. 是否有相鄰且同值的方塊

        # 2-a. 直
        for i in range(4):
            for j in range(4 - 1):
                if(mgrid[i][j] == mgrid[i][j + 1]):
                    return True
        # 2-b. 橫
        for i in range(4 - 1):
            for j in range(4):
                if(mgrid[i][j] == mgrid[i + 1][j]):
                    return True
        return False

# 遊戲畫面
def pt():
    x = 250
    y = 20
    global mscore
    text = 'score: ' + str(mscore)
    text = font[5].render(text, True, (0, 255, 0))    
    surface.blit(text, (20, 50))
    text1 = '     W    '
    text2 = 'A   S   D '
    text3 = '          ^'
    text4 = '<        v         > '
    text1 = font[5].render(text1, True, (0, 255, 0))    
    text2 = font[5].render(text2, True, (0, 255, 0))
    text3 = font[6].render(text3, True, (0, 255, 0))    
    text4 = font[6].render(text4, True, (0, 255, 0))
    surface.blit(text1, (50, 300))
    surface.blit(text2, (50, 340))
    surface.blit(text3, (50, 420))
    surface.blit(text4, (50, 460))
    text = 'u - undo   q - quit'
    text = font[6].render(text, True, (0, 255, 0))
    surface.blit(text, (50, 500))
    for i in mgrid:
        for j in i:
            t = str(j)
            c = int(j)
            c = int(math.log(1 + c, 2)) + 1
            l = len(t) + 1
            pygame.draw.rect(surface, b_color[c], pygame.Rect(x, y, 100, 100))
            t = font[l].render(t, True, f_color[c])
            surface.blit(t, (x + xx[l], y + yy[l]))
            x += 150
        x = 250
        y += 150

while(True):
    surface.fill((0, 0, 0))    
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(mode == 0):
                mode = 1
                move.spawn()
                move.back_up()
            if(mode == 2) | (mode == 3):
                mgrid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                mscore = 0
                move.spawn()
                move.back_up()
                mode = 1
        if(event.type == pygame.KEYDOWN):
            if(event.unicode == 'q'): mode = 0
            if(event.unicode == 'u'):
                move.undo()
                mode = 1
            if(mode == 1) & (check.canMove() == True):
                move.back_up()
                if(event.unicode == 'w') | (event.key == pygame.K_UP):
                    move.up()
                    if(check.isMove() == True): move.spawn()
                if(event.unicode == 'a') | (event.key == pygame.K_LEFT):
                    move.left()
                    if(check.isMove() == True): move.spawn()
                if(event.unicode == 's') | (event.key == pygame.K_DOWN):
                    move.down()
                    if(check.isMove() == True): move.spawn()
                if(event.unicode == 'd') | (event.key == pygame.K_RIGHT):
                    move.right()
                    if(check.isMove() == True): move.spawn()
        if(event.type == QUIT):
            pygame.quit()
            sys.exit()
    if(mode == 0): screen.start()
    if(mode == 1):
        if(check.canMove() == True): pt()
        else:
            time.sleep(1)
            mode = 3
    for i in mgrid:
        for j in i:
            if(j == 2048):
                mode = 2
    if(mode == 2): screen.win()
    if(mode == 3): screen.lose()
    pygame.display.update()

