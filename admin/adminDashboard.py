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
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\admin\assets\frame0")

def adminDashboardWindow():

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ALL FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Redirect to the Log In Window
    def redirectToLoginWindow():
        messagebox.showwarning('Warning', 'Are you sure you want to logout?')
        window.destroy()
        from logInWindow.main import logInWindow
        logInWindow()


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
        searchInputTextBox.insert('0.0', "Search Clinics by Name or Address")
        searchInputTextBox.configure(text_color='gray')


    # def filterTree(event):
    #     searchTerm = searchInputTextBox.get('0.0', "end").lower()
    #     table.delete(*table.get_children()) # Clear the current Treeview

    #     # Connecting to Clinic Admin DB
    #     clinicAdminConn = sqlite3.connect('clinicAdmins.db')
    #     clinicAdminCursor = clinicAdminConn.cursor()

    #     # Fetch filtered data from the database
    #     clinicAdminCursor.execute("""
    #         SELECT ClinicAdminID, FirstName, LastName, Email, Role, IsApproved 
    #         FROM clinicAdmins 
    #         WHERE ClinicAdminID LIKE ? OR FirstName LIKE ? OR LastName LIKE ? OR Email LIKE ? OR Role LIKE ?
    #     """, ('%'+searchTerm+'%', '%'+searchTerm+'%', '%'+searchTerm+'%', '%'+searchTerm+'%', '%'+searchTerm+'%'))
    #     rows = clinicAdminCursor.fetchall()

    #     # Insert filtered data into the Treeview
    #     for row in rows:
    #         table.insert("", "end", values=row)


    global count
    count = 0
    def insertTreeview():
        global count
        # Connecting to Clinic Admin DB
        clinicAdminConn = sqlite3.connect('clinicAdmins.db')
        clinicAdminCursor = clinicAdminConn.cursor()
        clinicAdminCursor.execute('SELECT * FROM clinicAdmins')
        clinicAdmins = clinicAdminCursor.fetchall()
        table.delete(*table.get_children())

        for clinicAdmin in clinicAdmins:
            clinicID = clinicAdmin[0]
            clinicName = clinicAdmin[7]
            clinicContact = clinicAdmin[9]
            adminName = f"{clinicAdmin[1]} {clinicAdmin[2]}"
            adminEmail = clinicAdmin[3]
            if clinicAdmin[10] == 0:
                isApproved = 'Waiting For Approval'
            elif clinicAdmin[10] == 1:
                isApproved = 'Approved'
            else:
                isApproved = 'Rejected'

            data = (clinicID, clinicName, clinicContact, adminName, adminEmail, isApproved)


            if count % 2 == 0:
                table.insert(parent='', index='end', values=data, tags=("evenrow",))
                print(clinicAdmin)
            else:
                table.insert(parent='', index='end', values=data, tags=("oddrow",))

            count += 1

    def approveClinic():
        # Connecting to Clinic Admin DB
        clinicAdminConn = sqlite3.connect('clinicAdmins.db')
        clinicAdminCursor = clinicAdminConn.cursor()

        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select a Clinic first.')
            return


        clinicData = table.item(selectedItem)["values"]
        clinicAdminID = clinicData[0]
        clinicName = clinicData[1]
        isApproveStatus = clinicData[5]
        

        if isApproveStatus == 'Approved':
            messagebox.showinfo('Info', f'{clinicName} is already approved.')
        else:
            
            clinicAdminCursor.execute('UPDATE clinicAdmins SET IsApproved=? WHERE ClinicAdminID=?', (1, clinicAdminID))
            clinicAdminConn.commit()
            clinicAdminConn.close()
            insertTreeview()
            messagebox.showinfo('Success', f'{clinicName} has just been approved successfully. \nTheir Clinic Admin will be notified.')

    
    def rejectClinic():
        # Connecting to Clinic Admin DB
        clinicAdminConn = sqlite3.connect('clinicAdmins.db')
        clinicAdminCursor = clinicAdminConn.cursor()

        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select a Clinic first.')
            return


        clinicData = table.item(selectedItem)["values"]
        clinicAdminID = clinicData[0]
        clinicName = clinicData[1]
        isApproveStatus = clinicData[5]
        

        if isApproveStatus == 'Rejected':
            messagebox.showinfo('Info', f'{clinicName} is already rejected.')
        else:
            
            clinicAdminCursor.execute('UPDATE clinicAdmins SET IsApproved=? WHERE ClinicAdminID=?', (2, clinicAdminID))
            clinicAdminConn.commit()
            clinicAdminConn.close()
            insertTreeview()
            messagebox.showinfo('Success', f'{clinicName} has just been rejected. \nTheir Clinic Admin will be notified.')
            

    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Admin Window)")
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
    logoutButton.pack(side="bottom", fill='y', expand=True, padx=(35, 0), pady=(395, 0))


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

    greetingLabel1 = ctk.CTkLabel(whiteFrame, text="Welcome, Someshwar Rao", font=("Inter", 36, "bold",), text_color="#000000")
    greetingLabel1.place(x=25, y=25)
    greetingLabel2 = ctk.CTkLabel(whiteFrame, text=f"{greeting}  ({formatted_date})", font=("Inter", 22,), text_color="#000000")
    greetingLabel2.place(x=25, y=72)
    roleLabel = ctk.CTkLabel(whiteFrame, text="(Admin)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=880, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Manage Clinic Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Manage Clinics", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="Manage the clinic registrations after verifying with Malaysian Registered Doctor System", 
        )
    descLabel.place(x=25, y=182)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
            whiteFrame, fg_color="#ffffff", text_color="gray", width=660, height=50, 
            border_color="#000", font=("Inter", 21), border_spacing=8,
            scrollbar_button_color="#1AFF75", border_width=2,
        )
    searchInputTextBox.insert('insert', "Search Clinics by Name or Address")
    searchInputTextBox.place(x=25, y=225)
    searchInputTextBox.bind("<FocusIn>", searchbarFocus)
    searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)
    searchInputTextBox.bind("<KeyRelease>", filterTree)


    # Approve Button with Icon
    approveIconPath = relative_to_assets("approve-icon.png")
    approveIcon = ctk.CTkImage(light_image=Image.open(approveIconPath), size=(33,33),)
    approveButton = ctk.CTkButton(
        whiteFrame, text=" Approve ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#00C16A", hover_color="#009B2B", image=approveIcon,
        command=approveClinic # anchor=ctk.W 
    )
    approveButton.place(x=700, y=225)

    # Reject Button with Icon
    rejectIconPath = relative_to_assets("reject-icon.png")
    rejectIcon = ctk.CTkImage(light_image=Image.open(rejectIconPath), size=(33,33),)
    rejectButton = ctk.CTkButton(
        whiteFrame, text=" Reject  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=rejectIcon,
        command=rejectClinic # anchor=ctk.W 
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
        'ID', 'Clinic Name', 'Clinic Contact',
        "Clinic Admin", "Admin Email", 'Approval Status'
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
    style.map('Treeview', background=[('selected', '#00BE97',)], font=[('selected', ('Inter', 16, 'bold'))],)

    # Treeview Table Headings Details
    table.heading('ID', text='ID',)
    table.heading('Clinic Name', text='Clinic Name')
    table.heading('Clinic Contact', text='Clinic Contact')
    table.heading('Clinic Admin', text='Clinic Admin')
    table.heading('Admin Email', text='Admin Email')
    table.heading('Approval Status', text='Approval Status')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("ID", width=43, anchor=ctk.CENTER)
    table.column("Clinic Name", width=220, anchor=ctk.CENTER)
    table.column("Clinic Contact", anchor=ctk.CENTER)
    table.column("Clinic Admin", width=250, anchor=ctk.CENTER)
    table.column("Admin Email", width=270, anchor=ctk.CENTER,)
    table.column("Approval Status", width=260, anchor=ctk.CENTER)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")

    
    insertTreeview()

    window.mainloop()


# Only execute the Admin Window if this script is run directly
if __name__ == "__main__":
    adminDashboardWindow()