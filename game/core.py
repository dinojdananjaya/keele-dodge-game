# I acknowledge the use of OpenAI ChatGPT.
# to co-create parts of this file.

"""
Core game types & contracts (stub). Implemented on feature branch.
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
    kind: str = "hazard"  # or "star"

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
        # TODO: implement in feature branch
        pass

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
        # TODO: implement in feature branch
        pass

    def tick(self) -> None:
        """Advance one frame. To be implemented on feature branch."""
        # TODO: implement in feature branch
        pass
