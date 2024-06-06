from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\logInWindow\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_login_window():
    window = Tk()
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
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        401.0,
        400.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        719.0,
        0.0,
        1350.0,
        800.0,
        fill="#FFFCFC",
        outline="")

    canvas.create_text(
        858.0,
        123.0,
        anchor="nw",
        text="Your Health, Our Priority",
        fill="#000000",
        font=("Inter", 32 * -1, "bold")
    )

    canvas.create_text(
        778.0,
        163.0,
        anchor="nw",
        text="– Book Appointments in Seconds",
        fill="#000000",
        font=("Inter", 32 * -1, "bold")
    )

    canvas.create_text(
        761.060302734375,
        396.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        1048.060302734375,
        396.0,
        anchor="nw",
        text="Sign In As",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        761.060302734375,
        290.0,
        anchor="nw",
        text="Email",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        1035.060302734375,
        346.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=769.060302734375,
        y=322.0,
        width=532.0,
        height=46.0
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
        x=761.0,
        y=525.0,
        width=547.8106689453125,
        height=64.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        891.560302734375,
        452.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=769.060302734375,
        y=428.0,
        width=245.0,
        height=46.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        1178.560302734375,
        452.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=1056.060302734375,
        y=428.0,
        width=245.0,
        height=46.0
    )

    canvas.create_text(
        934.060302734375,
        614.0,
        anchor="nw",
        text="Don’t have an account? Sign Up",
        fill="#000000",
        font=("Inter", 15 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        1254.0,
        705.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        380.0,
        368.0,
        image=image_image_3
    )
    window.resizable(False, False)
    window.mainloop()

# Only execute the login window if this script is run directly
if __name__ == "__main__":
    open_login_window()
