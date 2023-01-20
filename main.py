import random

import pygame

import block
import util
import game

running = True
last_rendered_fps = util.get_current_millis()
test_block = block.get_random_block()


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((400, 600))
    clock = pygame.time.Clock()
    game.init_blocks()
    while running:
        fps = round(clock.get_fps())
        screen.fill(util.Color.WHITE.value)
        render_fps(screen, fps)
        check_events()
        clock.tick()
        game.render(screen)
        game.update_hold(screen)
        pygame.display.flip()
    pygame.quit()


last_shown_fps = 0


def render_fps(screen, fps):
    global last_rendered_fps, last_shown_fps
    if (util.get_current_millis() - last_rendered_fps) < 100:
        util.renderText(screen, "FPS: {0}".format(last_shown_fps), 5, 5)
        return
    last_shown_fps = fps
    util.renderText(screen, "FPS: {0}".format(fps), 5, 5)

    last_rendered_fps = util.get_current_millis()


def check_events():
    global running, test_block
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.start_hold()
        elif event.type == pygame.MOUSEBUTTONUP:
            game.stop_hold()

if __name__ == '__main__':
    main()
