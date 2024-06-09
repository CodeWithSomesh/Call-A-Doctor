import sys
from pathlib import Path
from PIL import Image
import random
from random import choice

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Scrollbar, VERTICAL
import customtkinter as ctk



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\adminWindow\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = ctk.CTk()

window.geometry("1350x800+115+5")
window.title("CaD - Doctor Appointment Booking System (Admin Window)")
window.configure(fg_color="black")


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
whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", bg_color='#fff' )
whiteFrame.place(x=310, y=0)


# Label with Role Text 
adminLabel = ctk.CTkLabel(whiteFrame, text="Admin", font=("Inter", 64, "bold",), text_color="#000000")
adminLabel.place(x=434, y=28)


lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
lineFrame2.place(x=310, y=130)


h1Label = ctk.CTkLabel(whiteFrame, text="Manage Clinics", font=("Inter", 40, "bold", 'underline'), text_color="#000000")
h1Label.place(x=31, y=155)

descLabel = ctk.CTkLabel(
        whiteFrame, font=("Inter", 22,), text_color="#000000",
        text="Manage the clinic registrations after verifying with Malaysian Registered Doctor System", 
    )
descLabel.place(x=31, y=220)

def searchbarFocus(event):
    print(event)
    searchInputTextBox.delete('0.0', "end")
    searchInputTextBox.configure(text_color='black')
        

def searchbarOutFocus(event):
    print(event)
    searchInputTextBox.insert('0.0', "Search Clinics by Name or Address")
    searchInputTextBox.configure(text_color='gray')



searchInputTextBox = ctk.CTkTextbox(
        whiteFrame, fg_color="#ffffff", text_color="gray", width=973, height=60, 
        border_color="#000", font=("Inter", 25), border_spacing=15,
        scrollbar_button_color="#1AFF75", border_width=2,
    )
searchInputTextBox.insert('insert', "Search Clinics by Name or Address")
searchInputTextBox.place(x=31, y=260)
searchInputTextBox.bind("<FocusIn>", searchbarFocus)
searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)



tableFrame = ctk.CTkFrame(whiteFrame, width=930, height=430, fg_color="transparent", border_color='black', border_width=2 )
tableFrame.place(x=31, y=340)



style = ttk.Style(tableFrame)
style.theme_use('clam')
style.configure(
    'Treeview.Heading', font=('Inter', 16, 'bold'), 
    foreground='#fff', background='#000',
)
style.configure('Treeview', font=('Inter', 16, 'bold'), rowheight=50)
style.map('Treeview', background=[('selected', '#00BE97')])

tableScrollbar1 = Scrollbar(tableFrame, orient=VERTICAL)
# tableScrollbar2 = Scrollbar(tableFrame, orient="horizontal")


table = ttk.Treeview(tableFrame, yscrollcommand=tableScrollbar1.set,)
table.pack(side='left', fill='both')
table['columns'] = (
    'No', 'Clinic ID', 'Clinic Name', 'Clinic Contact',
    "Clinic Admin", "Admin Email"
)


tableScrollbar1.pack(side='left', fill='y')
tableScrollbar1.config(command=table.yview)
# tableScrollbar2.pack(side='bottom', fill='x')
# tableScrollbar2.config(command=table.xview)



table.heading('No', text='No')
table.heading('Clinic ID', text='Clinic ID',)
table.heading('Clinic Name', text='Clinic Name')
table.heading('Clinic Contact', text='Clinic Contact')
table.heading('Clinic Admin', text='Clinic Admin')
table.heading('Admin Email', text='Admin Email')

table.column("#0", width=0, stretch=ctk.NO)
table.column("No", width=37, anchor=ctk.CENTER)
table.column("Clinic ID", anchor=ctk.CENTER)
table.column("Clinic Name", width=210, anchor=ctk.CENTER)
table.column("Clinic Contact", anchor=ctk.CENTER)
table.column("Clinic Admin", width=250, anchor=ctk.CENTER)
table.column("Admin Email", width=305, anchor=ctk.CENTER,)

table.tag_configure("oddrow", background="#F2F5F8")
table.tag_configure("evenrow", background="#B4EFF7")

global count
count = 0
#     if count % 2 == 0:
#         table.insert(parent='', index=0, values=data, tags=("evenrow",))
#     else:
#         table.insert(parent='', index=0, values=data, tags=("oddrow",))




# <<<<<<<<<<<<<<<<<<<< AUTOMATED TESTING >>>>>>>>>>>>>>>>>>>>>

clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']



for i in range(100):
    num = (i+1)
    clinicID = ''.join(random.choices('0123456789', k=12))
    clinicName = choice(clinicNames)
    clinicContact = ''.join(random.choices('0123456789', k=8))
    clinicContact = f'+01{clinicContact}'
    adminName = choice(adminNames)
    adminEmail = f'{adminName.replace(" ", "")}@email.com'

    data = (num, clinicID, clinicName, clinicContact, adminName, adminEmail)
    if count % 2 == 0:
        table.insert(parent='', index='end', values=data, tags=("evenrow",))
    else:
        table.insert(parent='', index='end', values=data, tags=("oddrow",))

    count += 1

# Test the insertion in table
def testTableInsertion():
    clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    clinicAddress = ["Kuala Lumpur", "George Town", "Ipoh", "Johor Bahru", "Kota Kinabalu", "Shah Alam", "Malacca City", "Alor Setar", "Kuantan", "Kuching"]
    adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']

    for name in adminNames:
        email = name.replace(" ", "")

    for i in range(10):
        num = i
        clinicID = ''.join(random.choices('0123456789', k=12))
        clinicName = choice(clinicNames)
        clinicContact = ''.join(random.choices('0123456789', k=8))
        clinicAddress = choice(clinicAddress)
        adminName = choice(adminNames)
        adminEmail = f'{email}@email.com'

        data = (num, clinicID, clinicName, clinicContact, clinicAddress, adminName, adminEmail)
        if count % 2 == 0:
            table.insert(parent='', index=0, values=data, tags=("evenrow",))
        else:
            table.insert(parent='', index=0, values=data, tags=("oddrow",))

        count += 1




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
