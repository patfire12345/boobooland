import pygame
import sys
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Big Booboo & Baby Booboo Waddling in the Field")

# Colors
SKY = (135, 206, 235)
GRASS = (60, 179, 113)
SUN = (255, 223, 0)
SUN_RAY_COLOR = (255, 240, 100)
TEXT_COLOR = (0, 0, 0)
BUBBLE_COLOR = (255, 255, 255, 220)

# Load images
big_booboo_img = pygame.image.load("big_booboo.jpg").convert_alpha()
baby_booboo_img = pygame.image.load("baby_booboo.jpeg").convert_alpha()
squirrel_img = pygame.image.load("squirrel.jpg").convert_alpha()  # add a squirrel image

# Utility functions
def scale_proportionally(img, height=None):
    w, h = img.get_size()
    if height:
        ratio = height / h
        return pygame.transform.smoothscale(img, (int(w * ratio), height))
    return img

def crop_subsection(img, top_crop=0, bottom_crop=0):
    w, h = img.get_size()
    rect = pygame.Rect(0, top_crop, w, h - top_crop - bottom_crop)
    cropped = pygame.Surface((w, rect.height), pygame.SRCALPHA)
    cropped.blit(img, (0, 0), rect)
    return cropped

def crop_to_ellipse(image, padding=5):
    w, h = image.get_size()
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(mask, (255, 255, 255, 255),
                        (padding, padding, w - 2*padding, h - 2*padding))
    new_img = pygame.Surface((w, h), pygame.SRCALPHA)
    new_img.blit(image, (0, 0))
    new_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return new_img

# Prepare plushies
big_booboo_img = crop_subsection(big_booboo_img, 150, 40)
big_booboo_img = scale_proportionally(big_booboo_img, 300)
big_booboo_img = crop_to_ellipse(big_booboo_img, 15)

baby_booboo_img = scale_proportionally(baby_booboo_img, 180)
baby_booboo_img = crop_to_ellipse(baby_booboo_img, 10)

