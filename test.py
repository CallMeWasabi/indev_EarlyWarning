import tkinter as tk

def on_focus_out(event):
    if event.widget == root:
        label.configure(text="I DON'T have focus")

def on_focus_in(event):
    if event.widget == root:
        label.configure(text="I have focus")

root = tk.Tk()
label = tk.Label(width=30)
label.pack(side="top", fill="both", expand=True)

root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)

root.mainloop()