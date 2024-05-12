import sys
import pygame
from pygame.locals import QUIT
import random

pygame.init()
window_surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('1A2B')
window_surface.fill((0,0,0))
font = pygame.font.Font(None, 32)


g1="\"1 A 2 B\":"
g2="      1 number is correct and in the right place"
g3="      2 numbers are correct but in the wrong place"
g4="for example:"
g5="      the answer is \"1234\","
g6="      and the input is \"2345\","
g7="      it will be \"0 A 3 B\""

ans=random.sample(range(0,9),4)
def check_a(player,ans):
    n=0
    a=0
    while(n<4):
        if(player[n]==ans[n]):
            a+=1
        n+=1
    return a;

def check_b(player,ans):
    n=0
    b=0
    while(n<4):
        if(player[n] in ans)&(player[n]!=ans[n]):
            b+=1
        n+=1
    return b;

def game():
    k=int(text)
    player=[k//1000,k%1000//100,k%100//10,k%10]
    if(int(check_a(player,ans))<4):
        return(check_a(player,ans),check_b(player,ans))
    else:
        return(5,5)

text = ""
input_box = pygame.Rect(100, 100, 100, 32)
#sq=pygame.image.load('square.png').convert_alpha()
#sq=pygame.transform.scale(sq,(100,32))
n0=pygame.image.load('0.png').convert_alpha()
n0=pygame.transform.scale(n0,(150,150))
n1=pygame.image.load('1.png').convert_alpha()
n1=pygame.transform.scale(n1,(50,150))
n2=pygame.image.load('2.png').convert_alpha()
n2=pygame.transform.scale(n2,(150,150))
n3=pygame.image.load('3.png').convert_alpha()
n3=pygame.transform.scale(n3,(150,150))
n4=pygame.image.load('4.png').convert_alpha()
n4=pygame.transform.scale(n4,(150,150))
a=pygame.image.load('A.png').convert_alpha()
a=pygame.transform.scale(a,(150,150))
b=pygame.image.load('B.png').convert_alpha()
b=pygame.transform.scale(b,(150,150))
logo=pygame.image.load('logo.png').convert_alpha()
logo=pygame.transform.scale(logo,(400,200))
st=pygame.image.load('start.png').convert_alpha()
st=pygame.transform.scale(st,(500,100))
win=pygame.image.load('win.png').convert_alpha()
win=pygame.transform.scale(win,(500,100))

mode=0
nA=0
nB=0
while True:
    window_surface.fill((0,0,0))
    text_surface = font.render(text, True,(255,255,255))
    window_surface.blit(text_surface,(445, 300))
    #t = font.render("press \"h\" to help", True,(255,255,255))
    #window_surface.blit(t,(320, 525))
    if(mode==1):
        window_surface.blit(win,(150,200))
    elif(mode==0):
        window_surface.blit(logo,(200,100))
        window_surface.blit(st,(150,400))
    elif(mode==2):
        #window_surface.blit(sq,(360, 350))
        in_ = font.render("input 4 numbers: ____", True,(255,255,255))
        g1_ = font.render(g1, True,(255,255,255))
        window_surface.blit(g1_,(100, 365))
        g2_ = font.render(g2, True,(255,255,255))
        window_surface.blit(g2_,(100, 390))
        g3_ = font.render(g3, True,(255,255,255))
        window_surface.blit(g3_,(100, 415))
        g4_ = font.render(g4, True,(255,255,255))
        window_surface.blit(g4_,(100, 440))
        g5_ = font.render(g5, True,(255,255,255))
        window_surface.blit(g5_,(100, 465))
        g6_ = font.render(g6, True,(255,255,255))
        window_surface.blit(g6_,(100, 490))
        g7_ = font.render(g7, True,(255,255,255))
        window_surface.blit(g7_,(100, 515))
        
        window_surface.blit(in_,(260, 300))
        window_surface.blit(a,(250,100))
        window_surface.blit(b,(600,100))
        if(nA==0):
            window_surface.blit(n0,(80,100))
        elif(nA==1):
            window_surface.blit(n1,(130,100))
        elif(nA==2):
            window_surface.blit(n2,(80,100))
        elif(nA==3):
            window_surface.blit(n3,(80,100))
        elif(nA==4):
            window_surface.blit(n4,(80,100))
        if(nB==0):
            window_surface.blit(n0,(430,100))
        elif(nB==1):
            window_surface.blit(n1,(480,100))
        elif(nB==2):
            window_surface.blit(n2,(430,100))
        elif(nB==3):
            window_surface.blit(n3,(430,100))
        elif(nB==4):
            window_surface.blit(n4,(430,100))
    pygame.display.update()
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN)&(mode==2):
            if(len(text)==4)|(event.key == pygame.K_RETURN):
                (nA,nB)=game()
                if(nA,nB)==(5,5):
                    mode=1
                text = ""
            elif(event.key == pygame.K_BACKSPACE):
                text = text[:-1]
            else:
                if('0'<=event.unicode<='9'):
                    text += event.unicode
        if(event.type == pygame.MOUSEBUTTONDOWN)&(mode!=1):
            window_surface.fill((0,0,0))
            mode=2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
