import tkinter
from tkinter import ttk

# Task 5 - tkinter widgets
def main() -> int:
    win = tkinter.Tk()
    win.title("Main frame")
    
    elements = []
    elements.append(tkinter.Label(win, text="label"))
    elements.append(tkinter.Button(win, text="button"))

    check = ""
    elements.append(tkinter.Checkbutton(win, text="opt 1", variable=check))
    elements.append(tkinter.Radiobutton(win, text="opt 2", variable=check))
    elements.append(tkinter.Listbox(win, listvariable=[1,2,3]))
    elements.append(tkinter.Message(win, text="Message! Message!"))
    elements.append(tkinter.Scale(win, digits=1, to=100, orient="horizontal"))
    elements.append(tkinter.Text(win))
    elements.append(tkinter.Spinbox(win))

    [x.pack() for x in elements]
    win.mainloop()
    return 0


# Task 6 - using layouts
def grid_layout() -> int:
    win = tkinter.Tk()

    font = ("Iosevka", 18)
    l1 = tkinter.Label(win, text="I am the left brain", anchor="center", font=font, fg="#F00")
    l2 = tkinter.Label(win, text="I am the right brain", anchor="center", font=font, fg="#00F")
    l1.grid(row=0, column=0, sticky="NSEW")
    l2.grid(row=0, column=1, sticky="NSEW")
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)

    win.title("Bo Burnham's Brain")
    win.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(grid_layout())
