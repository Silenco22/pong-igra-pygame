#https://neat-python.readthedocs.io/en/latest/xor_example.html
import pygame
from paddle import Paddle
from ball import Ball
from game import Game
import neat 
import os
import pickle
#always initialize pygame first
pygame.init()

#1st draw windov with width, height
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# displays window with the name Pong
pygame.display.set_caption("Pong")

FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

WHITE = (255,255,255)
BLACK = (0,0,0)

#font for drawing scores
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

#winning
WINNING_SCORE = 4



 #setting where the left  and right paddle gonna be draw
left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball(WIDTH//2, HEIGHT//2)

game = Game()



def main():
    game = Game()
    run = True
    clock = pygame.time.Clock() #sets fps for every pc its gonna run the same speed on every pc

    

    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS) #wont run faster than 60 fps on every pc
        #passing every elemet to the drawing function
        game.draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score,True)
        #loopin through all the events taht occur like hiting keyboard etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exiting the game
                run =False
                break
        
        #getting pressed keys
        keys = pygame.key.get_pressed()
        

        #handling movemnet with aonther func to avoid clustering our mani func
        game.handle_paddle_movement(keys, left_paddle, right_paddle)
        #moving the ball
        ball.move()
         #handle collision
        game.handle_collision(ball, left_paddle, right_paddle)
       
        #calculating the score
        if ball.x < 0:
            right_score += 1
            ball.reset()
            game.hits_reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            game.hits_reset()
        #winnig the game
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            #dispaying some text wfter winning
            win_text = "Left won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right won!"

        if won:
            winning_text = SCORE_FONT.render(win_text, 1, WHITE)
            #bliting in the middle of the screen with math calcus :)
            WIN.blit(winning_text,(WIDTH // 2 - winning_text.get_width()//2, HEIGHT // 2 - winning_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            game.hits_reset()
            left_score = 0
            right_score = 0


     #exiting the game  
    pygame.quit()


def test_ai(genome, config):
    game=Game()
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    run = True
    clock = pygame.time.Clock()
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()

        game.handle_paddle_movement(keys, left_paddle, right_paddle)

        output = net.activate((right_paddle.y, ball.y, abs(right_paddle.x - ball.x)))
        decision = output.index(max(output))

        #right paddle
        keys = pygame.key.get_pressed()
        if decision == 0:
            pass
        elif decision == 1: #right up
            ai_key = 'UP'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)
        else: #right down
            ai_key = 'DOWN'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)

        ball.move()
        #handle collision
        game.handle_collision(ball, left_paddle, right_paddle)
        
        #when someone socres we +1 and ball and total paddle hits reset
        if ball.x < 0:
            right_score += 1
            ball.reset()
            game.hits_reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            game.hits_reset()
        
        

        

        game.draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, True)

    pygame.quit()

def calculate_fitness( genome1, genome2, game_info):
        genome1.fitness += game_info[0]
        genome2.fitness += game_info[1]

def train_ai(genome1, genome2, config):
    
    #setting up neat
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball(WIDTH//2, HEIGHT//2)

    left_score = 0
    right_score = 0

    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        
        
        output1 = net1.activate(
                (left_paddle.y, ball.y, abs(left_paddle.x - ball.x)))
        decision1 = output1.index(max(output1))

        keys =pygame.key.get_pressed()
        
        #moving ai paddles
        #left paddle
        if decision1 == 0:
            pass
        elif decision1 == 1: #left up
            ai_key = 'w'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)
        else: #left down
            ai_key = 's'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)

        output2 = net2.activate(
                (right_paddle.y, ball.y, abs(right_paddle.x - ball.x)))
        decision2 = output2.index(max(output2))

        #right paddle
        if decision2 == 0:
            pass
        elif decision2 == 1: #right up
            ai_key = 'UP'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)
        else: #right down
            ai_key = 'DOWN'
            game.handle_paddle_movement(keys, left_paddle, right_paddle, ai_key)

        

        ball.move()
        #handle collision
        game.handle_collision(ball, left_paddle, right_paddle)


        game_info = game.game_info_hits()

        
        #when someone socres we +1 and ball and total paddle hits reset
        if ball.x < 0:
            right_score += 1
            ball.reset()
            game.hits_reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            game.hits_reset()
        
       

        game.draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score,True)
        
       
        if left_score >= 1 or right_score >= 1 or game_info[0] > 50:
            calculate_fitness(genome1, genome2, game_info)
            break    
    


def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            train_ai(genome1, genome2, config)


def run_neat(config):
    
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    
    p = neat.Population(config)#setting up population wiht config file
    #adding reporter and check poithis will display data in console for 1 generation
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    
    #giving fitenss func to neat
    winner = p.run(eval_genomes, 1)
    #saving best genome to the file as bytes pickle alllows us to save enitre pyhton object
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def play_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    test_ai(winner, config)


#runs the game only if its directly called from this window
if __name__ == '__main__':
    """Comment/uncomment lines if u want to train or play against AI or to play against human"""
    #play 1v1 human normal game with main(): keys1: w,s  keys2: up arrow, down arrow
    main()
    local_dir = os.path.dirname(__file__)
    conf_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         conf_path)
    #train AI with run_neat(config):
    # run_neat(config)

    #play against AI: (uncomment next line and comment out run_neat(config) and main())
    # play_ai(config) 
