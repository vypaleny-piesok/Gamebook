import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dobrodružstvo Gamebook")

# Fonts
FONT = pygame.font.Font("medieval.ttf", 28)
BIG_FONT = pygame.font.Font("medieval.ttf", 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (160, 160, 160)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Background image and music
background_img = pygame.image.load("background_forest.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pygame.mixer.music.load("music.ogg")
pygame.mixer.music.play(-1)

# Icons
sword_icon = pygame.image.load("sword.png").convert_alpha()
sword_icon = pygame.transform.scale(sword_icon, (64, 64))
inventory_icon = pygame.image.load("inventory_icon.png").convert_alpha()
inventory_icon = pygame.transform.scale(inventory_icon, (48, 48))
leaf_img = pygame.image.load("leaf.png").convert_alpha()
leaf_img = pygame.transform.scale(leaf_img, (32, 32))

# Player stats
player_health = 100
inventory = []
show_inventory = False

# Falling leaves setup (adjusted for fewer leaves)
leaves = []
for _ in range(random.randint(2, 4)):  # Now only 2–4 leaves
    leaf = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(-HEIGHT, 0),
        "speed": random.uniform(0.2, 0.6),
        "img": leaf_img
    }
    leaves.append(leaf)

# Story node class
class StoryNode:
    def __init__(self, text, options):
        self.text = text
        self.options = options

# Define story nodes
nodes = {
    "start": StoryNode(
        "Zobudíš sa v lese. Neďaleko leží meč.",
        [
            {"text": "Zobrať meč", "next": "with_sword", "item": "Meč"},
            {"text": "Ignorovať meč", "next": "no_sword"}
        ]
    ),
    "with_sword": StoryNode(
        "Cítiš sa bezpečnejšie s mečom. Útočí na teba divé zviera!",
        [
            {"text": "Bojovať", "next": "fight_beast", "health_change": -20},
            {"text": "Utiecť", "next": "run_away", "health_change": -10}
        ]
    ),
    "no_sword": StoryNode(
        "Kráčaš ďalej. Zrazu ťa napadne divé zviera!",
        [
            {"text": "Bojovať holými rukami", "next": "fight_beast", "health_change": -40},
            {"text": "Utiecť", "next": "run_away", "health_change": -10}
        ]
    ),
    "fight_beast": StoryNode(
        "Bojoval si statočne. Zviera je porazené.",
        [
            {"text": "Pokračovať", "next": "end"}
        ]
    ),
    "run_away": StoryNode(
        "Utiekol si, ale si zranený.",
        [
            {"text": "Pokračovať", "next": "end"}
        ]
    ),
    "end": StoryNode(
        "Tvoje dobrodružstvo pokračuje...",
        []
    )
}

current_node = "start"

# Draw outlined text
def draw_text(text, x, y, max_width=700):
    words = text.split()
    line = ""
    y_offset = 0
    for word in words:
        if FONT.size(line + word)[0] > max_width:
            draw_outline_text(line.strip(), x, y + y_offset)
            y_offset += 35
            line = ""
        line += word + " "
    draw_outline_text(line.strip(), x, y + y_offset)

def draw_outline_text(text, x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                screen.blit(FONT.render(text, True, BLACK), (x + dx, y + dy))
    screen.blit(FONT.render(text, True, WHITE), (x, y))

def draw_inventory():
    if show_inventory:
        pygame.draw.rect(screen, (0, 0, 0, 180), (WIDTH - 150, HEIGHT - 200, 140, 140))
        if "Meč" in inventory:
            sword_rect = screen.blit(sword_icon, (WIDTH - 130, HEIGHT - 180))
            if sword_rect.collidepoint(pygame.mouse.get_pos()):
                draw_outline_text("Meč", WIDTH - 130, HEIGHT - 110)


def draw_health():
    pygame.draw.rect(screen, RED, (20, 20, 200, 25))
    pygame.draw.rect(screen, GREEN, (20, 20, max(0, player_health) * 2, 25))
    draw_outline_text(f"Zdravie: {player_health}", 230, 20)

def damage_flash():
    flash_surface = pygame.Surface((WIDTH, HEIGHT))
    flash_surface.set_alpha(120)
    flash_surface.fill((255, 0, 0))
    screen.blit(flash_surface, (0, 0))
    pygame.display.flip()
    pygame.time.delay(150)

def item_flash():
    flash_surface = pygame.Surface((WIDTH, HEIGHT))
    flash_surface.set_alpha(100)
    flash_surface.fill((0, 255, 0))
    screen.blit(flash_surface, (0, 0))
    pygame.display.flip()
    pygame.time.delay(150)

def fade_transition():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 15):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


# Function to draw leaves on screen
def draw_leaves():
    for leaf in leaves:
        screen.blit(leaf["img"], (leaf["x"], leaf["y"]))  # Correct access to 'x' and 'y' keys
        leaf["y"] += leaf["speed"]

        # Reset leaf position once it goes off screen
        if leaf["y"] > HEIGHT:
            leaf["y"] = random.randint(-HEIGHT, -20)
            leaf["x"] = random.randint(0, WIDTH)


def main():
    global current_node, player_health, show_inventory

    clock = pygame.time.Clock()

    while True:
        screen.blit(background_img, (0, 0))
        draw_leaves()

        node = nodes[current_node]
        draw_text(node.text, 20, 80)
        draw_health()
        draw_inventory()

        mouse = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if inventory_icon_rect.collidepoint(mouse):
                    show_inventory = not show_inventory

        # Inventory icon
        inventory_icon_rect = screen.blit(inventory_icon, (WIDTH - 60, 10))

        # Draw buttons with hover
        for i, option in enumerate(node.options):
            btn_rect = pygame.Rect(50, 300 + i * 60, 700, 45)
            color = DARK_GRAY if btn_rect.collidepoint(mouse) else LIGHT_GRAY
            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, btn_rect, 2, border_radius=8)
            draw_outline_text(option["text"], btn_rect.x + 10, btn_rect.y + 10)

            if btn_rect.collidepoint(mouse) and click:
                if "health_change" in option:
                    change = option["health_change"]
                    if change < 0:
                        damage_flash()
                    player_health += change
                if "item" in option:
                    inventory.append(option["item"])
                    item_flash()
                fade_transition()
                current_node = option["next"]
                break

        pygame.display.flip()
        clock.tick(60)

main()
