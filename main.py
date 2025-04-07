import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dobrodružstvo Gamebook")

# Load fonts
FONT = pygame.font.Font("medieval.ttf", 28)
BIG_FONT = pygame.font.Font("medieval.ttf", 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (160, 160, 160)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Load images
background_img = pygame.image.load("background_forest.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

sword_icon = pygame.image.load("sword.png").convert_alpha()
sword_icon = pygame.transform.scale(sword_icon, (64, 64))

# Load music
pygame.mixer.music.load("music.ogg")
pygame.mixer.music.play(-1)  # Loop forever
pygame.mixer.music.set_volume(0.5)

# Player stats
player_health = 100
inventory = []

# Story node class
class StoryNode:
    def __init__(self, text, options):
        self.text = text
        self.options = options  # List of dicts {text, next, health_change, item}

# Define story nodes (Slovak translation)
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

def render_with_outline(text, x, y, font=FONT, main_color=WHITE, outline_color=BLACK):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                screen.blit(outline, (x + dx, y + dy))
    main_text = font.render(text, True, main_color)
    screen.blit(main_text, (x, y))

def draw_text(text, x, y, max_width=700):
    words = text.split()
    line = ""
    y_offset = 0

    for word in words:
        if FONT.size(line + word)[0] > max_width:
            render_with_outline(line.strip(), x, y + y_offset)
            y_offset += 36
            line = ""
        line += word + " "
    render_with_outline(line.strip(), x, y + y_offset)

def draw_inventory():
    if "Meč" in inventory:
        screen.blit(sword_icon, (WIDTH - 90, HEIGHT - 90))  # pravý dolný roh
    inv_text = "Inventár: " + ", ".join(inventory) if inventory else "Inventár: (prázdny)"
    render_with_outline(inv_text, 20, HEIGHT - 60)

def draw_health():
    pygame.draw.rect(screen, RED, (20, 20, 200, 25))
    pygame.draw.rect(screen, GREEN, (20, 20, max(0, player_health) * 2, 25))
    render_with_outline(f"Zdravie: {player_health}", 230, 20)

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

def main():
    global current_node, player_health
    clock = pygame.time.Clock()

    while True:
        screen.blit(background_img, (0, 0))

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

        for i, option in enumerate(node.options):
            btn_rect = pygame.Rect(50, 300 + i * 60, 700, 45)
            color = DARK_GRAY if btn_rect.collidepoint(mouse) else LIGHT_GRAY
            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, btn_rect, 2, border_radius=8)
            render_with_outline(option["text"], btn_rect.x + 10, btn_rect.y + 8)

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
