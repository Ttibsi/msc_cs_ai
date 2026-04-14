from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
import numpy
import random

# matplotlib and tkinter
# https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

win = tkinter.Tk()
fig = Figure(figsize=(5,4))
ax = fig.add_subplot()

if random.randint(0, 10) % 2:
    ax.plot(
        numpy.random.standard_normal(50).cumsum(),
        color="black",
        linestyle="dashed"
    )
else:
    ax.hist(
        numpy.random.standard_normal(100).cumsum(),
        bins=20,
        color="black",
        alpha=0.3  # style option, sets opacity of the plot
    )

canvas = FigureCanvasTkAgg(fig, master=win)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
win.mainloop()
