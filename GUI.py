# -- coding: utf-8 --
# @Author: MSCopilot
# @Time: 2025/8/24 19:26

from maliang import Tk, Canvas, PhotoImage, Text
from tkinter.ttk import Treeview
from PIL import Image

def start_gui():
    root = Tk(
        (700, 900),
        (930, 260),
        title="WatchFile 设置"
    )
    root.icon(PhotoImage(file="icon.png"))

    canvas = Canvas(
        root,
        auto_zoom=True,
        auto_update=True,
        zoom_all_items=True,
        width=700,
        height=900,
    )
    canvas.pack(padx=0, pady=0)

    title = Text(
        canvas,
        position=(350, 20),
        family="HarmonyOS Sans SC Semibold",
        fontsize=48,
        text="WatchFile 设置",
        anchor="n"
    )

    root.mainloop()

if __name__ == '__main__':
    start_gui()