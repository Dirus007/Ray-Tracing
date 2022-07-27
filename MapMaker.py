import pygame as pg
#from pygame.locals import *
import math
import pickle

width=800
height=800
wmap=[]
n_X=64
n_Y=64
l=width/n_X
b=height/n_Y
a=0
win=pg.display.set_mode((width+2,height+2),0,32)
run=True
delay=20

for Y in range(0,n_Y):
    y_line=[]
    for X in range(0,n_X):
        y_line.append(0)
    wmap.append(y_line)

while run==True:
    pg.time.delay(delay)
    win.fill((0,0,0))
    keys=pg.key.get_pressed()
    mousex,mousey=pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run= False
    if keys[pg.K_q]:
        run=False
    if mousex>0 and mousex<width and mousey>0 and mousey<height:
        if keys[pg.K_LSHIFT]:
            if keys[pg.K_0]:
                a=0
            if keys[pg.K_1]:
                a=1
            if keys[pg.K_2]:
                a=2
            if keys[pg.K_3]:
                a=3
            if keys[pg.K_4]:
                a=4
            if keys[pg.K_5]:
                a=5
            if keys[pg.K_6]:
                a=6
            wmap[int(mousey/b)][int(mousex/l)]=a
    for y in range(0,n_Y):
        for x in range(0,n_X):
            if wmap[y][x]==0:
                pg.draw.rect(win,(0,0,0),(x*l,y*b,l,b))  #black
            if wmap[y][x]==1:
                pg.draw.rect(win,(0,0,255),(x*l,y*b,l,b))  #blue
            if wmap[y][x]==2:
                pg.draw.rect(win,(255,0,0),(x*l,y*b,l,b))  #red
            if wmap[y][x]==3:
                pg.draw.rect(win,(0,255,0),(x*l,y*b,l,b))  #green
            if wmap[y][x]==4:
                pg.draw.rect(win,(255,255,0),(x*l,y*b,l,b)) #yellow
            if wmap[y][x]==5:
                pg.draw.rect(win,(0,255,255),(x*l,y*b,l,b))  #cyan
            if wmap[y][x]==6:
                pg.draw.rect(win,(255,0,255),(x*l,y*b,l,b))  #pink
            
                
    for X in range(0,n_X+2):
        pg.draw.line(win,(255,255,255),(X*l,0),(X*l,height),2)
    for Y in range(0,n_Y+2):
        pg.draw.line(win,(255,255,255),(0,Y*b),(width,Y*b),2)  
    pg.display.update()
pg.quit()
f=open("wmap.txt",'wb')
pickle.dump([width,height,wmap],f)
f.close()
    
    