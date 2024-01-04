# Grid size
TILEWIDTH = 16
TILEHEIGHT = 16

# Window size (grids)
NROWS = 36
NCOLS = 28
SCREENWIDTH = NCOLS*TILEWIDTH
SCREENHEIGHT = NROWS*TILEHEIGHT
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# Colors (rgb tuple)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Direction value (key for dictionary)
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

# Entities
PLAYER = 0
ZOMBIE = 1

# Zombie mode
WANDER = 0 
CHASE = 1

# Portal
PORTAL = 3

# Text
SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4