# game options/settings
import random
TITLE = "Flip Flop!"
WIDTH = 480
HEIGHT = 640
FPS = 60

HS_FILE = 'highscrore.txt'
# Player properties

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1.0
PLAYER_JUMP = 14

# Starting platforms
PLATFORM_LIST = []
# plat_len_delay = 500
# for i in range(3):
#     num = random.randrange(75, HEIGHT - 275)
#     PLATFORM_LIST.append((WIDTH + plat_len_delay, 0, num))
#     PLATFORM_LIST.append((WIDTH + plat_len_delay, num + 170, num + 350, False))
#     plat_len_delay += 260
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

