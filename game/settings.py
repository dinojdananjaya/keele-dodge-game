# I acknowledge the use of OpenAI ChatGPT.
# to co-create parts of this file.

from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    WIDTH: int = 480
    HEIGHT: int = 720
    BG: str = "#111111"

    PLAYER_WIDTH: int = 50
    PLAYER_HEIGHT: int = 20
    PLAYER_SPEED: int = 10

    HAZARD_SIZE: int = 22
    STAR_SIZE: int = 16

    TICK_MS: int = 16  # ~60 FPS

    START_LIVES: int = 3

    BASE_FALL_SPEED: float = 3.5
    BASE_SPAWN_CHANCE: float = 0.03
    DIFFICULTY_RAMP: float = 0.00002

    COLLISION_PAD: int = 2

SETTINGS = Settings()
