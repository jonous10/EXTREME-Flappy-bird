

import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Set screen dimensions
screenWidth = 1920
screenHeight = 1200
percent = 0

# Define screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("EXTREME Flappy Bird")

# Define Images
ash = pygame.image.load("ash665.jpg")
pipeImage = pygame.image.load("Pipe.png")
backgroundImage = pygame.image.load("flappyBackground.png")
bird = pygame.image.load("Flappy.png")

# Define score variables
score = 0
highScore = 0

playerPath = []
last_position = (0, 0)

smoothJumpIteration = 0



# Quick Text drawing function !

def QuickText(
        font : str, 
        size : int, 
        color : tuple, 
        pos : tuple, 
        text : str
        ):
    textFont = pygame.font.SysFont(font, size)
    textRender = textFont.render(text, True, color)
    screen.blit(textRender, pos)

# Quick Image drawing function !

def QuickImage(
        image, 
        size : tuple, 
        pos : tuple,
        flip : bool
        ):
    image = pygame.transform.scale(image, size)
    if flip:
        image = pygame.transform.flip(image, False, True) # This flip only important for top pipe !
    screen.blit(image, pos)

# Math.sign():

def sign(num):
    return 1 if num > 0 else -1 if num < 0 else 0

# Defining a class to use when spawning pipes
class Pipe:
    def __init__(self, x):
        # Initializes common variables
        self.past = False
        self.x = x
        self.topOfGap = random.randint(pipeMinHeight, screenHeight - pipeMinHeight - pipeGap)
        self.bottomOfGap = self.topOfGap + pipeGap
            
    def draw(self):
        # Calculate the image height to have a constant image ratio
        pipeHeight = 650 + pipeWidth * 0.1
        # Draw top pipe
        QuickImage(pipeImage, (pipeWidth, pipeHeight), (self.x, -pipeHeight + self.topOfGap), True)
        # Draw bottom pipe
        QuickImage(pipeImage, (pipeWidth, pipeHeight), (self.x, self.bottomOfGap), False)
    def move(self):

        global score

        # Moves pipes
        self.x -= pipeSpeed

        if self.past == False and self.x + pipeWidth < playerX:
            score += 1
            self.past = True

    def offScreen(self):
        # Checks if the pipe is off screen
        return self.x + pipeWidth < 0
    def hitboxTop(self):
        hitbox = (self.x, 0, pipeWidth, self.topOfGap)
        return hitbox
    def hitboxBottom(self):
        hitbox = (self.x, self.bottomOfGap, pipeWidth, screenHeight)
        return hitbox
    
# Define player variables
playerRadius = 20
playerX = 400 # These positional variable do not change, rather self.y
guestX = 450
playerY = 600
playerGravity = 0.4
playerJumpForce = 400
playerGlideForce = 2


