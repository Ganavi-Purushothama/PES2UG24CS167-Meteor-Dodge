import pygame
import random
import math


class Meteor:
    def __init__(
        self,
        width,
        x=None,
        y=None,
        radius=None,
        vx=None,
        vy=None
    ):
        self.x = random.randint(0, width) if x is None else x
        self.y = -30 if y is None else y

        self.radius = (
            random.randint(12, 28)
            if radius is None
            else radius
        )

        if vx is None or vy is None:
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)

            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
        else:
            self.vx = vx
            self.vy = vy

        self.color = (
            random.randint(160, 220),
            random.randint(80, 120),
            random.randint(40, 80)
        )

        self.rot = 0
        self.rot_speed = random.uniform(-3, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx = self.x - cx
        dy = self.y - cy

        return (dx ** 2 + dy ** 2) ** 0.5 < self.radius + 16

    def split(self):
        """Split a large meteor into two smaller meteors."""

        # Only large meteors split.
        if self.radius < 20:
            return []

        child_radius = max(8, int(self.radius * 0.5))

        speed = max(
            3,
            (self.vx ** 2 + self.vy ** 2) ** 0.5
        )

        base_angle = math.atan2(self.vy, self.vx)
        spread = math.radians(35)

        angle1 = base_angle - spread
        angle2 = base_angle + spread

        child1 = Meteor(
            width=700,
            x=self.x,
            y=self.y,
            radius=child_radius,
            vx=math.cos(angle1) * speed,
            vy=math.sin(angle1) * speed
        )

        child2 = Meteor(
            width=700,
            x=self.x,
            y=self.y,
            radius=child_radius,
            vx=math.cos(angle2) * speed,
            vy=math.sin(angle2) * speed
        )

        return [child1, child2]

    def draw(self, screen):
        pts = []

        for i in range(7):
            angle = math.radians(
                self.rot + i * (360 / 7)
            )

            r = self.radius * (
                0.8 + 0.2 * (i % 2)
            )

            pts.append(
                (
                    int(
                        self.x
                        + r * math.cos(angle)
                    ),
                    int(
                        self.y
                        + r * math.sin(angle)
                    )
                )
            )

        pygame.draw.polygon(
            screen,
            self.color,
            pts
        )

        inner = []

        for i in range(7):
            angle = math.radians(
                self.rot + i * (360 / 7)
            )

            inner.append(
                (
                    int(
                        self.x
                        + (self.radius * 0.5)
                        * math.cos(angle)
                    ),
                    int(
                        self.y
                        + (self.radius * 0.5)
                        * math.sin(angle)
                    )
                )
            )

        pygame.draw.polygon(
            screen,
            tuple(
                max(0, c - 40)
                for c in self.color
            ),
            inner
        )