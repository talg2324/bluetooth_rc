"""

@talg

"""

import pygame
from bluetooth import *

BTsocket = BluetoothSocket(RFCOMM)

# Reminder: 3 = UP , 4 = DOWN, 5 = RIGHT, 6 = LEFT
direct_dict = {273: '3', 274: '4', 275: '5', 276: '6'}

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printt(self, screen, textString):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


BTsocket.connect(("3C:71:BF:60:6E:1E", 1))

pygame.init()

# Set the width and height of the screen [width,height]
size = [700, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("ArduinoMobile Controls")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Get ready to print
textPrint = TextPrint()

# Set frame to reset each 10mills
pygame.key.set_repeat(10, 10)

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
		all_keys = pygame.key.get_pressed()
		for key in direct_dict:
			if all_keys[key]:
				BTsocket.send(direct_dict[key])

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    textPrint.reset()

    textPrint.printt(screen, "Welcome to Tal's ArduinoMobile!")
    textPrint.printt(screen, "Instructions: ")
    textPrint.printt(screen, "Use the arrow keys to control the car,")
    textPrint.printt(screen, "Please note that Reverse is not supported")

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
BTsocket.close()