class Player:
    def __init__(self, X):
        # Initializes common variables
        self.x = X
        self.y = playerY
        self.rot = 0
        self.velocity = 0

        self.buttonReleased = False
        self.canJump = False
        self.buttonHeldTime = 0

        self.bird = bird

        self.path = []
        self.oldPath = []

        self.bird = pygame.transform.scale(self.bird, (200, 100))

    def gravity(self):
        self.velocity += playerGravity

    def updateJump(self):
        # The player can only jump if the time the button is held is a short
        if 0 < self.buttonHeldTime < 0.1:  
            self.canJump = True
        else:
            self.canJump = False

        
        if self.canJump and self.buttonReleased:
            print("JUMP!!!!!")
            self.velocity -= playerJumpForce * 0.02  # Apply jump force
            self.buttonReleased = False

    def updateGlide(self):
        if self.buttonHeldTime >= 0.1:  # Long time press for glide
            print("GLIDE!!!!!")
            self.velocity += -(self.velocity * self.velocity) * playerGlideForce * clockTick * sign(self.velocity)

    def updatePosition(self):
        # Update Position based on velocity
        self.y += self.velocity

        # Teleports player when out of the screen to the other side of the screen (Portal)
        if self.y < 0:
            self.y = screenHeight
            # Saves the old path so it can show on the other side
            self.oldPath = self.path
            self.path = []

        if self.y > screenHeight:
            self.y = 0
            # Saves the old path so it can show on the other side
            self.oldPath = self.path
            self.path = []

        if len(self.path) > 1:
            # Update rotation of bird based on trigonometry, by taking the inverse tangent of the opposite over adjacent
            opposite = self.path[-1][0] - self.path[-2][0]
            adjacent = self.path[-1][1] - self.path[-2][1]
            # Apply the rotation of that in degrees
            self.rot = math.atan(opposite / adjacent)

    def draw(self, color):
        screen.blit(self.bird, (self.x - 100, self.y - 50))

    # Executes the operations 
    def executeOps(self, color, pathColor, pathWidth):
        self.gravity()
        self.updateJump()
        self.updateGlide()
        self.updatePosition()
        self.paths(pathColor, pathWidth)
        self.draw(color)

    def hitbox(self):
        hitbox = pygame.Rect(
            self.x - 0.71 * playerRadius,
            self.y - 0.71 * playerRadius,
            2 * playerRadius,
            2 * playerRadius
        )
        return hitbox

    # Check for a collision between the player and a pipe
    def collided(self, pipeTop, pipeBottom):
        this = self.hitbox()
        return this.colliderect(pipeTop) or this.colliderect(pipeBottom)

    def paths(self, color, width):
        # Offset based on pipes
        self.path = [(i[0] - pipeSpeed, i[1]) for i in self.path]
        self.oldPath = [(i[0] - pipeSpeed, i[1]) for i in self.oldPath]

        # Adds turbulance
        turb = 0.4
        self.path = [(i[0] + random.uniform(-turb, turb), i[1] + random.uniform(-turb, turb)) for i in self.path]
        self.oldPath = [(i[0] + random.uniform(-turb, turb), i[1] + random.uniform(-turb, turb)) for i in self.oldPath]

        self.path.append((self.x, self.y))

        if len(self.path) + len(self.oldPath) > 40:
            if len(self.oldPath) > 0:
                self.oldPath.pop(0)
            else:
                self.path.pop(0)
        if len(self.path) > 1:
            pygame.draw.lines(screen, color, False, self.path, width)
        if len(self.oldPath) > 1:
            pygame.draw.lines(screen, color, False, self.oldPath, width)

inBluePhase = True
animPerc = 0

while inBluePhase:
    QuickImage(ash, (1920, 1200), (0, 0), False)

    percent += 0.01

    # Animates the animated percent
    integers = [
        1, 2, 3, 5, 6, 7, 8, 9, 10, 
        11, 14, 15, 16, 17, 18, 19, 
        32, 33, 34, 35, 36, 41, 42, 
        43, 49, 50, 51, 54, 55, 56, 
        57, 58, 60, 61, 62, 49, 50,
        74, 75, 76, 77, 78, 79, 80, 
        81, 82, 83, 85, 92, 98, 99]
    # Rounds animPerc down to nearest integer in list integers
    for i in range(len(integers) - 1):
        if integers[i] < percent < integers[i + 1]:
            animPerc = integers[i]

    QuickText(
        "Arial", 
        20, 
        (255, 255, 255), 
        (205, 775),
        "For more information about this issue and possible fixes, please visit our website.\n To launch Co-op press keycode 8, for Solo press keycode 4"
        )
    
    QuickText(
        "Arial", 
        45, 
        (255, 255, 255), 
        (205, 675),
        f"{animPerc}%"
        )

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_8:
                inBluePhase = False
                coop = True
            if event.key == pygame.K_4:
                inBluePhase = False
                coop = False
    # Update display
    pygame.display.flip()


