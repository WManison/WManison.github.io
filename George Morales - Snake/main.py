'''
Snake Game
George D. Morales
4/8/2025
University of Colorado Colorado Springs
Copyright (c) 2025 George D. Morales. All rights reserved.
Licensed under the MIT License.

This is a simple implementation of the classic Snake game using the Pygame module.
Much like the original game, the player controls a "snake" that takes the form of a cube moving around a grid
and eats "fruit" that appears on the grid. The snake grows in length each time it eats a fruit, and the game ends
when the snake collides with itself or the walls of the grid.
The score is tracked via how many fruits the snake has eaten, and is displayed at the end of the game.
The game is played using the arrow keys to control the snake's direction.
'''

#import the necessary modules to make this program work
#import the pygame module to create the game window and display the game elements
import pygame
from pygame.locals import *
#import the random module to generate random numbers for the fruit's position
import random
#import the asyncio module to create asynchronous functions
import asyncio

#set the colors to be used in the game
#these colors are used to set the background color, the snake color, and the fruit color
SURFACE_COLOR = (167, 255, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)

#define the GRID_SIZE variable to be used to set the size of the grid
#and set the grid size to 30
GRID_SIZE = 30

#define the Snake class
#this class is used to create a snake sprite and move it around the game board
class Snake:
    #constructor to define the snake's attributes
    #this constructor sets the snake's length, position, direction, and color
    def __init__(self):
        self.length = 1
        #set the initial snake position to be at the center of the screen
        self.positions = [(300, 300)]
        #set the snake's initial direction to be None, aka not moving
        self.direction = (0, 0)
        #set the snake's color to be red
        self.color = RED
    #end of Snake constructor

    #define the update function 
    #this function will be used to update the snake's position
    #as it travels around the game board
    #this function will be called every time the snake moves
    def update(self):
        #get the current position of the snake's head
        head_x, head_y = self.positions[0]

        #calculate the new head position based on direction and set a new variable
        #new_head to be the new position of the snake's head
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        #add the new head to the snake's positions and remove the last segment of the snake as it moves
        #to simulate the snake's movement
        self.positions = [new_head] + self.positions[:-1]
    #end of function update()

    #define the grow function 
    #this function will be used to grow the snake's body when it eats a fruit
    #this function will be called every time the snake eats a fruit
    def grow(self):

        #get the position of the snake's tail
        #and store it in a variable called tail
        tail = self.positions[-1]
        #get the position of the second last segment of the snake
        #and store it in a variable called second_last
        second_last = self.positions[-2] if len(self.positions) > 1 else tail

        #calculate the direction of the tail segment by using the position of the 
        #second last segment and the tail segment
        #and store the result in a new variable called tail_direction
        tail_direction = (tail[0] - second_last[0], tail[1] - second_last[1])

        #calculate the new segment in the direction opposite to the tail's movement
        #and set a new variable new_segment equal to the new position of the snake's tail, 
        #aka the next position behind the tail
        new_segment = (tail[0] - tail_direction[0], tail[1] - tail_direction[1])
        #add the new segment to the snake behind the tail using the calculated
        #new_segment variable to extend the snake's body
        self.positions.append(new_segment)
    #end of function grow()

    #define the set_direction function
    #this function will be used to set the snake's direction based on the user's keyboard input
    #this function will be called every time the user presses a key
    def set_direction(self, direction):
        #prevent the snake from moving in the opposite direction since the snake would run into itself
        #by checking if the direction is opposite to the current direction
        #if the direction is opposite to the current direction, do not change the direction
        #else, set the direction to the new direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    #end of function set_direction()

    #define the draw function
    #this function will be used to draw the snake on the screen
    #this function will be called every time the snake moves
    def draw(self, screen):
        #set a for loop to iterate through the snake's positions
        #for each position of the snake, aka the number of segments that make up the snake
        #draw a rectangle at the position of the snake using the color and size of the snake
        #to simulate the snake's whole body movement on the screen
        for position in self.positions:
            pygame.draw.rect(screen, self.color, pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE))
    #end of function draw()
#end of class Snake

