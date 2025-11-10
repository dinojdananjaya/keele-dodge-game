# I acknowledge the use of OpenAI ChatGPT.
# to co-create parts of this file.

"""
Tkinter entrypoint (minimal boot). Real loop added on GUI feature branch.
Run: python -m game.tkui
"""

import tkinter as tk
from .settings import SETTINGS

def main():
    root = tk.Tk()
    root.title("Dodge & Collect")
    root.configure(bg=SETTINGS.BG)
    canvas = tk.Canvas(root, width=SETTINGS.WIDTH, height=SETTINGS.HEIGHT,
                       bg=SETTINGS.BG, highlightthickness=0)
    canvas.pack()
    canvas.create_text(SETTINGS.WIDTH/2, SETTINGS.HEIGHT/2,
                       fill="#FFFFFF", font=("Consolas", 20, "bold"),
                       text="Dodge & Collect\n(boot)")
    root.mainloop()

if __name__ == "__main__":
    main()
