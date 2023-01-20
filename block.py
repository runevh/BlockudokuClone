import copy
import random

import util
import pygame
from enum import Enum

size = 30


class Block:
    name = "undefined"
    shape = []
    rotation = 0
    width = 0  # Total width in blocks
    height = 0  # Total height in blocks
    rect = (0, 0, size, size)

    def __init__(self, shape=None):
        if shape is None:
            self.shape = [[0, 0]]
        else:
            self.shape = shape

        largest_x = 0
        largest_y = 0
        for coord in self.shape:
            if coord[0] > largest_x:
                largest_x = coord[0]
            if coord[1] > largest_y:
                largest_y = coord[1]
        self.width = largest_x + 1
        self.height = largest_y + 1

    def new_rotation(self, rotation=-1):
        if rotation != -1:
            self.rotation = rotation
            return
        self.rotation = random.randint(0, 4)

    def get_width(self):
        if self.rotation == 0 or self.rotation == 2:
            return self.width
        else:
            return self.height

    def get_height(self):
        if self.rotation == 0 or self.rotation == 2:
            return self.height
        else:
            return self.width

    def render(self, screen, x, y, new_size=size):
        for coord in self.get_block_shape():
            pygame.draw.rect(screen, util.Color.BLACK.value,
                             pygame.Rect(x + coord[0] * new_size, y + coord[1] * new_size, new_size, new_size))

    def get_block_shape(self):
        rotated_shape = []
        if self.rotation == 0:
            return self.shape
        elif self.rotation == 1:
            for coord in self.shape:
                rotated_shape.append([coord[1], coord[0]])
        elif self.rotation == 2:
            for coord in self.shape:
                rotated_shape.append([self.width - 1 - coord[0], self.height - 1 - coord[1]])
        else:
            for coord in self.shape:
                rotated_shape.append([coord[1], self.width - 1 - coord[0]])

        return rotated_shape


def get_random_block(rotation=-1):
    raw = random.choice(blocks_types)
    block = raw.value
    block.name = raw.name
    block.new_rotation(rotation)
    block.rect = (0, 0, size * block.get_width(), size * block.get_height())
    return copy.deepcopy(block)


class Blocks(Enum):
    FIVE = Block([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]])
    FOUR = Block([[0, 0], [0, 1], [0, 2], [0, 3]])
    THREE = Block([[0, 0], [0, 1], [0, 2]])
    TWO = Block([[0, 0], [0, 1]])
    ONE = Block([[0, 0], [0, 1]])
    U = Block([[0, 1], [0, 0], [0, 1], [0, 2], [1, 2]])
    L = Block([[0, 2], [0, 1], [0, 0], [1, 0]])
    J = Block([[1, 2], [1, 1], [1, 0], [0, 0]])
    SMALL_L = Block([[0, 1], [0, 0], [1, 0]])
    SMALL_J = Block([[1, 1], [1, 0], [0, 0]])
    LONG_L = Block([[0, 2], [0, 1], [0, 0], [0, 1], [0, 2]])
    T_LONG = Block([[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]])
    T = Block([[0, 0], [0, 1], [0, 2], [1, 1]])
    TWO_DIAGONAL = Block([[0, 0], [1, 1]])
    THREE_DIAGONAL = Block([[0, 0], [1, 1], [2, 2]])
    Z = Block([[0, 1], [1, 1], [1, 0], [2, 0]])
    S = Block([[0, 0], [1, 0], [1, 1], [2, 1]])
    SQUARE = Block([[0, 0], [1, 0], [0, 1], [1, 1]])


blocks_types = list(Blocks)
