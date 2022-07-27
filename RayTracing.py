import pygame as pg
#from pygame.locals import *
import math
import pickle

f=open("wmap.txt",'rb')
obj=pickle.load(f)
f.close()
width=obj[0]
height=obj[1]
wmap=obj[2]

dist=[]
delay=50

win=pg.display.set_mode((2*width,height))
mapx=0
mapy=0
man_range=120*math.pi/180
vision_range=20/180 *math.pi
vision_lines=250

n_X=len(wmap[0])
n_Y=len(wmap)
l=width/n_X
b=height/n_Y

vision_lines=200
vision_range=40
vision_rad=0
min_r1=4000
min_r2=4000
r=5000
X=0
Y=0
p=1
hor_angle=30*math.pi/180
player_x=3*l + 10
player_y=3*b + 10
player_v=4
run=True
while run==True:
    dist=[]
    win.fill((0,0,0))
    pg.time.delay(delay)
    mousex,mousey=pg.mouse.get_pos()
    mouse_rad=mousex/width * 3*math.pi
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run= False
    keys=pg.key.get_pressed()
    if keys[pg.K_w]:
        if wmap[int((player_y+2)/b)][int(player_x/l)]==0:
            player_x=player_x+player_v*math.cos(mouse_rad)
            player_y=player_y+player_v*math.sin(mouse_rad)
        else:
            player_x=player_x-player_v*math.cos(mouse_rad)*2
            player_y=player_y-player_v*math.sin(mouse_rad)*2
    if keys[pg.K_s]:
        if wmap[int((player_y-2)/b)][int(player_x/l)]==0:
            player_x=player_x-player_v*math.cos(mouse_rad)
            player_y=player_y-player_v*math.sin(mouse_rad)
        else:
            player_x=player_x+player_v*math.cos(mouse_rad)*2
            player_y=player_y+player_v*math.sin(mouse_rad)*2
    if keys[pg.K_a]:
        if wmap[int(player_y/b)][int((player_x-2)/l)]==0:
            player_x=player_x-player_v
        else:
            player_x=player_x+2*player_v+2
    if keys[pg.K_d]:
        if wmap[int(player_y/b)][int((player_x+2)/l)]==0:
            player_x=player_x+player_v
        else:
            player_x=player_x-2*player_v-2
            
    if keys[pg.K_q]:
        run=False
    for y_line in range(0,n_Y):
        for x_line in range(0,n_X):
            if wmap[y_line][x_line]==1:
                pg.draw.rect(win,(0,0,255),(x_line*l,y_line*b,l,b))
            if wmap[y_line][x_line]==2:
                pg.draw.rect(win,(255,0,0),(x_line*l,y_line*b,l,b))
            if wmap[y_line][x_line]==3:
                pg.draw.rect(win,(0,255,0),(x_line*l,y_line*b,l,b))
            if wmap[y_line][x_line]==4:
                pg.draw.rect(win,(255,255,0),(x_line*l,y_line*b,l,b))
            if wmap[y_line][x_line]==5:
                pg.draw.rect(win,(0,255,255),(x_line*l,y_line*b,l,b))
            if wmap[y_line][x_line]==6:
                pg.draw.rect(win,(255,0,255),(x_line*l,y_line*b,l,b))
        pg.draw.line(win, (25,25,25), (0,y_line*b), (width, y_line*b), 2)
    for x_line in range(0,n_X+1):
        pg.draw.line(win, (25,25,25), (x_line*l,0), (x_line*l, height), 2)
    pg.draw.line(win,(255,255,0),(player_x,player_y),(player_x+10*math.cos(mouse_rad),player_y+10*math.sin(mouse_rad)),3)
    pg.draw.line(win,(255,255,255),(player_x-10*math.sin(mouse_rad),player_y+10*math.cos(mouse_rad)),(player_x+10*math.sin(mouse_rad),player_y-10*math.cos(mouse_rad)),3)
    for i in range(0,vision_lines):
        vision_rad=mouse_rad-(vision_range*math.pi/360)+(i*vision_range/vision_lines)*math.pi/180
        r=0
        X_=player_x
        Y_=player_y
        step=1
        condition=True
        while condition==True:
            X_=X_+step*math.cos(vision_rad)
            Y_=Y_+step*math.sin(vision_rad)
            r=r+step
            if not (wmap[int(Y_/b)][int(X_/l)]==0):
                dist.append([r,vision_rad,wmap[int(Y_/b)][int(X_/l)]])
                pg.draw.line(win,(0,180,0),(player_x,player_y),(player_x+r*math.cos(vision_rad),player_y+r*math.sin(vision_rad)),1)   
                condition=False
    X=width
    for j in range(0,vision_lines):
        i=vision_lines-j-1
        r=dist[i][0]
        diagonal=((width)**2+(height)**2)**0.5
        g=250-(r**(0.5)-0)*(250-10)/(diagonal**0.5-0)
        m=l/2
        bl=l
        
        block=0
        ground=0
        sky=0
        
        vis=20*math.pi/180
        if r<m/math.tan(vis):
            block=2*vis
            sky=0
            ground=0
        else:
            block=math.atan(m/r)+math.atan((bl-m)/r)
            ground=vis-math.atan(m/r)
            sky=2*vis-block-ground
        pg.draw.rect(win,(120,204,204),(X+i*width/vision_lines,0,width/vision_lines,(sky/(2*vis)*height)))
        pg.draw.rect(win,(120,120,120),(X+i*width/vision_lines,(sky+block)/(2*vis)*height,width/vision_lines,(ground/(2*vis)*height)))
        if dist[i][2]==1:          
            #pg.draw.line(win,(0,0,g),(X+i*width/vision_lines-(width/vision_lines)/2,sky/(2*vis)*height),(X+i*width/vision_lines-(width/vision_lines)/2,(sky/(2*vis)*height)+(block/(2*vis)*height)),int(width/vision_lines))
            pg.draw.rect(win,(0,0,g),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))
        if dist[i][2]==2:
            pg.draw.rect(win,(g,0,0),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))
        if dist[i][2]==3:
            pg.draw.rect(win,(0,g,0),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))
        if dist[i][2]==4:
            pg.draw.rect(win,(g,g,0),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))
        if dist[i][2]==5:
            pg.draw.rect(win,(0,g,g),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))   
        if dist[i][2]==6:
            pg.draw.rect(win,(g,0,g),(X+i*width/vision_lines,sky/(2*vis)*height,width/vision_lines,(block/(2*vis)*height)))    
    pg.display.update()
pg.quit()       
        
              