import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 300
dis_height = 200

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake - Food')
 
clock = pygame.time.Clock()

block_size = 10
snake_block = 10


# display messages in pygame
score_font = pygame.font.SysFont(None, 15)

def score(n):
    value = score_font.render("Score: " + str(n), True, black)
    dis.blit(value, [0,0])

font_style = pygame.font.SysFont(None, 15)
    
def message(msg, colour): 
    mesg = font_style.render(msg, True, colour)
    dis.blit(mesg, [dis_width/3,dis_height/2])

# draw snake
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

    
# main loop
def gameloop():
    game_end = False    
    game_over = False
    x1 = dis_width/2
    y1 = dis_height/2
    snake_head = [x1,y1]
    framerate = 10

    x_change = 0
    y_change = 0
    
    food_x = round(random.randrange(0, dis_width - block_size) / 10.0)*10
    food_y = round(random.randrange(0, dis_height - block_size) / 10.0)*10

    snake_list = []
    snake_length = 1
    turn = 1
    n = 0
    win = False
    while not game_over and turn > 0:
        while game_end == True:
            if win == True:
                dis.fill(white)
                message("You win.", black)
                pygame.display.update()
                time.sleep(1)
                break
            else:
                message("You lose.", black)
                pygame.display.update()
                time.sleep(1)
                break
        while game_end == True:
            dis.fill(white)
            message("Press q - quit or p - play again", black)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_end = False # get out of this loop
                    if event.key == pygame.K_p:
                        gameloop()

##############################################################################
######################### START OF FOOD MOVEMENT #############################
##############################################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and food_x != 0: 
                    x_change = -snake_block # move 1 block toward 0 position 
                    y_change = 0
                elif event.key == pygame.K_RIGHT and food_x != dis_width-10: #and (len(snake_list)== 1 or x1+snake_block != snake_list[-2][0]):
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and food_y != 0: #and (len(snake_list)== 1 or y1-snake_block != snake_list[-2][1]):
                    x_change = 0
                    y_change = -snake_block  # (0,0) is top left corner. So goes up is minus
                elif event.key == pygame.K_DOWN and food_y != dis_height-10: #and (len(snake_list)== 1 or y1+snake_block != snake_list[-2][1]):
                    x_change = 0
                    y_change = snake_block
                #print(x1, y1)
        
        #pygame.draw.rect(dis,red,[food_x,food_y,snake_block,snake_block])
        
        food_x += x_change # these x1 and x2 are in the while loop, so 
        
        food_y += y_change # x and y position will continuosly update itself

        if food_x >= dis_width-10 and x_change == block_size or food_x <= 0 and x_change == -block_size:
            x_change = 0
        if food_y >= dis_height-10 and y_change == block_size or food_y <= 0 and y_change == -block_size:
            y_change = 0

        dis.fill(white) # got to fill with white immediately to clean off the trodden path
        pygame.draw.rect(dis,red,[food_x,food_y,snake_block,snake_block])

##############################################################################
######################### START OF SNAKE MOVEMENT ############################
##############################################################################

        if [food_x, food_y] in snake_list:
            win = False
            game_end = True
            
                     #and (len(snake_list)== 1 or x1-snake_block != snake_list[-2][0]):
                     # ^ when LEFT is pressed and as long as its only one head or not going back to the body, 
        if turn % 3 != 0: #snake stop every 4 turns
            
            x_diff = food_x - snake_head[0]
            y_diff = food_y - snake_head[1]

            if abs(x_diff) >= abs(y_diff):
                if x_diff > 0:
                    x1 += snake_block
                elif x_diff <= 0:
                    x1 -= snake_block
            else:
                if y_diff > 0:
                    y1 += snake_block
                else:
                    y1 -= snake_block
            
            snake_head = [x1,y1] # continuously create new pos for head
            snake_list.append(snake_head) # append into snake list to be drawn
            
            if len(snake_list) > snake_length:
                del snake_list[0] # if havent lengthen, delete the previous head pos
            for x in snake_list[:-1]: # check from tail to before head ([-1] is the head, we always append head) to see if it coincides with head
                if x == snake_head:
                    win = True
                    game_end = True
                    
                   
        snake(snake_block, snake_list) # draw snake after updating length and ensure we passed the tail
        pygame.display.update()

        # increment turns, increase snake length and framerate to up difficulty
        turn += 1
        if turn%9 == 0: 
            snake_length += 1
            framerate += 0.5
        speed = min(framerate, 50)
        clock.tick(speed)

    
    pygame.quit()
    quit()


gameloop()