#define the Fruit class
#this class is used to create fruit objects that the snake will eat
#and to generate a random position for the fruit on the screen
class Fruit:
    #define the constructor for the fruit class
    #this constructor will be used to set the fruit's position and color
    def __init__(self, screen_width, screen_height):
        #set the fruit's position to a random position on the screen
        #using the random_position function
        self.position = self.random_position(screen_width, screen_height)
        #set the fruit's onscreen color to be green
        self.color = GREEN
    #end of Fruit constructor

    #define the random_position function
    #this function will be used to generate a random position for the fruit objects on the screen
    #this function will be called every time a new fruit is created
    def random_position(self, screen_width, screen_height):
        #generate a random x and y position for the fruit
        #using the random.randint function to generate a random number
        #between 0 and the screen width and height respectively
        #and set the new x and y variables equal to their respective coordinates
        x = random.randint(0, (screen_width // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (screen_height // GRID_SIZE) - 1) * GRID_SIZE
        #return the new x and y position as a tuple
        return (x, y)
    #end of function random_position()

    #define the draw function
    #this function will be used to draw the fruit on the screen
    #this function will be called every time a new fruit object is created
    def draw(self, screen):
        #draw the fruit as a rectangle similar to that of the snake
        #using the color and size of the fruit
        #to display the fruit on the screen
        #set the fruit's position to be at the random position on the grid that was generated
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
#end of class Fruit

#define the main function
#this function will be used to run the game and its main loop
#this function will be called when a game is started via the restart game option
#and when the code is run
async def main():
    #initialize the pygame module by calling the pygame.init() function
    #this function will be used to initialize all the modules that are imported
    #from the pygame module in order to properly create and run the game and its elements
    pygame.init()

    #set the screen dimensions to be used in the game
    #set the WINDOW_WIDTH and WINDOW_HEIGHT variables to be used to the set size of 630
    #combined with the GRID_SIZE, this will make the 21x21 grid
    WINDOW_WIDTH, WINDOW_HEIGHT = 630, 630
    #create the game window using the pygame.display.set_mode() function
    #that will set the size of the game window to be the same as the screen dimensions
    #and store its attributes in the new variable SCREEN
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #display the caption 'Snake Game' on the game window using the pygame.display.set_caption() function
    pygame.display.set_caption('Snake Game')

    #initialize the snake and fruit objects and store them in their respective 
    #variables snake and fruit
    snake = Snake()
    fruit = Fruit(WINDOW_WIDTH, WINDOW_HEIGHT)

    #create the game loop
    #define and initially set variable score_tracker, that will be used to keep track of the score, to 0
    score_tracker = 0
    #create the clock variable to be used to control the frame rate of the game, 
    #aka the speed at which the snake moves
    clock = pygame.time.Clock()
    #create the run_game variable to be used to control the game loop
    #and set its initial value to True
    run_game = True

    #set the font and the text size for the 
    #game over messages
    #these messages include a game over message, a score message, and a play again message
    game_over_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 40)
    play_again_font = pygame.font.Font(None, 40)
    


    #create the game over messages to be displayed after the game is completed
    game_over_text = game_over_font.render("Game Over!", True, WHITE)
    #create the message to ask the player if they want to play again
    play_again_text = play_again_font.render("Would you like to play again? y/n", True, WHITE)

    #set a for loop that will act as the main game loop
    #this loop will run until run_game is set to False,
    #aka when the game is over or when the user quits the game
    while run_game:
        #check for any events that occur in the game
        for event in pygame.event.get():
            #if that event is a quit event, then run_game is set to False
            #and the game will end
            if event.type == pygame.QUIT:
                run_game = False
            elif event.type == pygame.KEYDOWN:
                # Handle key presses for direction changes
                #if the key pressed is the left arrow key, then set the snake's direction to be left
                if event.key == pygame.K_LEFT:
                        snake.set_direction((-GRID_SIZE, 0))
                #if the key pressed is the right arrow key, then set the snake's direction to be right
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((GRID_SIZE, 0))
                #if the key pressed is the up arrow key, then set the snake's direction to be up
                elif event.key == pygame.K_UP:
                    snake.set_direction((0, -GRID_SIZE))
                #if the key pressed is the down arrow key, then set the snake's direction to be down
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, GRID_SIZE))

        #update the snake's current position using the update function attribute
        #of the snake class
        snake.update()


        #set an if statement to check if the snake's head is in the same position as the fruit
        #if it is, then the games score will go up by 1 and the snake will grow by one length
        if snake.positions[0] == fruit.position:
            #grow the snake by one length
            snake.grow()
            #increase the score of the current game by 1
            score_tracker += 1
            print(f"Score: {score_tracker}")
            #create a new fruit object and set it to a random position
            #on the board
            fruit = Fruit(WINDOW_WIDTH, WINDOW_HEIGHT)
            #check if the fruit's position is in the snake's path, aka if it is overlapping with the snake's body
            #if it is, then generate a new fruit and its position
            #repeat until the fruit's position is not in the snake's path
            #print a message to the console to indicate that the fruit's position is in the snake's path
            #and that a new fruit is being generated
            while fruit.position in snake.positions:
                fruit = Fruit(WINDOW_WIDTH, WINDOW_HEIGHT)
                print("Fruit position in path of snake, regenerating fruit")
            #update the snake's position
            snake.update()

        #check for snake collision with itself
        #if the snake's head collides with any of its body segments, the game ends
        if snake.positions[0] in snake.positions[1:]:
            #set the snake's direction to be None, aka not moving
            snake.set_direction((0, 0))
            #end the game loop
            run_game = False

        '''
        #optional debugging section to check the snake's position
        #get the snake's head position and body positions and store them in new, 
        #respective variables head and body
        head = snake.positions[0]
        body = snake.positions[1:]

        #print the snake's current head and body positions to the console for debugging purposes
        print(f"Snake Head: {snake.positions[0]}")
        print(f"Snake Body: {snake.positions[1:]}")
        '''

        #section to draw the game
        #first, clear the screen by filling it with the background color
        SCREEN.fill(BLACK)
        #then, draw the grid using the draw_grid function
        draw_grid(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN, WHITE)
        #then, draw the snake using the draw method of the snake class
        snake.draw(SCREEN)
        #then, draw the fruit using the draw method of the fruit class
        fruit.draw(SCREEN)

        #update the display to show the new frame by calling the pygame.display.flip() function
        pygame.display.flip()

        #set the frame rate of the game, aka the speed at which the snake moves
        #using the clock.tick() function and initially set the frame rate to 10
        clock.tick(10)

        #check for collisions with the walls
        #if the snake's head goes out of bounds, end the game
        head_x, head_y = snake.positions[0]
        if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 0 or head_y >= WINDOW_HEIGHT:
            #set the snake's direction to be None, aka not moving
            snake.set_direction((0, 0))
            #end the game loop
            run_game = False
        await asyncio.sleep(0)
    #end of the game loop

    #clear the screen by making it all black
    SCREEN.fill(BLACK)

    #create the score message to be displayed after the game is completed
    score_text = score_font.render(f"Your Score: {score_tracker}", True, WHITE)

    #display the game over message to the screen
    SCREEN.blit(game_over_text, (WINDOW_WIDTH // 3 - game_over_text.get_width() // 6.5, WINDOW_HEIGHT // 3 - game_over_text.get_height() // 3))
    #display the score message to the screen
    SCREEN.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2.25 - score_text.get_height() // 2))
    #display the play again message to the screen
    SCREEN.blit(play_again_text, (WINDOW_WIDTH // 2 - play_again_text.get_width() // 2, WINDOW_HEIGHT // 1.75 - play_again_text.get_height() // 3))

    #update the display to show the game over message and the play again message
    pygame.display.flip()

    #get user input on whether they want to restart and play the game again or not
    #set a variable wait_for_input to be True
    wait_for_input = True
    #set a while loop that will loop until the user presses a key
    while wait_for_input:
        #check for any events that occur in the game
        #if the event is a quit event, then set wait_for_input to False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait_for_input = False
            #if the event is a key down event, then check if the key pressed is the Y or N key
            if event.type == pygame.KEYDOWN:
                #if the key pressed is the Y key, then restart the game by going back to the
                #beginning of the main function and set wait_for_input to False
                if event.key == pygame.K_y:
                    await main()
                    wait_for_input = False
                #if the key pressed is the N key, then set wait_for_input to False
                elif event.key == pygame.K_n:
                    wait_for_input = False


    #quit the pygame module by calling the pygame.quit() function
    #this function will be used to quit the game and close the game window
    pygame.quit()
#end of the main function

#define the draw_grid function
#this function will be used to draw the grid on the screen
#this function will be called every time the gameboard is drawn or updated
def draw_grid(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN, GRIDLINE_COLOR):
    #set the cell size of the grid to be the same as the grid size
    #and store it in a new variable called block_size
    block_size = GRID_SIZE
 
    #set a for loop to iterate through the x and y coordinates of the grid
    #using the range function to create a grid of rectangles
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            #create a rectangle at the x and y coordinates of the grid
            #using the pygame.Rect function to create a rectangle object
            #and set the rectangle's position to be at the x and y coordinates
            #of the grid using the block size and store it in a new variable called rect
            rect = pygame.Rect(x, y, block_size, block_size)
            #draw the rectangle on the screen using the pygame.draw.rect function
            pygame.draw.rect(SCREEN, GRIDLINE_COLOR, rect, 1)
#end of function draw_grid()

#call the main function to run the program
if __name__ == '__main__':
    asyncio.run(main())