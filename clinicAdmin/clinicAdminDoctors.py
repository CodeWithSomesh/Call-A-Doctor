import sys
from pathlib import Path
from PIL import Image
import random
from random import choice
import sqlite3
from datetime import datetime

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\clinicAdmin\assets\frame0")

def clinicAdminDoctorWindow(email):
    # Connecting to Clinic Admin DB
    clinicAdminConn = sqlite3.connect('clinicAdmins.db')
    clinicAdminCursor = clinicAdminConn.cursor()
    clinicAdminCursor.execute('SELECT * FROM clinicAdmins WHERE Email=?', [email])
    result = clinicAdminCursor.fetchone()
    #username = f"{result[1]} {result[2]}" # Getting user's full name to display on top 

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ALL FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Redirect to the Log In Window
    def redirectToLoginWindow():
        window.destroy()
        from logInWindow.main import logInWindow
        logInWindow()

    
    # Redirect to the Clinic Admin Dashboard Window
    def redirectToAdminDashboardWindow():
        window.destroy()
        from clinicAdmin.clinicAdminDashboard import clinicAdminDashboardWindow
        clinicAdminDashboardWindow()


    # When user is typing remove placeholder
    def searchbarFocus(event):
        print(event)
        searchInputTextBox.delete('0.0', "end")
        searchInputTextBox.configure(text_color='black')
            

    # When user is does not type or left halfway while typing,
    # then replace placeholder
    def searchbarOutFocus(event):
        print(event)
        searchInputTextBox.delete('0.0', "end")
        searchInputTextBox.insert('0.0', "Search Doctors by their Name or Clinic Name")
        searchInputTextBox.configure(text_color='gray')


    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Clinic Admin Window)")
    window.configure(fg_color="black")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()
    

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
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=dashboardIcon,
        command=redirectToAdminDashboardWindow # anchor=ctk.W
    )
    dashboardButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=25)

    # Doctor Button with Icon
    doctorIconPath = relative_to_assets("doctor-icon.png")
    doctorIcon = ctk.CTkImage(light_image=Image.open(doctorIconPath), size=(44,44),)
    doctorButton = ctk.CTkButton(
        sidebarFrame, text=" Doctors     ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#37D8B7", hover_color="#37D8B7", image=doctorIcon,
        # anchor=ctk.W 
    )
    doctorButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=(0, 25))

    # Profile Button with Icon
    profileIconPath = relative_to_assets("profile-icon.png")
    profileIcon = ctk.CTkImage(light_image=Image.open(profileIconPath), size=(44,44),)
    profileButton = ctk.CTkButton(
        sidebarFrame, text=" Profile       ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=profileIcon,
        # anchor=ctk.W
    )
    profileButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=(0, 25))

    # Line that seperates Logout Button from others 
    lineFrame = ctk.CTkFrame(window, width=310, height=2, fg_color="#37D8B7" )
    lineFrame.place(x=0, y=686)

    # Logout Button with Icon
    logoutIconPath = relative_to_assets("logout-icon.png")
    logoutIcon = ctk.CTkImage(light_image=Image.open(logoutIconPath), size=(33,33),)
    logoutButton = ctk.CTkButton(
        sidebarFrame, text=" Logout      ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=logoutIcon,
        command=redirectToLoginWindow # anchor=ctk.W 
    )
    logoutButton.pack(side="bottom", fill='y', expand=True, padx=(35, 0), pady=(310, 0))


    # <<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>
    whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", bg_color='#fff' )
    whiteFrame.place(x=310, y=0)


    # Label with Greeting Message & User's First Name 

    now = datetime.now()  # Get the current date and time
    formatted_date = now.strftime("%B %d, %Y") # Format the date as 'Month Day, Year'
    current_hour = now.hour # Get the current hour
    current_time = now.strftime("%H:%M:%S") # Get the current time

    # Generate greeting message based on the current time
    if current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!" 

    greetingLabel1 = ctk.CTkLabel(whiteFrame, text="Welcome, {username}", font=("Inter", 36, "bold",), text_color="#000000")
    greetingLabel1.place(x=25, y=25)
    greetingLabel2 = ctk.CTkLabel(whiteFrame, text=f"{greeting}  ({formatted_date})", font=("Inter", 22,), text_color="#000000")
    greetingLabel2.place(x=25, y=72)
    roleLabel = ctk.CTkLabel(whiteFrame, text="(Clinic Admin)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=775, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Manage Doctors Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Manage Doctors", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="Manage the status of registered doctors in the app", 
        )
    descLabel.place(x=25, y=182)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
            whiteFrame, fg_color="#ffffff", text_color="gray", width=660, height=50, 
            border_color="#000", font=("Inter", 21), border_spacing=8,
            scrollbar_button_color="#1AFF75", border_width=2,
        )
    searchInputTextBox.insert('insert', "Search Doctors by their Name or Clinic Name")
    searchInputTextBox.place(x=25, y=225)
    searchInputTextBox.bind("<FocusIn>", searchbarFocus)
    searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)


    # Approve Button with Icon
    approveIconPath = relative_to_assets("approve-icon.png")
    approveIcon = ctk.CTkImage(light_image=Image.open(approveIconPath), size=(33,33),)
    approveButton = ctk.CTkButton(
        whiteFrame, text=" Approve ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#00C16A", hover_color="#009B2B", image=approveIcon,
        # anchor=ctk.W 
    )
    approveButton.place(x=700, y=225)

    # Reject Button with Icon
    rejectIconPath = relative_to_assets("reject-icon.png")
    rejectIcon = ctk.CTkImage(light_image=Image.open(rejectIconPath), size=(33,33),)
    rejectButton = ctk.CTkButton(
        whiteFrame, text=" Reject  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=rejectIcon,
        # anchor=ctk.W 
    )
    rejectButton.place(x=870, y=225)


    # <<<<<<<<<<<<<<<<<<<< TABLE FRAME STORING TREEVIEW >>>>>>>>>>>>>>>>>>>>> 
    tableFrame = ctk.CTkFrame(whiteFrame, fg_color="transparent",)
    tableFrame.place(x=25, y=295)

    # Initializing Treeview Scrollbar
    tableScrollbar1 = Scrollbar(tableFrame, orient=VERTICAL)
    # tableScrollbar2 = Scrollbar(tableFrame, orient="horizontal")

    # Treeview that stores User Data
    table = ttk.Treeview(tableFrame, yscrollcommand=tableScrollbar1.set,height=12)
    table.pack(side='left', fill='both')
    table['columns'] = (
        'No', 'Clinic ID', 'Clinic Name', 'Clinic Contact',
        "Clinic Admin", "Admin Email"
    )

    # Placing and Configuring Treeview Scrollbar
    tableScrollbar1.pack(side='left', fill='y')
    tableScrollbar1.config(command=table.yview)
    # tableScrollbar2.pack(side='bottom', fill='x')
    # tableScrollbar2.config(command=table.xview)

    # Styling the Treeview Heading and Rows 
    style = ttk.Style(tableFrame)
    style.theme_use('clam')
    style.configure(
        'Treeview.Heading', font=('Inter', 16, 'bold'), 
        foreground='#fff', background='#000', hover=False,
    )
    style.configure('Treeview', font=('Inter', 16), rowheight=47, fieldbackground="#DAFFF7")
    style.map(
        'Treeview', 
        background=[('selected', '#00BE97',)], 
        font=[('selected', ('Inter', 16, 'bold'))],
    )
    
    # Treeview Table Headings Details
    table.heading('No', text='No')
    table.heading('Clinic ID', text='Clinic ID',)
    table.heading('Clinic Name', text='Clinic Name')
    table.heading('Clinic Contact', text='Clinic Contact')
    table.heading('Clinic Admin', text='Clinic Admin')
    table.heading('Admin Email', text='Admin Email')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("No", width=43, anchor=ctk.CENTER)
    table.column("Clinic ID", anchor=ctk.CENTER)
    table.column("Clinic Name", width=220, anchor=ctk.CENTER)
    table.column("Clinic Contact", anchor=ctk.CENTER)
    table.column("Clinic Admin", width=250, anchor=ctk.CENTER)
    table.column("Admin Email", width=315, anchor=ctk.CENTER,)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")


    # <<<<<<<<<<<<<<<<<<<< AUTOMATED TESTING >>>>>>>>>>>>>>>>>>>>>
    global count
    count = 0
    #     if count % 2 == 0:
    #         table.insert(parent='', index=0, values=data, tags=("evenrow",))
    #     else:
    #         table.insert(parent='', index=0, values=data, tags=("oddrow",))

    clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']



    for i in range(15):
        num = (i+1)
        clinicID = ''.join(random.choices('0123456789', k=12))
        clinicName = choice(clinicNames)
        clinicContact = ''.join(random.choices('0123456789', k=8))
        clinicContact = f'+01{clinicContact}'
        adminName = choice(adminNames)
        adminEmail = f'{(adminName.replace(" ", "")).lower()}@email.com'

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
    


    window.mainloop()


# Only execute the Clinic Admin Doctor Window if this script is run directly
if __name__ == "__main__":
    clinicAdminDoctorWindow(email=None)