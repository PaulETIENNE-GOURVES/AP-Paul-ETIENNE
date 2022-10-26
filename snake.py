import pygame as pg
import random as rd
import sys


pg.init()
screen = pg.display.set_mode((600, 600))
checker_index = []
for i in range(30):
    for j in range(30):
        if (i + j) % 2 == 0:
            checker_index.append([i, j])
clock = pg.time.Clock()


width = 20
height = 20

color_snake = (100,0,255)
color_fruit = (255,100,0)

serpent = [[10,15],[11,15],[12,15],[13,15]]
direction = [1,0]
fruit = [10,10]
score = 0

# on rajoute une condition à la boucle: si on la passe à False le programme s'arrête
running = True
while running:
    clock.tick(3)
    # on itère sur tous les évènements qui ont eu lieu depuis le précédent appel
    # ici donc tous les évènements survenus durant la seconde précédente
    for event in pg.event.get():
        # chaque évênement à un type qui décrit la nature de l'évênement
        # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
        if event.type == pg.QUIT:
            running = False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False
            if event.key == pg.K_UP and direction!=[0,1] :
                direction = [0,-1]
            if event.key == pg.K_DOWN and direction!=[0,-1] :
                direction = [0,1]
            if event.key == pg.K_LEFT and direction!=[1,0] :
                direction = [-1,0]
            if event.key == pg.K_RIGHT and direction!=[-1,0] :
                direction = [1,0]
    tete = [serpent[-1][0]+direction[0],serpent[-1][1]+direction[1]]

    #autocollision
    if tete in serpent[:-1]:
        running = False
        print(f"Game over ! Self-bite \nScore : {score}")

    #traversée murs
    if tete[0] > 29:
        tete = [0, tete[1]]
    elif tete[0] < 0:
        tete = [29, tete[1]]
    elif tete[1] > 29:
        tete = [tete[0], 0]
    elif tete[1] < 0:
        tete = [tete[0], 29]


    serpent.append(tete)


    if tete != fruit:
        serpent.pop(0)
    else:
        fruit[0] = rd.randint(0,29)
        fruit[1] = rd.randint(0,29)
        score +=1
    

    #dessin du fond d'écran
    screen.fill((150,200,0))
    for pos in checker_index:
        case = pg.Rect(pos[0]*20, pos[1]*20, width, height)
        pg.draw.rect(screen, (200, 255, 0), case)

    #dessin du fruit
    rect_fruit = pg.Rect(fruit[0]*20, fruit[1]*20, width, height)
    pg.draw.rect(screen, color_fruit, rect_fruit)

    #dessin du serpent
    for pos in serpent:
        rect = pg.Rect(pos[0]*20, pos[1]*20, width, height)
        pg.draw.rect(screen, color_snake, rect)
    

    pg.display.update()
    pg.display.set_caption(f"🐍 Score: {score}")

pg.quit()