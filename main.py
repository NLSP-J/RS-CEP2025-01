import asyncio
import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()

purple = (128, 0, 128)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris') 

pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
speed = 10
score = 0
running = True
lifes = 5
wave = 0


player_size = 50
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/images (1).jfif')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 50
obj_data = []     # List to store object positions and their images
obj = pg.image.load('./assets/images/reactor.webp')
obj = pg.transform.scale(obj, (obj_size, obj_size))

bg_image = pg.image.load('./assets/images/images.jfif')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 1000:    
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])

def update_objects(obj_data):
    global score

    for object in obj_data:
        global wave
        x, y, image_data = object
        if y < win_height:
            y += (speed + wave)
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score += 1
            wave = score//10


def collision_check(obj_data, player_pos):
    global running
    global lifes
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            if lifes == 1:
                time.sleep(2)
                running = False
                break
            else:
                lifes -= 1
                time.sleep(3)
                obj_data.remove(object)
                break

async def main():
    global running, wave, bg_image, player_pos
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 20
                elif event.key == pg.K_RIGHT:
                    x += 20
                elif event.key == pg.K_UP:
                    x -= 50
                elif event.key == pg.K_DOWN:
                    x += 50
                player_pos = [x, y]


        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, purple)
        screen.blit(text, (win_width - 200, win_height - 40))

        text = f'Lifes: {lifes}'
        text = font.render(text, 10, purple)
        screen.blit(text, (win_width - 100, win_height - 20))

        text = f'Wave: {wave}'
        text = font.render(text, 10, purple)
        screen.blit(text, (win_width - 400, win_height - 80))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)
        if wave == 7:
            bg_image = pg.image.load('./assets/images/gameover.jpg')

        clock.tick(30)
        pg.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
