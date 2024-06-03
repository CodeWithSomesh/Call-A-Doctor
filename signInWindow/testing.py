from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\signInWindow\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = ctk.CTk()

window.geometry("1350x800")
window.configure(bg = "#000000")


canvas = Canvas(
    window,
    bg = "#000000",
    height = 800,
    width = 1350,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

textbox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#828282", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75"
)
textbox.pack()



window.resizable(False, False)
window.mainloop()