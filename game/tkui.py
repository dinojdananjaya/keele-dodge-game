# I acknowledge the use of OpenAI ChatGPT (GPT-5, https://chat.openai.com/)
# to co-create parts of this file.

"""
Tkinter UI wrapper for Dodge & Collect.
Run with: python -m game.tkui
"""

from __future__ import annotations
import tkinter as tk

from .settings import SETTINGS
from .core import GameState

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dodge & Collect")
        self.root.configure(bg=SETTINGS.BG)
        self.canvas = tk.Canvas(root, width=SETTINGS.WIDTH, height=SETTINGS.HEIGHT,
                                bg=SETTINGS.BG, highlightthickness=0)
        self.canvas.pack()

        self.state = GameState()
        self._bind_keys()

        self.hud = self.canvas.create_text(10, 10, anchor="nw", fill="#e0e0e0",
                                           font=("Consolas", 14), text="")
        self._loop()

    def _bind_keys(self):
        self.root.bind("<KeyPress-Left>",  lambda e: self.state.set_move(-1))
        self.root.bind("<KeyPress-Right>", lambda e: self.state.set_move(1))
        self.root.bind("<KeyRelease-Left>", self._key_release)
        self.root.bind("<KeyRelease-Right>", self._key_release)

    def _key_release(self, event):
        self.state.set_move(0)

    def _draw(self):
        self.canvas.delete("game")

        # Player
        p = self.state.player
        self.canvas.create_rectangle(p.x, p.y, p.x + p.w, p.y + p.h,
                                     fill="#4FC3F7", width=0, tags="game")

        # Hazards
        for h in self.state.hazards:
            self.canvas.create_rectangle(h.x, h.y, h.x + h.w, h.y + h.h,
                                         fill="#F44336", width=0, tags="game")

        # Stars
        for s in self.state.stars:
            self.canvas.create_oval(s.x, s.y, s.x + s.w, s.y + s.h,
                                    fill="#FFD54F", width=0, tags="game")

        self.canvas.itemconfigure(self.hud,
                                  text=f"Score: {self.state.score}   Lives: {self.state.lives}")

        if self.state.game_over:
            self.canvas.create_text(SETTINGS.WIDTH/2, SETTINGS.HEIGHT/2, fill="#FFFFFF",
                                    font=("Consolas", 28, "bold"),
                                    text="GAME OVER", tags="game")
            self.canvas.create_text(SETTINGS.WIDTH/2, SETTINGS.HEIGHT/2 + 36, fill="#CCCCCC",
                                    font=("Consolas", 16),
                                    text="Press Enter to restart", tags="game")

    def _loop(self):
        if self.state.game_over:
            self.root.bind("<Return>", self._restart)
        else:
            self.root.after(SETTINGS.TICK_MS, self._loop)
        self.state.tick()
        self._draw()

    def _restart(self, _evt):
        self.root.unbind("<Return>")
        self.state = GameState()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