# Scale squirrel 25% smaller
squirrel_img = scale_proportionally(squirrel_img, int(150 * 0.75))
# Move squirrel to middle of the screen vertically
squirrel_rect = squirrel_img.get_rect(topleft=(50, HEIGHT//2 - squirrel_img.get_height()//2))


# Starting positions
big_x, big_y = 150, HEIGHT - 350
baby_x, baby_y = -150, HEIGHT - 250

# Speeds
big_speed = 1.5
baby_speed = 2.3

# Frame control
clock = pygame.time.Clock()
frame = 0

# Font with emoji support
try:
    font = pygame.font.SysFont("Segoe UI Emoji", 36)
except:
    font = pygame.font.SysFont(None, 36)

# Speech bubble storage: [text, target, timer]
click_messages = []

# Dragging state
dragging = None
drag_offset_x, drag_offset_y = 0, 0

# Speech bubble function
def draw_speech_bubble(surface, text, center_pos):
    text_surf = font.render(text, True, TEXT_COLOR)
    padding_x, padding_y = 10, 6
    bubble_width = text_surf.get_width() + 2 * padding_x
    bubble_height = text_surf.get_height() + 2 * padding_y
    bubble_surf = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
    pygame.draw.ellipse(bubble_surf, BUBBLE_COLOR, (0, 0, bubble_width, bubble_height))
    bubble_surf.blit(text_surf, (padding_x, padding_y))
    bubble_rect = bubble_surf.get_rect(center=center_pos)
    surface.blit(bubble_surf, bubble_rect.topleft)

# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if big_rect.collidepoint(mouse_pos):
                    dragging = "big"
                    drag_offset_x = big_rect.centerx - mouse_pos[0]
                    drag_offset_y = big_rect.centery - mouse_pos[1]
                    click_messages.append(["Sad Booboo 😢", "big", 120])
                elif baby_rect.collidepoint(mouse_pos):
                    dragging = "baby"
                    drag_offset_x = baby_rect.centerx - mouse_pos[0]
                    drag_offset_y = baby_rect.centery - mouse_pos[1]
                    click_messages.append(["Sad Baby Booboo 😢", "baby", 120])
                elif squirrel_rect.collidepoint(mouse_pos):
                    click_messages.append(["Booboo friend!", "squirrel", 120])
                else:
                    if big_rect.collidepoint(mouse_pos):
                        click_messages.append(["Big Booboo!", "big", 120])
                    elif baby_rect.collidepoint(mouse_pos):
                        click_messages.append(["Baby Booboo!", "baby", 120])
            elif event.button == 3:  # Right click
                if big_rect.collidepoint(mouse_pos):
                    click_messages.append(["Big Booboo", "big", 120])
                elif baby_rect.collidepoint(mouse_pos):
                    click_messages.append(["Baby Booboo", "baby", 120])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging == "big":
                # Remove any sad message
                click_messages = [msg for msg in click_messages if not (msg[1] == "big" and "Sad" in msg[0])]
                click_messages.append(["Happy Booboo! 😄", "big", 120])
            elif dragging == "baby":
                click_messages = [msg for msg in click_messages if not (msg[1] == "baby" and "Sad" in msg[0])]
                click_messages.append(["Happy Baby Booboo! 😄", "baby", 120])
            dragging = None

    # Background
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, HEIGHT//2, WIDTH, HEIGHT//2))

    # Sun with rays
    sun_center = (WIDTH - 100, 100)
    sun_radius = 60
    pygame.draw.circle(screen, SUN, sun_center, sun_radius)
    for i in range(12):
        angle = math.radians(i * 30 + frame)
        x1 = sun_center[0] + math.cos(angle) * (sun_radius + 10)
        y1 = sun_center[1] + math.sin(angle) * (sun_radius + 10)
        x2 = sun_center[0] + math.cos(angle) * (sun_radius + 30)
        y2 = sun_center[1] + math.sin(angle) * (sun_radius + 30)
        pygame.draw.line(screen, SUN_RAY_COLOR, (x1, y1), (x2, y2), 3)

    # Update positions if not dragging
    if dragging != "big":
        big_x += big_speed
    if dragging != "baby":
        baby_x += baby_speed
    frame += 1

    # Waddling offsets & tilt
    if dragging != "big":
        big_offset = math.sin(frame * 0.1) * 10
        big_tilt = math.sin(frame * 0.1) * 7
    else:
        big_offset = 0
        big_tilt = 180

    if dragging != "baby":
        baby_offset = math.sin(frame * 0.15) * 6
        baby_tilt = math.sin(frame * 0.15) * 10
    else:
        baby_offset = 0
        baby_tilt = 180

    # Reset positions
    if big_x > WIDTH and dragging != "big":
        big_x = -big_booboo_img.get_width()
    if baby_x > WIDTH and dragging != "baby":
        baby_x = -baby_booboo_img.get_width()

    # Draw plushies
    rotated_big = pygame.transform.rotozoom(big_booboo_img, -big_tilt, 1)
    rotated_baby = pygame.transform.rotozoom(baby_booboo_img, -baby_tilt, 1)

    if dragging == "big":
        big_rect = rotated_big.get_rect(center=(mouse_pos[0] + drag_offset_x, mouse_pos[1] + drag_offset_y))
        big_x, big_y = big_rect.topleft
    else:
        big_rect = rotated_big.get_rect(center=(big_x + big_booboo_img.get_width()//2 + big_offset,
                                                big_y + big_booboo_img.get_height()//2))
    if dragging == "baby":
        baby_rect = rotated_baby.get_rect(center=(mouse_pos[0] + drag_offset_x, mouse_pos[1] + drag_offset_y))
        baby_x, baby_y = baby_rect.topleft
    else:
        baby_rect = rotated_baby.get_rect(center=(baby_x + baby_booboo_img.get_width()//2 + baby_offset,
                                                  baby_y + baby_booboo_img.get_height()//2))

    screen.blit(rotated_big, big_rect.topleft)
    screen.blit(rotated_baby, baby_rect.topleft)
    screen.blit(squirrel_img, squirrel_rect.topleft)

    # Draw speech bubbles
    for msg in click_messages[:]:
        text, target, timer = msg
        if target == "big":
            bubble_pos = (big_rect.centerx, big_rect.top - 30)
        elif target == "baby":
            bubble_pos = (baby_rect.centerx, baby_rect.top - 30)
        elif target == "squirrel":
            bubble_pos = (squirrel_rect.centerx, squirrel_rect.top - 30)
        draw_speech_bubble(screen, text, bubble_pos)
        msg[2] -= 1
        if msg[2] <= 0:
            click_messages.remove(msg)

    pygame.display.flip()
    clock.tick(60)
