import pygame
import numpy as np
import solver
import Object
import threading


pygame.init()

width, height = (1920, 1080)
base_screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock() 

object_list= []

def createNewObject(pos,aceleration,radius,color=(255,255,255)):
    object_list.append(Object.Object(np.array(pos,dtype=float),np.array(aceleration),radius,color))


def drawObjects(screen):
    for i in object_list:
        pygame.draw.circle(screen,i.color,(i.position),i.radius)


def drawInfo(screen):
    data = (Solver_fc.infoGet())
    for i , z in enumerate(data):
        GAME_FONT.render_to(screen, (1300, 200+(i*50)),str(z), (0, 0, 0))

    GAME_FONT.render_to(screen, (1300, 100),"Fps: " + str(round(clock.get_fps())), (255, 0, 0))


def drawEcene(screen):
    base_screen.fill((255,255,255))
    pygame.draw.circle(screen,(0,0,0),(500,500),400)


def siguiente_color_RGB(color):
    r, g, b = color

    if r == 255 and g < 255 and b < 256:
        g+=15
    elif r <= 255 and g == 255 and b < 256 and r > 0:
        r-=15
    elif r == 0 and g == 255 and b < 255:
        b+=15
    elif b == 255 and r == 0 and g>0:
        g-=15
    elif g == 0 and b == 255 and r < 255:
        r+=15

    
    
    return (r, g, b)

Solver_fc = solver.Solver(object_list,10)
GAME_FONT = pygame.freetype.Font("DS-DIGI.TTF", 24)


createNewObject([500,500],[0,0],10)

#createNewObject([500,550],[0,0],20)
run = True
Lock = False
random_color = (255,0,0)
counter = 0

def permaUpdate():
    while True:
        Solver_fc.update(0.01)

#UpdateThread = threading.Thread(target=permaUpdate, daemon=True)
#UpdateThread.start()



while run:
    counter+=10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        '''
       if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            pass
            # mouse_pos = pygame.mouse.get_pos()
            #createNewObject(mouse_pos,[0,0],random.randint(5,50))

            #object_list.append(Object.Object(np.array(mouse_pos),np.array([0,0])))
            #object_list[0].setPosition(np.array(mouse_pos))
    
    if event.type == pygame.MOUSEBUTTONDOWN and not Lock:
        Lock = True
        
    
    if Lock == True:
        if event.type == pygame.MOUSEBUTTONUP :
            mouse_pos = pygame.mouse.get_pos()
            l = siguiente_color_RGB(random_color)
            random_color = l
            print(random_color)
            createNewObject(mouse_pos,[0,0],10,random_color)
            Lock = False
        '''
    if counter%200 == 0:
        l = siguiente_color_RGB(random_color)
        random_color = l
        createNewObject([600,500],[0,0],20,random_color)

    
    
    drawEcene(base_screen)
    drawObjects(base_screen)
    drawInfo(base_screen)
    

    dt = clock.tick(60)
  
    Solver_fc.update(0.05)
    #Solver_fc.update(0.01)
    #Solver_fc.update(0.05)
    pygame.display.flip()
    