#!/usr/bin/env python3
"""
Create PROUTMAN splash screen from existing assets.
"""

import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 1024, 768

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (124, 252, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# Create surface
screen = pygame.Surface((WIDTH, HEIGHT))

# Draw sky background
screen.fill(SKY_BLUE)

# Draw grass at bottom
pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 200, WIDTH, 200))

# Draw game board pattern
board_y = HEIGHT - 300
board_height = 250
tile_size = 50

for y in range(board_y, board_y + board_height, tile_size):
    for x in range(100, WIDTH - 100, tile_size):
        # Checkerboard pattern
        if ((x // tile_size) + (y // tile_size)) % 2 == 0:
            color = (160, 120, 80)
        else:
            color = (180, 140, 100)
        pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
        pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 2)

# Draw clouds
cloud_font = pygame.font.Font(None, 120)
for x, y in [(150, 80), (400, 120), (700, 90), (850, 130)]:
    cloud = cloud_font.render("☁️", True, WHITE)
    screen.blit(cloud, (x, y))

# Draw sun
sun_font = pygame.font.Font(None, 150)
sun = sun_font.render("☀️", True, YELLOW)
screen.blit(sun, (WIDTH - 200, 50))

# Draw title with outline
title_font = pygame.font.Font(None, 150)
title_text = "PROUTMAN"

# Draw outline
for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
    outline = title_font.render(title_text, True, BLACK)
    screen.blit(outline, (WIDTH // 2 - 350 + dx, 100 + dy))

# Draw main title with gradient effect
title_colors = [ORANGE, YELLOW, ORANGE]
for i, color in enumerate(title_colors):
    offset = i * 2
    title = title_font.render(title_text, True, color)
    screen.blit(title, (WIDTH // 2 - 350 + offset, 100 + offset))

# Draw cloud in "O" of PROUT
cloud_small = pygame.font.Font(None, 80)
cloud_o = cloud_small.render("☁️", True, WHITE)
screen.blit(cloud_o, (WIDTH // 2 - 80, 115))

# Draw subtitle
subtitle_font = pygame.font.Font(None, 70)
subtitle = subtitle_font.render("L'aventure Codée!", True, BROWN)
subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 250))
screen.blit(subtitle, subtitle_rect)

# Draw cacas on the board
caca_font = pygame.font.Font(None, 100)
caca_positions = [
    (200, board_y + 80),
    (350, board_y + 130),
    (500, board_y + 80),
    (650, board_y + 130),
    (800, board_y + 80),
]

for x, y in caca_positions:
    # Draw shadow
    shadow = caca_font.render("💩", True, (50, 50, 50))
    screen.blit(shadow, (x + 5, y + 5))
    # Draw caca
    caca = caca_font.render("💩", True, BROWN)
    screen.blit(caca, (x, y))

# Draw character placeholder (green circle with mask)
char_x, char_y = WIDTH // 2, board_y + 50
pygame.draw.circle(screen, (100, 200, 100), (char_x, char_y), 60)
pygame.draw.circle(screen, BLACK, (char_x, char_y), 60, 3)

# Draw mask
pygame.draw.ellipse(screen, (50, 150, 50), (char_x - 50, char_y - 20, 100, 40))
pygame.draw.ellipse(screen, BLACK, (char_x - 50, char_y - 20, 100, 40), 2)

# Draw eyes
pygame.draw.circle(screen, WHITE, (char_x - 20, char_y - 10), 12)
pygame.draw.circle(screen, WHITE, (char_x + 20, char_y - 10), 12)
pygame.draw.circle(screen, BLACK, (char_x - 20, char_y - 10), 6)
pygame.draw.circle(screen, BLACK, (char_x + 20, char_y - 10), 6)

# Draw lightning bolt on chest
bolt_points = [
    (char_x - 10, char_y + 10),
    (char_x + 5, char_y + 20),
    (char_x - 5, char_y + 20),
    (char_x + 10, char_y + 30),
]
pygame.draw.polygon(screen, YELLOW, bolt_points)
pygame.draw.polygon(screen, ORANGE, bolt_points, 2)

# Draw prout cloud
prout_font = pygame.font.Font(None, 90)
prout_cloud = prout_font.render("PROUT!", True, WHITE)
prout_rect = prout_cloud.get_rect()
prout_rect.center = (char_x + 150, char_y - 50)

# Draw cloud background
pygame.draw.ellipse(screen, WHITE, prout_rect.inflate(40, 30))
pygame.draw.ellipse(screen, BLACK, prout_rect.inflate(40, 30), 3)
screen.blit(prout_cloud, prout_rect)

# Draw description
desc_font = pygame.font.Font(None, 40)
descriptions = [
    "Pour Apprendre à Coder et S'Amuser!",
    "Création de Jeu & Apprentissage Renforcé",
]

y = 350
for desc in descriptions:
    text = desc_font.render(desc, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, y))
    screen.blit(text, text_rect)
    y += 45

# Draw game instructions with emojis
inst_font = pygame.font.Font(None, 35)
instructions = [
    "💨 Drop Prouts (Trumps) to destroy walls",
    "💩 Place Cacas to block enemies",
    "🎯 Collect power-ups and defeat AI",
]

y = 480
for inst in instructions:
    text = inst_font.render(inst, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, y))
    # Draw white background for readability
    bg_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(screen, WHITE, bg_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, bg_rect, 2, border_radius=10)
    screen.blit(text, text_rect)
    y += 40

# Draw "START GAME" button
button_font = pygame.font.Font(None, 60)
button_text = button_font.render("START GAME", True, WHITE)
button_rect = button_text.get_rect(center=(WIDTH // 2 - 150, HEIGHT - 80))
button_bg = button_rect.inflate(40, 20)
pygame.draw.rect(screen, ORANGE, button_bg, border_radius=15)
pygame.draw.rect(screen, BLACK, button_bg, 4, border_radius=15)
screen.blit(button_text, button_rect)

# Draw "OPTIONS" button
options_text = button_font.render("OPTIONS", True, WHITE)
options_rect = options_text.get_rect(center=(WIDTH // 2 + 150, HEIGHT - 80))
options_bg = options_rect.inflate(40, 20)
pygame.draw.rect(screen, (100, 150, 255), options_bg, border_radius=15)
pygame.draw.rect(screen, BLACK, options_bg, 4, border_radius=15)
screen.blit(options_text, options_rect)

# Add decorative characters (purple and orange friends)
friend_font = pygame.font.Font(None, 80)

# Purple friend
purple_x, purple_y = 150, board_y + 100
pygame.draw.rect(screen, (150, 100, 200), (purple_x, purple_y, 60, 80), border_radius=10)
pygame.draw.rect(screen, BLACK, (purple_x, purple_y, 60, 80), 3, border_radius=10)
# Eyes
pygame.draw.circle(screen, WHITE, (purple_x + 15, purple_y + 25), 8)
pygame.draw.circle(screen, WHITE, (purple_x + 45, purple_y + 25), 8)
pygame.draw.circle(screen, BLACK, (purple_x + 15, purple_y + 25), 4)
pygame.draw.circle(screen, BLACK, (purple_x + 45, purple_y + 25), 4)
# Smile
pygame.draw.arc(screen, BLACK, (purple_x + 10, purple_y + 30, 40, 30), 3.14, 0, 3)

# Orange friend
orange_x, orange_y = WIDTH - 210, board_y + 100
pygame.draw.rect(screen, ORANGE, (orange_x, orange_y, 60, 80), border_radius=10)
pygame.draw.rect(screen, BLACK, (orange_x, orange_y, 60, 80), 3, border_radius=10)
# Eyes
pygame.draw.circle(screen, WHITE, (orange_x + 15, orange_y + 25), 8)
pygame.draw.circle(screen, WHITE, (orange_x + 45, orange_y + 25), 8)
pygame.draw.circle(screen, BLACK, (orange_x + 15, orange_y + 25), 4)
pygame.draw.circle(screen, BLACK, (orange_x + 45, orange_y + 25), 4)
# Smile
pygame.draw.arc(screen, BLACK, (orange_x + 10, orange_y + 30, 40, 30), 3.14, 0, 3)

# Save the image
output_path = "bomber_game/assets/images/proutman_splash.jpg"
pygame.image.save(screen, output_path)

print(f"✅ Splash screen created: {output_path}")
print(f"📏 Size: {WIDTH}x{HEIGHT}")
print(f"🎨 Theme: PROUTMAN - L'aventure Codée!")
print(f"\n🎮 Now run: ./launch_bomberman.sh")

pygame.quit()
