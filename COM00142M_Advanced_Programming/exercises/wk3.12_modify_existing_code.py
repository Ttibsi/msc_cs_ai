import tkinter as tk
from tkinter import ttk

def get_def():
    term = term_entry.get()
    # clears the text box from previous entries
    output.delete(0.0, tk.END)
    if term in computer_defs:
        definition = computer_defs[term]
    else:
        definition = "sorry that term is not in the dictionary"

    output.insert(tk.END, definition)

window = tk.Tk()
window.title("Computer Science Definitions")
window.configure(background='black')

# text to output to the user
instruction=tk.StringVar()
instruction.set('Enter a term you would like to know the definition of:')

# adding instruction for user
tk.Label(window, text=instruction.get(), 
         bg='black', fg='white', font='none 12 bold').grid(row=1,column=0, columnspan=2, sticky='EW')

# create a text entry box
term_entry = tk.Entry(window,bg='white', width=30)
term_entry.grid(row=2, column=0, sticky='E')

ttk.Button(window, text='GET', width=6, command=get_def).grid(row=2, column=1, sticky='W')

# lable for output
tk.Label(window, text='\nDefinition:', bg='black', fg='white', font='none 12 bold').grid(row=4,column=0, columnspan=2, sticky='W')

# output for the definiton (large text box)
output = tk.Text(window, width=75, height=6, wrap='word', background='white')
output.grid(row=5, column=0, columnspan=2)

computer_defs = {
    'term':'Def',
    'term2':'Def2',
    "function": "A reusable block of code tagged with a name",
    "class": "A blueprint for groupinng of attributes (variables) and methods (functions)"
}

# Allow the user to add their own definitions
tk.Label(window, text='Enter new definition', bg='black', fg='white', font='none 12 bold').grid(row=6,column=0, columnspan=2, sticky='W')
tk.Label(window, text="term", bg='black', fg='white', font='none 12 bold').grid(row=7,column=0, sticky='W')
new_term = tk.Entry(window, bg="white", width=30).grid(row=7, column=1, sticky="W")
tk.Label(window, text="definition", bg='black', fg='white', font='none 12 bold').grid(row=7,column=2, sticky='W')
new_def = tk.Entry(window, bg="white", width=30).grid(row=7, column=3, sticky="W")

# Save to JSON file
import json
def save():
    with open("computer_defintions.json", "w") as f:
        json.dump(computer_defs, f)
    print("Saved to computer_defintions.json")


ttk.Button(window, text='SAVE', width=6, command=save).grid(row=8, column=1, sticky='W')


window.mainloop()
