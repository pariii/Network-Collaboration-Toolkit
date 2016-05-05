from tkinter import ttk
import tkinter as tk

def main():
    frame = Tk()
    frame.geometry("480x360")

    credit = tk.DoubleVar(frame, value=0)
    # credit = tk.StringVar(frame, value="0")

    ttk.Label(frame, textvariable = credit).pack()

    def add_credit(amt):
        global credit
        credit.set(credit.get() + amt)
        # new_credit = str(int(credit.get().replace(".",""))+amt)
        # credit.set(new_credit[:-2]+"."+new_credit[-2:])

    ttk.Button(frame, text="10p", command = lambda: add_credit(0.1)).pack()
    # ttk.Button(frame, text="10p", command = lambda: add_credit(10)).pack()

    ttk.Button(frame, text="20p", command = lambda: add_credit(0.2)).pack()
    # ttk.Button(frame, text="20p", command = lambda: add_credit(20)).pack()

    ttk.Button(frame, text="50p", command = lambda: add_credit(0.5)).pack()
    # ttk.Button(frame, text="50p", command = lambda: add_credit(50)).pack()

    ttk.Button(frame, text="P1",  command = lambda: add_credit(1.0)).pack()
    # ttk.Button(frame, text="P1",  command = lambda: add_credit(100)).pack()

    frame.mainloop()