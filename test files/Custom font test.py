import tkinter 
import tkinter as tk 
import tkinter.ttk


root = tk.Tk()

label = tkinter.Label(root, font=("ds-digital", 50), background="black", foreground="white" , text="boost")
label.pack(anchor="center")



canvas = tk.Canvas(root, width=480, height=480, borderwidth=0, highlightthickness=0,
bg="black")
"""canvas.grid()
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
boost_text = canvas.create_text(240, 240, text='boost', fill="white", font= (', 50 bold'))
canvas.pack()
"""

root.mainloop()