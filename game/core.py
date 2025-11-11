# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com/)
# to co-create parts of this file.

"""
UI-agnostic game rules and state for Dodge & Collect.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
import random

from .settings import SETTINGS

Vec = Tuple[float, float]

@dataclass
class Entity:
    x: float
    y: float
    w: int
    h: int
    vy: float = 0.0
    kind: str = "hazard"  # "hazard" or "star"

    def aabb(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)

@dataclass
class Player:
    x: float
    y: float
    w: int
    h: int
    speed: int

    def move(self, dx: int, width: int) -> None:
        self.x = max(0, min(width - self.w, self.x + dx * self.speed))

@dataclass
class GameState:
    width: int = SETTINGS.WIDTH
    height: int = SETTINGS.HEIGHT
    tick_count: int = 0
    rng: random.Random = field(default_factory=random.Random)

    player: Player = field(default_factory=lambda: Player(
        x=(SETTINGS.WIDTH - SETTINGS.PLAYER_WIDTH)/2,
        y=SETTINGS.HEIGHT - 80,
        w=SETTINGS.PLAYER_WIDTH,
        h=SETTINGS.PLAYER_HEIGHT,
        speed=SETTINGS.PLAYER_SPEED,
    ))
    hazards: List[Entity] = field(default_factory=list)
    stars: List[Entity] = field(default_factory=list)

    score: int = 0
    lives: int = SETTINGS.START_LIVES
    game_over: bool = False

    move_dir: int = 0  # -1, 0, +1

    def set_move(self, direction: int) -> None:
        self.move_dir = max(-1, min(1, direction))

    def spawn_prob(self) -> float:
        return SETTINGS.BASE_SPAWN_CHANCE + self.tick_count * SETTINGS.DIFFICULTY_RAMP

    def fall_speed(self) -> float:
        return SETTINGS.BASE_FALL_SPEED + (self.tick_count * SETTINGS.DIFFICULTY_RAMP * 200)

    def spawn_entities(self) -> None:
        if self.rng.random() < self.spawn_prob():
            x = self.rng.randint(0, self.width - SETTINGS.HAZARD_SIZE)
            kind = "hazard" if self.rng.random() < 0.7 else "star"
            if kind == "hazard":
                self.hazards.append(Entity(x=x, y=-SETTINGS.HAZARD_SIZE, w=SETTINGS.HAZARD_SIZE,
                                           h=SETTINGS.HAZARD_SIZE, vy=self.fall_speed(), kind="hazard"))
            else:
                self.stars.append(Entity(x=x, y=-SETTINGS.STAR_SIZE, w=SETTINGS.STAR_SIZE,
                                         h=SETTINGS.STAR_SIZE, vy=self.fall_speed()*0.85, kind="star"))

    @staticmethod
    def _collide(a: Player, b: Entity, pad: int = SETTINGS.COLLISION_PAD) -> bool:
        ax1, ay1, ax2, ay2 = a.x+pad, a.y+pad, a.x + a.w - pad, a.y + a.h - pad
        bx1, by1, bx2, by2 = b.x+pad, b.y+pad, b.x + b.w - pad, b.y + b.h - pad
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

    def tick(self) -> None:
        if self.game_over:
            return

        self.tick_count += 1

        # Move player
        if self.move_dir != 0:
            self.player.move(self.move_dir, self.width)

        # Spawn
        self.spawn_entities()

        # Move & cull
        for obj in self.hazards + self.stars:
            obj.y += obj.vy
        self.hazards = [h for h in self.hazards if h.y < self.height + 50]
        self.stars = [s for s in self.stars if s.y < self.height + 50]

        # Collisions (hazards)
        remaining_hazards: List[Entity] = []
        for h in self.hazards:
            if self._collide(self.player, h):
                self.lives -= 1
            else:
                remaining_hazards.append(h)
        self.hazards = remaining_hazards

        # Collisions (stars)
        gained = 0
        remaining_stars: List[Entity] = []
        for s in self.stars:
            if self._collide(self.player, s):
                gained += 10
            else:
                remaining_stars.append(s)
        self.stars = remaining_stars
        self.score += gained

        if self.lives <= 0:
            self.game_over = True
