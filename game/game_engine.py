import pygame
import random
from game.ship import Ship
from game.meteor import Meteor

WIDTH, HEIGHT = 700, 520
FPS = 60
BG = (8, 5, 20)


class Laser:
    """Simple defensive projectile fired by the player's ship."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x - 3,
            y - 10,
            6,
            14
        )
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

    def off_screen(self):
        return self.rect.bottom < 0

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 80, 80),
            self.rect
        )


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Meteor Dodge"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            26,
            bold=True
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            46,
            bold=True
        )

        self.stars = [
            (
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(1, 3)
            )
            for _ in range(80)
        ]

        self.reset()

    def reset(self):
        self.ship = Ship(
            WIDTH // 2,
            HEIGHT - 80
        )

        self.meteors = []
        self.lasers = []

        self.timer = 0
        self.spawn_interval = 60
        self.score = 0

        self.game_over = False
        self.started = False

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    # Launch the game
                    if (
                        not self.started
                        and not self.game_over
                    ):
                        self.started = True

                    # Restart after game over
                    elif self.game_over:
                        self.reset()

                    # Fire laser during active gameplay
                    else:
                        self.lasers.append(
                            Laser(
                                self.ship.rect.centerx,
                                self.ship.rect.top
                            )
                        )

        return True

    def update(self):

        if self.game_over or not self.started:
            return

        # Move ship
        keys = pygame.key.get_pressed()

        self.ship.move(
            keys,
            WIDTH,
            HEIGHT
        )

        # Increase timer
        self.timer += 1

        # Spawn meteors
        if self.timer >= self.spawn_interval:

            self.meteors.append(
                Meteor(WIDTH)
            )

            self.timer = 0

            self.spawn_interval = max(
                20,
                self.spawn_interval - 0.3
            )

        # Update meteors
        for meteor in self.meteors:

            meteor.update()

            # Meteor hits ship
            if meteor.collides(
                self.ship.rect
            ):
                self.game_over = True

        # Update lasers
        for laser in self.lasers:
            laser.update()

        # --------------------------------
        # LASER + METEOR COLLISIONS
        # --------------------------------

        remaining_meteors = []
        used_lasers = set()

        for meteor in self.meteors:

            destroyed = False

            for laser_index, laser in enumerate(
                self.lasers
            ):

                if laser_index in used_lasers:
                    continue

                dx = (
                    laser.rect.centerx
                    - meteor.x
                )

                dy = (
                    laser.rect.centery
                    - meteor.y
                )

                distance = (
                    dx ** 2 + dy ** 2
                ) ** 0.5

                if distance < meteor.radius:

                    destroyed = True
                    used_lasers.add(
                        laser_index
                    )

                    # --------------------------------
                    # LARGE METEOR → TWO SMALL METEORS
                    # --------------------------------

                    fragments = meteor.split()

                    if fragments:
                        remaining_meteors.extend(
                            fragments
                        )

                    # Small meteor simply disappears
                    break

            if not destroyed:
                remaining_meteors.append(
                    meteor
                )

        self.meteors = remaining_meteors

        # Remove lasers that have been used
        # or have left the screen
        self.lasers = [
            laser
            for index, laser in enumerate(
                self.lasers
            )
            if (
                index not in used_lasers
                and not laser.off_screen()
            )
        ]

        # Remove meteors below screen
        self.meteors = [
            meteor
            for meteor in self.meteors
            if not meteor.off_screen(HEIGHT)
        ]

        # Score
        self.score += 1

    def draw(self):

        self.screen.fill(BG)

        # Stars
        for sx, sy, sr in self.stars:

            pygame.draw.circle(
                self.screen,
                (200, 200, 220),
                (sx, sy),
                sr
            )

        # Meteors
        for meteor in self.meteors:
            meteor.draw(
                self.screen
            )

        # Lasers
        for laser in self.lasers:
            laser.draw(
                self.screen
            )

        # Ship
        self.ship.draw(
            self.screen
        )

        # Score
        sc = self.font.render(
            f"Time: {self.score // 60}s",
            True,
            (200, 200, 240)
        )

        self.screen.blit(
            sc,
            (10, 10)
        )

        # Start screen
        if not self.started:

            msg = self.font.render(
                "Press SPACE to launch",
                True,
                (180, 180, 240)
            )

            self.screen.blit(
                msg,
                (
                    WIDTH // 2
                    - msg.get_width() // 2,
                    HEIGHT // 2
                )
            )

        # Game over
        if self.game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 150)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            message = self.big_font.render(
                "DESTROYED!",
                True,
                (220, 80, 60)
            )

            score_message = self.font.render(
                f"Survived {self.score // 60}s | "
                "SPACE to Restart",
                True,
                (200, 200, 200)
            )

            self.screen.blit(
                message,
                (
                    WIDTH // 2
                    - message.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )

            self.screen.blit(
                score_message,
                (
                    WIDTH // 2
                    - score_message.get_width() // 2,
                    HEIGHT // 2 + 20
                )
            )

        pygame.display.flip()

    def run(self):

        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()