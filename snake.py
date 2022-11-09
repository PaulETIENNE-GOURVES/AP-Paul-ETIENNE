import pygame as pg
import random as rd
import sys


pg.init()

#tailles des carrés
width = 20
height = 20

#couleurs 
color_snake = (100, 0, 255)
color_fruit = (255, 100, 0)

#position des items
serpent = [[10, 15], [11, 15], [12, 15], [13, 15]]
direction = [1, 0]
fruit = [10, 10]
score = 0

#liste des coordonnées pour tracer le damier en arrière-plan
checker_index = []
for i in range(30):
    for j in range(30):
        if (i + j) % 2 == 0:
            checker_index.append([i, j])

running = True # True tant que le programme tourne
bot = False # True quand le bot est activé

# Définition de fonctions annexe pour le bot 
def signe(x):
    '''Renvoie -1 si x négatif et +1 si x positif'''
    if x >= 0:
        return 1
    elif x < 0:
        return -1

def opp(dir):
    '''Renvoie la direction opposée'''
    if dir == [1, 0]:
        return [-1, 0]
    elif dir == [-1, 0]:
        return [1, 0]
    elif dir == [0, 1]:
        return [0, -1]
    elif dir == [0, -1]:
        return [0, 1]

def dir_bot(serpent, direction, fruit):
    '''Renvoie la direction que doit suivre le serpent pour se diriger vers le fruit, 
    en évitant dans la majorité des cas qu'il y ait self-bite'''
    vect = [fruit[0] - serpent[-1][0], fruit[1] - serpent[-1][1]]
    if abs(vect[0]) >= abs(vect[1]):
        dir1 = [signe(vect[0]), 0]
        dir2 = [0, signe(vect[1])]
    else:
        dir1 = [0, signe(vect[1])]
        dir2 = [signe(vect[0]), 0]
    head = [serpent[-1][0] + dir1[0], serpent[-1][1] + dir1[1]]
    if dir1 != opp(direction) and head not in serpent:
        return dir1
    else:
        return dir2
# Fin de la définition de fonctions annexe pour le bot

# Définition fonction de sauvegarde
def save_state(serpent, direction, fruit, score):
    save = open("save.py", "w")
    vals = [serpent, direction, fruit, score]
    names = ["save_serpent", "save_direction", "save_fruit", "save_score"]
    txt = ""
    for k in range(4):
        txt = txt + names[k] + f" = {vals[k]} ; "
    save.write(txt)


# Définition fonction chargement de sauvegarde
def load_state():
    global serpent, direction, fruit, score
    from save import save_direction, save_fruit, save_score, save_serpent
    serpent = save_serpent
    direction = save_direction
    fruit = save_fruit
    score = save_score



def setup():
    return pg.display.set_mode((600, 600)), pg.time.Clock()


def handle_events():
    global direction
    global running
    global bot
    global score
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
                print(f"Score : {score}")
            if event.key == pg.K_UP and direction != [0, 1]:
                direction = [0, -1]
            if event.key == pg.K_DOWN and direction != [0, -1]:
                direction = [0, 1]
            if event.key == pg.K_LEFT and direction != [1, 0]:
                direction = [-1, 0]
            if event.key == pg.K_RIGHT and direction != [-1, 0]:
                direction = [1, 0]
            if event.key == pg.K_b:
                bot = not bot
            if event.key == pg.K_s:
                save_state(serpent, direction, fruit, score)
            if event.key == pg.K_l:
                load_state()


def move_snake():
    global direction
    global running
    global bot
    global score
    # on vérifie si le bot doit être activé, si oui la direction est donnée à tout moment par dir_bot
    if bot:
        direction = dir_bot(serpent, direction, fruit)
    tete = [serpent[-1][0] + direction[0], serpent[-1][1] + direction[1]]
    # autocollision
    if tete in serpent[:-1]:
        running = False
        print(f"Game over ! Self-bite \nScore : {score}")
    # traversée murs
    if tete[0] > 29:
        tete = [0, tete[1]]
    elif tete[0] < 0:
        tete = [29, tete[1]]
    elif tete[1] > 29:
        tete = [tete[0], 0]
    elif tete[1] < 0:
        tete = [tete[0], 29]
    # on ajoute la tête au serpent
    serpent.append(tete)
    # on lui retire la queue si il n'a pas mangé de fruit à cette frame
    if tete != fruit:
        serpent.pop(0)
    # on dessine un nouveau fruit si le fruit a été mangé à cette frame
    else:
        fruit[0] = rd.randint(0, 29)
        fruit[1] = rd.randint(0, 29)
        score += 1


def draw_frame(screen):
    # dessin du fond d'écran
    screen.fill((150, 200, 0))
    for pos in checker_index:
        case = pg.Rect(pos[0] * 20, pos[1] * 20, width, height)
        pg.draw.rect(screen, (200, 255, 0), case)
    # dessin du fruit
    rect_fruit = pg.Rect(fruit[0] * 20, fruit[1] * 20, width, height)
    pg.draw.rect(screen, color_fruit, rect_fruit)
    # dessin du serpent
    for pos in serpent:
        rect = pg.Rect(pos[0] * 20, pos[1] * 20, width, height)
        pg.draw.rect(screen, color_snake, rect)
    #affichage du score
    pg.display.update()
    pg.display.set_caption(f"🐍 Score: {score}")


def wait_for_next_frame(clock):
    clock.tick(3)



screen, clock = setup()

while running:

    handle_events()

    move_snake()

    draw_frame(screen)

    wait_for_next_frame(clock)

pg.quit()