running = True
inGame = True
deathScreen = False
while running:

    # Define pipe variables
    pipeMinHeight = 120
    pipeMinHeightMax = 250
    
    pipeWidth = 110
    pipeWidthMax = 200
    
    pipeGap = 500
    pipeGapMin = 240
    
    pipeSpeed = 10
    pipeSpeedMax = 20
    
    pipeFreq = 10
    pipeFreqMax = 50


    # Defines and empty list to fill with pipes later
    pipes = []

    # Start time since last pipe at 1 second instant first spawn
    timeSinceLastPipe = 1.0
    timeStep = 0
    clock = pygame.time.Clock()
    
    player = Player(playerX)
    guest = Player(guestX)

    newHighscore = False
    score = 0

    while inGame:
        clockTick = clock.tick(60) * 0.001

        # Handles events

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            player.buttonHeldTime += clockTick
        else: 
            player.buttonHeldTime = 0
            print("RESET PLAYER !")
        if pressed[pygame.K_RSHIFT] and coop:
            guest.buttonHeldTime += clockTick
        else: 
            guest.buttonHeldTime = 0
            print("RESET GUEST !")

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    inGame = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.buttonReleased = True
                else:
                    player.buttonReleased = False
                if event.key == pygame.K_RSHIFT:
                    guest.buttonReleased = True
                else:
                    guest.buttonReleased = False



        # Draws the flappy bird background
        QuickImage(backgroundImage, (1920, 1200), (0, 0), False)

        # Increasing the time since last pipe by a small tick in sec
        timeSinceLastPipe += clockTick
        if timeSinceLastPipe * pipeSpeed >= pipeFreq:

            pipes.append(Pipe(screenWidth))
            timeSinceLastPipe = 0  # Reset the timer to 0

        # Decrease pipe gap, increase pipe thickness, and more pipe variables over time

        timeStep += clockTick
        if timeStep > 0.2:
            timeStep = 0

            pipeGap -= 1
            if pipeGap < pipeGapMin:
                pipeGap = pipeGapMin
                print("PIPE GAP LOCKED IN!")
            pipeWidth += 2
            if pipeWidth > pipeWidthMax:
                pipeWidth = pipeWidthMax
                print("PIPE WIDTH LOCKED IN!")
            pipeFreq += 0.1
            if pipeFreq > pipeFreqMax:
                pipeFreq = pipeFreqMax
                print("PIPE FREQ LOCKED IN!")
            pipeSpeed += 0.04
            if pipeSpeed > pipeSpeedMax:
                pipeSpeed = pipeSpeedMax
                print("PIPE SPEED LOCKED IN!")
            pipeMinHeight += 1
            if pipeMinHeight > pipeMinHeightMax:
                pipeMinHeight = pipeMinHeightMax
                print("PIPE SPREAD LOCKED IN!")

            # Used to test the extremes flappy bird

            #pipeGap = pipeGapMin
            #pipeWidth = pipeWidthMax
            #pipeFreq = pipeFreqMax
            #pipeSpeed = pipeSpeedMax
            #pipeMinHeight = pipeMinHeightMax

        # Pipe Operations!

        # Assure that the list of pipes is not empty
        if len(pipes) != 0:
            # Moves and draws each pipe in list pipes
            for pipe in pipes:
                pipe.move()
                pipe.draw()

                # Very long condition... this is maybe weird
                if (player.collided(pipe.hitboxTop(), pipe.hitboxBottom())):
                    deathScreen = True
                    inGame = False
                if (guest.collided(pipe.hitboxTop(), pipe.hitboxBottom()) and coop):
                    deathScreen = True
                    inGame = False
                        

            # Checks if the first pipe in pipes is off screen
            if pipes[0].offScreen():
                # Removes that pipe from pipes
                pipes.pop(0)

        # Player Operations!

        player.executeOps((250, 45, 58), (180, 220, 255), 10)

        # Guest Operations (if in coop) !

        if coop:
            guest.executeOps((24, 198, 70), (160, 255, 220), 10)



        # Draw Score !

        scoreColor = (0, 0, 0)
        if score > highScore:
            newHighscore = True
            scoreColor = (30, 200, 5)

        QuickText(
            "Calibri",
            70,
            scoreColor,
            (840, 620),
            f"{score}"
            )

        # Update the display
        pygame.display.flip()

    # Death Screen

    restartDelay = 0
    while deathScreen:
        restartDelay += clock.tick(60) * 0.001 # Adds 0.001 to restartDelay every millisecond. 1 = 1 sec

        # Fills the screen with a red-ish colour
        screen.fill((120, 55, 55))
        
        # Death Screen text changing based on whether player hit a new highscore
        DSTextColor = (220, 210, 205)
        if newHighscore:
            highScore = score
            DSTextColor = (180, 255, 105)
            deathScreenText = f"A New Highscore of {highScore}"
            
        else:
            DSTextColor = (220, 150, 205)
            deathScreenText = f"Score : {score} Highscore : {highScore}"

        # Handles events
        if restartDelay > 0.5:
            QuickText(
                "Calibri",
                45,
                (255, 255, 255),
                (750, 750),
                "Press [SPACE] to restart"
                )
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        deathScreen = False
                    if event.key == pygame.K_SPACE:
                        inGame = True
                        deathScreen = False

        QuickText(
                "Calibri",
                45,
                DSTextColor,
                (750, 600),
                deathScreenText
                )

        # Update display
        pygame.display.flip()

pygame.quit()
sys.exit()