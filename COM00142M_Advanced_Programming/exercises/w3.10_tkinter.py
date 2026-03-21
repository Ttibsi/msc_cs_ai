import tkinter


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

if __name__ == "__main__":
    raise SystemExit(main())
