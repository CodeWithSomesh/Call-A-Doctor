from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\signInWindow\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Must be TK, giving issues if its CTK
window = Tk()
window.title("CaD - Doctor Appointment Booking System (Login Window)")
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


bgImagePath = PhotoImage(
    file=relative_to_assets("image_1.png"))
bgImage = canvas.create_image(
    326.0,
    401.0,
    image=bgImagePath
)

whiteBgPath = PhotoImage(
    file=relative_to_assets("image_2.png"))
whiteBg = canvas.create_image(
    969.0,
    400.0,
    image=whiteBgPath
)

canvas.create_text(
    670.0,
    53.0,
    anchor="nw",
    text="Create Account",
    fill="#000000",
    font=("Inter", 48 * -1, "bold", "underline")
)

canvas.create_text(
    670.0,
    154.0,
    anchor="nw",
    text="First Name",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)


canvas.create_text(
    994.0,
    154.0,
    anchor="nw",
    text="Last Name",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

canvas.create_text(
    670.0,
    260.0,
    anchor="nw",
    text="Address",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

canvas.create_text(
    670.0,
    406.0,
    anchor="nw",
    text="Email",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

canvas.create_text(
    670.0,
    512.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

canvas.create_text(
    994.0,
    512.0,
    anchor="nw",
    text="Sign In As",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)






entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    979.5,
    462.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=678.0,
    y=438.0,
    width=603.0,
    height=46.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    979.5,
    336.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=678.0,
    y=292.0,
    width=603.0,
    height=86.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=670.0,
    y=641.0,
    width=619.0,
    height=64.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    817.5,
    568.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=678.0,
    y=544.0,
    width=279.0,
    height=46.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    1141.5,
    568.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=1002.0,
    y=544.0,
    width=279.0,
    height=46.0
)



entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    1141.5,
    210.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=1002.0,
    y=186.0,
    width=279.0,
    height=46.0
)

canvas.create_text(
    865.0,
    718.0,
    anchor="nw",
    text="Already have an account? Login",
    fill="#000000",
    font=("Inter", 15 * -1, "bold")
)
window.resizable(False, False)
window.mainloop()
