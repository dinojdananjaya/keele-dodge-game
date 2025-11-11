# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com/)
# to co-create parts of this file.

from game.core import GameState, Entity
from game.settings import SETTINGS

def test_scoring_on_star_collision():
    s = GameState()
    s.stars.append(Entity(x=s.player.x, y=s.player.y, w=SETTINGS.STAR_SIZE, h=SETTINGS.STAR_SIZE, kind="star"))
    s.tick()
    assert s.score >= 10

def test_life_loss_on_hazard_collision():
    s = GameState()
    lives_before = s.lives
    s.hazards.append(Entity(x=s.player.x, y=s.player.y, w=SETTINGS.HAZARD_SIZE, h=SETTINGS.HAZARD_SIZE, kind="hazard"))
    s.tick()
    assert s.lives == lives_before - 1