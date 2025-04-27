'''
Blackjack Game
Jack Dodge
4/27/2025
University of Colorado Colorado Springs
Copyright (c) 2025 Jack Dodge. All rights reserved.
Licensed under the MIT License.
'''

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# RGB colors
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Card size
CARD_WIDTH, CARD_HEIGHT = 70, 100

# Choosing font
font = pygame.font.SysFont('Arial', 24)

# Calculate the values of each participants hand
def calculateHandValues(hand):
    # Store the value of the hand and the number of aces to account for soft hands.
    value = 0
    aces = 0
    for card in hand:
        # Add 10 to value for face cards
        if card[0] in ['J', 'Q', 'K']:
            value += 10
        # Add 11 for ace value, track aces to account for soft hands
        elif card[0] in ['A']:
            aces += 1
            value += 11
        # Add numbered values normally
        else:
            value += int(card[0])
    
    # Change aces to 1's if the hand goes above 21
    while aces > 0 and value > 21:
        aces -= 1
        value -= 10
    return value

# Function to draw the card and add it to the board of who drew it.
def drawCard(x, y, value, suit, face_up=True):
    """Draw a card at position (x, y)"""
    if face_up:
        # Card background
        pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
        
        # Red cards are hearts and diamonds, black is clubs and spades.
        color = RED if suit in ['♥', '♦'] else BLACK

        text = font.render(value, True, color)
        # Position of vard value symbol
        screen.blit(text, (x + 5, y + 5))
        
        # Render the card suit symbol
        suit_text = font.render(suit, True, color)
        # Location of the suit symbol on the card
        screen.blit(suit_text, (x + CARD_WIDTH - 20, y + CARD_HEIGHT - 30))
    else:
        # Blue backing for the facedown card
        pygame.draw.rect(screen, (0, 0, 139), (x, y, CARD_WIDTH, CARD_HEIGHT))
        # Black border to differentiate from the surroundings
        pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)

# 52 Card deck, 4 suits, 2-10 with J Q K A.
def createDeck():
    suits = ['♠', '♥', '♦', '♣']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []
    # Loop so every suit has every card type
    for suit in suits:
        for value in values:
            deck.append((value, suit))
    # Randomize deck
    random.shuffle(deck)
    return deck

def resetVariables():
    # Make and reset the deck
    deck = createDeck()
    # Track player and dealer hands, start them off with 2 cards from deck
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    game_over = False
    # For the main messages, clears previous messages
    message = ""
    return deck, player_hand, dealer_hand, game_over, message


def main():
    
    deck, player_hand, dealer_hand, game_over, message = resetVariables()
        
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Key presses doing something here
            if event.type == pygame.KEYDOWN:
                # Pressing h adds a card to the players hand
                if event.key == pygame.K_h and not game_over:
                    player_hand.append(deck.pop())
                    if calculateHandValues(player_hand) > 21:
                        game_over = True
                        message = "Player Busts! Dealer wins!"
                # Pressing s reveals the dealers hand and ends the game
                if event.key == pygame.K_s and not game_over:
                    game_over = True
                    # Dealer flips cards and draws until they have a value >= 17
                    while calculateHandValues(dealer_hand) < 17:
                        # dealer draws
                        dealer_hand.append(deck.pop())
                    # Calculate the final value of both hands
                    player_hand_value = calculateHandValues(player_hand)
                    dealer_hand_value = calculateHandValues(dealer_hand)

                    # If dealer hand greater than 21 player wins
                    if dealer_hand_value > 21:
                        message = "Dealer Busts! Player Wins!"
                    # If dealer hand greater than players dealer wins
                    elif dealer_hand_value > player_hand_value:
                        message = "Dealer Wins!"
                    # If dealer hand less than player hand player wins
                    if dealer_hand_value < player_hand_value:
                        message = "Player Wins!"
                    # If they tie then it's a tie
                    if dealer_hand_value == player_hand_value:
                        message = "It's a Tie!"
                # Pressing R resets the game by resetting variables, can only be done once the game is over
                if event.key == pygame.K_r and game_over:
                    deck, player_hand, dealer_hand, game_over, message = resetVariables()
        
        # Create green table
        screen.fill(GREEN)
        
        # Draw dealer's cards
        # Currently using seperate lines for dealer and player cards, may go back and make it one object
        pygame.draw.rect(screen, (0, 80, 0), (50, 50, WIDTH - 100, 150))
        # Words designating that the hand is the dealers
        dealer_text = font.render("Dealer's Hand:", True, WHITE)
        # Location of designator, right above their board to the far left
        screen.blit(dealer_text, (50, 20))
        
        # Creates the images of the dealers first card facedown, then second one face up 
        for i, card in enumerate(dealer_hand):
            if i == 0 and not game_over:
                drawCard(100 + i * 80, 80, card[0], card[1], face_up = False)
            else:
                drawCard(100 + i * 80, 80, card[0], card[1])
        
        # Draw player's cards
        pygame.draw.rect(screen, (0, 80, 0), (50, 300, WIDTH - 100, 150))
        # Words designating that the hand is the players
        player_text = font.render("Player's Hand:", True, WHITE)
        # Location of designator, right above their board to the far left
        screen.blit(player_text, (50, 270))
        
        # Creates the images of the players 2 cards.
        for i, card in enumerate(player_hand):
            drawCard(100 + i * 80, 330, card[0], card[1])
        
        # Draw instructions
        if not game_over:
            # Give the player the rules
            instructions = font.render("Press H to Hit, S to Stand", True, WHITE)
            # Location of the rules on the board
            screen.blit(instructions, (WIDTH//2 - 150, HEIGHT - 50))
        
        else:
            # Display victory/defeat/tie messages
            result_text = font.render(message, True, WHITE)
            screen.blit(result_text, (WIDTH//2 - 100, HEIGHT - 50))
            # Ask if user wants to restart
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - 60, HEIGHT - 80))
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()