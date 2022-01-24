import tkinter as tk 
from tkinter import filedialog, Text 
import os 

root = tk.Tk()
canvas = tk.Canvas(root, width=480, height=480, borderwidth=0, highlightthickness=0,
bg="black")

canvas.grid()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

canvas.create_circle(240, 240, 230, fill="black", outline="grey", width=4)

canvas.create_circle_arc(240, 240, 210, style="arc", outline="white", width=40,
                         start=270-50, end=270+50)
#Start of gauge = 270-50, end is 270+50
canvas.create_circle_arc(240, 240, 210, style="arc", outline="red", width=40,
                         start=-40, end=220)
root.title("Circles and Arcs")
root.mainloop()