import sys
from pathlib import Path
from PIL import Image

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import Tk, Canvas, PhotoImage, Entry, Button
import customtkinter as ctk



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\adminWindow\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1350x800")
window.title("CaD - Doctor Appointment Booking System (Admin Window)")
window.configure(bg = "#000")


# canvas = Canvas(
#     window,
#     bg = "#fff",
#     height = 800,
#     width = 1043,
#     bd = 0,
#     highlightthickness = 0,
#     relief = "ridge"
# )

# canvas.place(x = 307, y = 0)
# canvas.create_rectangle(
#     0.0,
#     131.0,
#     1350.0,
#     133.0,
#     fill="#FFFFFF",
#     outline="")

# canvas.create_rectangle(
#     0.0,
#     0.0,
#     307.0,
#     800.0,
#     fill="#000000",
#     outline="")

# <<<<<<<<<<<<<<<<<<<< SIDEBAR FRAME >>>>>>>>>>>>>>>>>>>>>
sidebarFrame = ctk.CTkFrame(window, width=310, height=800, fg_color="#000", border_color="#000", )
sidebarFrame.place(x=0, y=0)



# 3D Image
logoImgPath = relative_to_assets("image_1.png")
logoImg = ctk.CTkImage(light_image=Image.open(logoImgPath), size=(213,74))
logoImgLabel = ctk.CTkLabel(sidebarFrame, image=logoImg, text_color='#000',text='', anchor=ctk.W,)
logoImgLabel.pack(side="top", fill='none', expand=False, padx=(30, 0), pady=25)

# Dashboard Button with Icon
dashboardIconPath = relative_to_assets("dashboard-icon.png")
dashboardIcon = ctk.CTkImage(light_image=Image.open(dashboardIconPath), size=(33,33))
dashboardButton = ctk.CTkButton(
    sidebarFrame, text=" Dashboard", width=240, height=60, 
    font=("Inter", 26, "bold",), fg_color="#37D8B7", hover_color="#37D8B7", image=dashboardIcon,
    # anchor=ctk.W
)
dashboardButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=25)

# Profile Button with Icon
profileIconPath = relative_to_assets("profile-icon.png")
profileIcon = ctk.CTkImage(light_image=Image.open(profileIconPath), size=(33,33),)
profileButton = ctk.CTkButton(
    sidebarFrame, text=" Profile       ", width=240, height=60, 
    font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=profileIcon,
    # anchor=ctk.W
)
profileButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=(0, 25))

lineFrame = ctk.CTkFrame(window, width=310, height=2, fg_color="#37D8B7" )
lineFrame.place(x=0, y=686)


# Logout Button with Icon
logoutIconPath = relative_to_assets("logout-icon.png")
logoutIcon = ctk.CTkImage(light_image=Image.open(logoutIconPath), size=(33,33),)
logoutButton = ctk.CTkButton(
    sidebarFrame, text=" Logout      ", width=240, height=60, 
    font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=logoutIcon,
    # anchor=ctk.W 
)
logoutButton.pack(side="bottom", fill='y', expand=True, padx=(35, 0), pady=(395, 0))


# <<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>
whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", )
whiteFrame.place(x=310, y=0)




# canvas.create_text(
#     721.0,
#     28.0,
#     anchor="nw",
#     text="Admin",
#     fill="#000000",
#     font=("Inter ExtraBold", 64 * -1)
# )

# canvas.create_text(
#     338.0,
#     149.0,
#     anchor="nw",
#     text="Manage Clinics",
#     fill="#000000",
#     font=("Inter SemiBold", 40 * -1)
# )

# canvas.create_text(
#     338.0,
#     213.0,
#     anchor="nw",
#     text="Manage the clinic registrations after verifying with Malaysian Registered Doctor System",
#     fill="#000000",
#     font=("Inter", 22 * -1)
# )

# entry_image_1 = PhotoImage(
#     file=relative_to_assets("entry_1.png"))
# entry_bg_1 = canvas.create_image(
#     818.5,
#     300.0,
#     image=entry_image_1
# )
# entry_1 = Entry(
#     bd=0,
#     bg="#FFFFFF",
#     fg="#000716",
#     highlightthickness=0
# )
# entry_1.place(
#     x=340.0,
#     y=270.0,
#     width=957.0,
#     height=58.0
# )

# image_image_2 = PhotoImage(
#     file=relative_to_assets("image_2.png"))
# image_2 = canvas.create_image(
#     818.0,
#     568.0,
#     image=image_image_2
# )
window.resizable(False, False)
window.mainloop()
