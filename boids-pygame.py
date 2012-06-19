from random import *
from math   import *
from pygame.locals import *
import pygame

#size(320,180)
WIDTH=640
HEIGHT=360
screen = pygame.display.set_mode((WIDTH,HEIGHT),0,24)
#speed(20)


boids=[]
dt = 2.0 #/30
v0 = 3.0

for i in range(0,30):
    boids.append([WIDTH*random(),HEIGHT*random(),150.0,v0*(random()-0.5),v0*(random()-0.5),random()-0.5])



def snapshot(boids):
    #colormode(HSB)
    bgcolor = pygame.Color(0)
    bgcolor.hsva = (0.666*360, 0.7*100, 0.5*100)
    screen.fill(bgcolor)
    #background(0.666,0.7,0.5)
    #strokewidth(4)
    linecolor = pygame.Color(0)
    for x,y,z,vx,vy,vz in boids:
    	b =  (1-abs(vz/v0))*100
    	if b < 0:
    		b = 0
    	elif b > 100:
    		b = 100
        linecolor.hsva = (0.6*360, 0.4*100, b)
        #stroke(0.6, 0.4, 1-abs(vz/v0))
        #strokewidth( z / 60.0 )
        #line(x,y,x-vx*5,y-vy*5)
        pygame.draw.line(screen, linecolor, map(int,(x,y)), map(int,(x-vx*5,y-vy*5)), int(z / 60.0))
    pygame.display.flip()
    pygame.time.wait(20)



def proceed(boids, dt, v0):
    newboids = []
    for i in range(0,len(boids)):
        x,y,z,vx,vy,vz = boids[i]
        #find the nearest one
        avx,avy,avz = 0.0, 0.0, 0.0
        rvx,rvy,rvz = 0.0, 0.0, 0.0
        svx,svy,svz = 0.0, 0.0, 0.0
        ns,na,nr    = 0.0, 0.0, 0.0
        for j in range(0,len(boids)):
            if j != i:
                dx = x - boids[j][0]
                dy = y - boids[j][1]
                dz = z - boids[j][2]
                rr = dx**2 + dy**2 + dz**2
                r = sqrt(rr)
                ar = 20.0
                if r < ar:
                    rvx += dx/(ar * (r/ar))
                    rvy += dy/(ar * (r/ar))
                    rvz += dz/(ar * (r/ar))
                    nr  += 1.0
                if r < 25.0:
                    svx += boids[j][3]
                    svy += boids[j][4]
                    svz += boids[j][5]
                    ns  += 1.0
                elif r < 60.0:
                    avx += dx/r
                    avy += dy/r
                    avz += dz/r
                    na  += 1.0
        if na > 0.0:
            na *= 4.0
            vx -= avx / na
            vy -= avy / na
            vz -= avz / na
        if nr > 0.0:
            vx += rvx / nr
            vy += rvy / nr
            vz += rvz / nr
        if ns > 0.0:
            ns *= 30.0
            vx += svx / ns 
            vy += svy / ns
            vz += svz / ns
        #Attractive force
        #if 3000.0 <  rrmin < 10000.0:
        #    dx = x - boids[min][0]
        #    dy = y - boids[min][1]
        #    dz = z - boids[min][2]
        #    r  = sqrt( dx**2 + dy**2 + dz**2 )
        #    vx = vx - dx/r
        #    vy = vy - dy/r
        #    vz = vz - dz/r
        #Centroidal force
        #dx = x - WIDTH/2
        #dy = y - HEIGHT/2
        #dz = z
        #r  = sqrt( dx**2 + dy**2 + dz**2 )
        #if r > 100.0:
        #    vx = vx - dx/r
        #    vy = vy - dy/r
        #    vz = vz - dz/r
                    
        v = sqrt(vx**2 + vy**2 + vz**2)
        if v > v0:
            vx = vx/v * v0
            vy = vy/v * v0
            vz = vz/v * v0
        x  = x + vx * dt
        y  = y + vy * dt
        z  = z + vz * dt
        vg = 0.5
        if x < 50.0:
            vx += vg
        if WIDTH-50.0 < x:
            vx -= vg
        if y < 50.0:
            vy += vg
        if HEIGHT-50.0 < y:
            vy -= vg
        if z < 100.0:
            vz += vg
        if 300.0 < z:
            vz -= vg
        newboids.append([x,y,z,vx,vy,vz])
    return newboids

def draw():
    global boids, dt, v0
    boids = proceed(boids, dt, v0)
    snapshot(boids)    

while True:
    draw()
    pygame.event.get()
    pressed = pygame.key.get_pressed()
    if pressed[K_q]:
        break
	