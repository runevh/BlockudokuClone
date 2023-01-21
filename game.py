import random
from math import floor

import pygame
import util
import block

offset = [400 / 2 - (block.size * 9 + 2) / 2, 50]
occupied_blocks = []  # Rows
new_blocks = []


def init_blocks():
    generate_new_blocks()
    for _ in range(9):
        row = []
        for _ in range(9):
            row.append(0)
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
    x = coords[0] - ((selected_block.get_width() * block.size) / 2)
    y = coords[1] - ((selected_block.get_height() * block.size) / 2)

    for r in get_free_places():
        pygame.draw.rect(screen, util.Color.LIGHTGRAY.value,
                         pygame.Rect(offset[0] + (r[0]) * block.size, offset[1] + (r[1]) * block.size, block.size,
                                     block.size))

    selected_block.render(screen, x, y)


def get_raster_block(x_cord, y_cord):
    if x_cord - offset[0] < 0:
        return -1
    if y_cord - offset[1] < 0:
        return -1
    x = int((x_cord - offset[0]) / block.size)
    y = int((y_cord - offset[1]) / block.size)
    if x > 8 or y > 8:
        return -1
    return x, y


def get_block_state(x_cord, y_cord):
    occ = occupied_blocks[y_cord][x_cord]
    return occ


def get_free_places():
    temp_r = []
    if selected_block == 0:
        return temp_r

    coords = pygame.mouse.get_pos()
    x = coords[0] - ((selected_block.get_width() * block.size) / 2)
    y = coords[1] - ((selected_block.get_height() * block.size) / 2)

    for bb in selected_block.get_block_shape():
        mid_x = x + bb[0] * block.size + block.size / 2
        mid_y = y + bb[1] * block.size + block.size / 2
        r = get_raster_block(mid_x, mid_y)
        if r == -1:
            temp_r = []
            break
        if get_block_state(r[0], r[1]) == 1:
            temp_r = []
            break
        temp_r.append(r)

    return temp_r


def stop_hold():
    global held, selected_block, temp_index
    held = False
    new_blocks[temp_index] = selected_block

    for r in get_free_places():
        occupied_blocks[r[1]][r[0]] = 1

    selected_block = 0
    temp_index = -1


def update_removal():
    rows_n = check_rows_for_completion()
    collums = check_collums_for_completion()
    squares = check_squares_for_completion()
    remove_culloms(collums)
    remove_rows(rows_n)


def check_squares_for_completion():
    result = []
    # int(len(occupied_blocks) / 3)
    temp = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in range(3):
        for j in range(3):
            y = i * 3 + j
            for x in range(0, 9):
                square = i * 3 + int(floor(x / 3))
                if temp[square] == 0:
                    continue
                temp[square] = occupied_blocks[y][x]
                if j == 2 and 0 == (x + 1) % 3:
                    if temp[square] == 1:
                        result.append(square)

    return result


def check_rows_for_completion():
    # Check for rows
    n_rows = []
    for i in range(len(occupied_blocks)):
        row_complete = True
        rows = occupied_blocks[i]
        for x in rows:
            if x == 0:
                row_complete = False
                break
        if row_complete:
            print(i)
            n_rows.append(i)
    return n_rows


def check_collums_for_completion():
    # Check for rows
    collums = []
    temp = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for y in range(len(occupied_blocks)):
        row = occupied_blocks[y]
        for x in range(len(row)):
            if temp[x] == 0:
                continue
            temp[x] = row[x]
            if y == 8:
                if row[x] == 1:
                    collums.append(x)
    return collums


def remove_culloms(culloms):
    global occupied_blocks
    for y in range(len(occupied_blocks)):
        for x in culloms:
            occupied_blocks[y][x] = 0


def remove_rows(rows):
    for y in rows:
        row = occupied_blocks[y]
        for x in range(len(row)):
            occupied_blocks[y][x] = 0


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
