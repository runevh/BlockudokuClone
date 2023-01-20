import random
import pygame
import util
import block

offset = [400 / 2 - (block.size * 9 + 2) / 2, 50]
occupied_blocks = []  # Rows
new_blocks = []


def init_blocks():
    generate_new_blocks()
    for _ in range(0, 9):
        row = []
        for _ in range(0, 9):
            row.append(random.randint(0, 1))
        occupied_blocks.append(row)


def render_blocks(screen):
    for y in range(0, len(occupied_blocks)):
        row = occupied_blocks[y]
        for x in range(0, len(row)):
            if row[x] == 1:
                pygame.draw.rect(screen, util.Color.BLACK.value,
                                 pygame.Rect(offset[0] + x * block.size, offset[1] + y * block.size, block.size,
                                             block.size))


def generate_new_blocks():
    new_blocks.clear()
    for _ in range(0, 3):
        new_blocks.append(block.get_random_block())


def render_new_blocks(screen):
    for i in range(0, 3):
        b = new_blocks[i]
        if b == 0:
            continue

        b.render(screen, (400 / 3) * (i + 1) - ((b.get_width() * 23) / 2) - 400 / 6, 395 - ((b.get_height() * 23) / 2),
                 23)


held = False
selected_block = 0
temp_index = -1


def is_clicked(coords, i, b):
    if b == 0:
        return False

    x = coords[0]
    y = coords[1]
    left = (400 / 3) * (i + 1) - (b.get_width() * 23) / 2 - 400 / 6
    if x < left:
        return False
    if x > left + b.get_width() * 23:
        return False
    top = 395 - ((b.get_height() * 23) / 2)
    if y < top:
        return False
    if y > top + b.get_height() * 23:
        return False

    return True


def start_hold():
    global selected_block, held, temp_index
    held = True
    coords = pygame.mouse.get_pos()
    for i in range(0, 3):
        b = new_blocks[i]
        if not is_clicked(coords, i, b):
            continue
        selected_block = b
        temp_index = i
        new_blocks[i] = 0
        break


def update_hold(screen):
    if not held:
        return

    if selected_block == 0:
        return
    coords = pygame.mouse.get_pos()
    selected_block.render(screen, coords[0] - ((selected_block.get_width() * block.size) / 2),
                          coords[1] - ((selected_block.get_height() * block.size) / 2))

    # offset[0] + x * block.size, offset[1] + y * block.size


def stop_hold():
    global held, selected_block, temp_index
    held = False
    new_blocks[temp_index] = selected_block
    selected_block = 0
    temp_index = -1


def render(screen):
    render_blocks(screen)
    render_new_blocks(screen)
    for x in range(0, 10):
        color = util.Color.LIGHTGRAY.value
        line_width = 1
        if x % 3 == 0:
            color = util.Color.DARKGRAY.value
            line_width = 2
        pygame.draw.rect(screen, color,
                         pygame.Rect(offset[0] + x * block.size, offset[1], line_width, block.size * 9 + 2))
        pygame.draw.rect(screen, color,
                         pygame.Rect(offset[0], offset[1] + x * block.size, block.size * 9 + 2, line_width))
