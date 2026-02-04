import tkinter as tk

root = tk.Tk()
label = tk.Label(root, text="Processing", font=("Arial", 14))
label.pack(pady=20)

dots = 0

def animate_loading():
    global dots
    dots = (dots + 1) % 4
    label.config(text="Processing" + "." * dots)
    root.after(500, animate_loading)

animate_loading()
root.mainloop()
