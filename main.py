import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gamebook Adventure")

# Fonts
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Player stats
player_health = 100
inventory = []

# Story node class
class StoryNode:
    def __init__(self, text, options):
        self.text = text
        self.options = options  # List of dicts {text, next, health_change, item}

# Define story nodes
nodes = {
    "start": StoryNode(
        "You wake up in a forest. A sword lies nearby.",
        [
            {"text": "Take the sword", "next": "with_sword", "item": "Sword"},
            {"text": "Ignore the sword", "next": "no_sword"}
        ]
    ),
    "with_sword": StoryNode(
        "You feel safer with the sword. A wild beast attacks!",
        [
            {"text": "Fight", "next": "fight_beast", "health_change": -20},
            {"text": "Run", "next": "run_away", "health_change": -10}
        ]
    ),
    "no_sword": StoryNode(
        "You keep walking. A wild beast attacks!",
        [
            {"text": "Fight barehanded", "next": "fight_beast", "health_change": -40},
            {"text": "Run", "next": "run_away", "health_change": -10}
        ]
    ),
    "fight_beast": StoryNode(
        "You fought bravely. The beast is gone.",
        [
            {"text": "Continue", "next": "end"}
        ]
    ),
    "run_away": StoryNode(
        "You escaped, but you're hurt.",
        [
            {"text": "Continue", "next": "end"}
        ]
    ),
    "end": StoryNode(
        "Your adventure continues...",
        []
    )
}

current_node = "start"

def draw_text(text, x, y, max_width=700):
    words = text.split()
    line = ""
    y_offset = 0
    for word in words:
        if FONT.size(line + word)[0] > max_width:
            screen.blit(FONT.render(line, True, BLACK), (x, y + y_offset))
            y_offset += 30
            line = ""
        line += word + " "
    screen.blit(FONT.render(line, True, BLACK), (x, y + y_offset))

def draw_inventory():
    inv_text = "Inventory: " + ", ".join(inventory) if inventory else "Inventory: (empty)"
    screen.blit(FONT.render(inv_text, True, BLACK), (20, HEIGHT - 60))

def draw_health():
    pygame.draw.rect(screen, RED, (20, 20, 200, 25))
    pygame.draw.rect(screen, GREEN, (20, 20, max(0, player_health) * 2, 25))
    screen.blit(FONT.render(f"Health: {player_health}", True, WHITE), (230, 20))

def main():
    global current_node, player_health

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        node = nodes[current_node]
        draw_text(node.text, 20, 70)
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

        # Draw buttons
        for i, option in enumerate(node.options):
            btn_rect = pygame.Rect(50, 300 + i * 60, 700, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, btn_rect)
            text = FONT.render(option["text"], True, BLACK)
            screen.blit(text, (btn_rect.x + 10, btn_rect.y + 5))

            if btn_rect.collidepoint(mouse) and click:
                if "health_change" in option:
                    player_health += option["health_change"]
                if "item" in option:
                    inventory.append(option["item"])
                current_node = option["next"]
                break

        pygame.display.flip()
        clock.tick(60)

main()
