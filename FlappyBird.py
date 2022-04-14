import os
import random
import pygame

# Const Variables

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))

FLOOR_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

BIRD_IMG = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

RESTART_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'restart.png')))

SCORE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'score.png')))

pygame.font.init()

SCORE_FONT = pygame.font.SysFont('arial', 40)


class Bird:
    IMGS = BIRD_IMG

    # rotation animations

    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0
        self.img_counter = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calc the displacement
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.velocity * self.time

        # limit the displacement
        if displacement > 16:
            displacement = 16

        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # bird angle
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_VELOCITY

    def draw_bird(self, screen):

        # define which image will be used
        self.img_counter += 1

        if self.img_counter < self.ANIMATION_TIME:
            self.image = self.IMGS[0]

        elif self.img_counter < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]

        elif self.img_counter < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]

        elif self.img_counter < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]

        elif self.img_counter >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.img_counter = 0

        # if bird be downing, won't flap wings
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.img_counter = self.ANIMATION_TIME * 2

        # draw the image
        image_rotated = pygame.transform.rotate(self.image, self.angle)
        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = image_rotated.get_rect(center=pos_center_image)
        screen.blit(image_rotated, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.position_top = 0
        self.position_base = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BASE = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.position_top = self.height - self.PIPE_TOP.get_height()
        self.position_base = self.height + self.DISTANCE

    def move_pipe(self):
        self.x -= self.VELOCITY

    def draw_pipe(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.position_top))
        screen.blit(self.PIPE_BASE, (self.x, self.position_base))

    def pipe_collision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        distance_top = (self.x - bird.x, self.position_top - round(bird.y))
        distance_base = (self.x - bird.x, self.position_base - round(bird.y))

        base_point = bird_mask.overlap(base_mask, distance_base)
        top_point = bird_mask.overlap(top_mask, distance_top)

        if base_point or top_point:
            return True
        else:
            return False


class Floor:
    VELOCITY = 5
    WIDTH = FLOOR_IMG.get_width()
    IMAGE = FLOOR_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move_floor(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw_floor(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


# Auxiliary Functions

def draw_screen(screen, birds, pipes, floor, score):
    screen.blit(BACKGROUND_IMG, (0, 0))
    for bird in birds:
        bird.draw_bird(screen)

    for pipe in pipes:
        pipe.draw_pipe(screen)

    text = SCORE_FONT.render(f"Score: {score}", True, 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    floor.draw_floor(screen)
    pygame.display.update()


def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    timer = pygame.time.Clock()
    playing = True

    while playing:
        timer.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        # Moving items

        for bird in birds:
            bird.move()
        floor.move_floor()

        add_pipe = False
        delete_pipe = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.pipe_collision(bird):
                    birds.pop(i)

                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move_pipe()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                delete_pipe.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for pipe in delete_pipe:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, score)


if __name__ == '__main__':
    main()
