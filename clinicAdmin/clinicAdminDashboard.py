import sys
from pathlib import Path
from PIL import Image
import sqlite3

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\clinicAdmin\assets\frame0")

def clinicAdminDashboardWindow(email):
    # Helper function to get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Function to redirect to the Log In Window
    def redirectToLoginWindow():
        msg = messagebox.askokcancel('Warning', 'Are you sure you want to logout?')

        if msg:
            window.destroy()
            from logInWindow.main import logInWindow
            logInWindow()


    # Redirect to the Clinic Admin Doctor Window
    def redirectToClinicAdminDoctorWindow():
        window.destroy()
        from clinicAdmin.clinicAdminDoctors import clinicAdminDoctorWindow
        clinicAdminDoctorWindow(email)


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
        searchInputTextBox.insert('0.0', "Search by Patient Name or Doctor Name ")
        searchInputTextBox.configure(text_color='gray')


    global count
    count = 0
    def insertTreeview(array=None):
        global count

        # Connecting to Clinic Admin DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        appointmentCursor.execute('SELECT * FROM appointments')
        appointments = appointmentCursor.fetchall()
        table.delete(*table.get_children())

        # Executed when searchbar is entered
        if array is None:
            for appointment in appointments:
                appointmentID = appointment[0]
                patientName = appointment[1]
                doctorType = appointment[5]
                doctorName = appointment[3]
                availability = appointment[6]
                if appointment[14] == 0:
                    isConfirmed = 'Waiting For Confirmation'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                else:
                    isConfirmed = 'Doctor Replaced'

                data = (appointmentID, patientName, doctorType, doctorName, availability, isConfirmed)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))

                count += 1
        
        # Executed when Approve Button is clicked
        else:
            for appointment in array:
                appointmentID = appointment[0]
                patientName = appointment[1]
                doctorType = appointment[5]
                doctorName = appointment[3]
                availability = appointment[6]
                if appointment[14] == 0:
                    isConfirmed = 'Waiting For Confirmation'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                else:
                    isConfirmed = 'Doctor Replaced'

                data = (appointmentID, patientName, doctorType, doctorName, availability, isConfirmed)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
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
            

    def searchBy():
        # Connecting to Clinic Admin DB
        clinicAdminConn = sqlite3.connect('clinicAdmins.db')
        clinicAdminCursor = clinicAdminConn.cursor()
        searchTerm = searchInputTextBox.get('0.0', 'end').strip()
        searchOption = searchByDropdown.get()

        if searchOption == 'Clinic Admin ID':
            searchOption = "ClinicAdminID"
        elif searchOption == 'Clinic Name':
            searchOption = "ClinicName"
        elif searchOption == 'Clinic Contact':
            searchOption = "ClinicNumber"
        elif searchOption == 'Admin Email':
            searchOption = "Email"
        elif searchOption == 'Approval Status':
            searchOption = "IsApproved"

            if searchTerm == 'Waiting For Approval':
                searchTerm = '0'
            elif searchTerm == 'Approved':
                searchTerm = '1'
            elif searchTerm == 'Rejected':
                searchTerm = '2'


        if searchTerm == "":
            messagebox.showerror('Error', 'Enter value to search.')
        elif searchOption == 'Search By Option':
            messagebox.showerror('Error', 'Please select an option.')
        else:
            clinicAdminCursor.execute(f'SELECT * FROM clinicAdmins WHERE {searchOption}=?', (searchTerm,))
            result = clinicAdminCursor.fetchall()
            insertTreeview(result)



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
        font=("Inter", 26, "bold",), fg_color="#37D8B7", hover_color="#37D8B7", image=dashboardIcon,
        # anchor=ctk.W
    )
    dashboardButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=25)

    # Doctor Button with Icon
    doctorIconPath = relative_to_assets("doctor-icon.png")
    doctorIcon = ctk.CTkImage(light_image=Image.open(doctorIconPath), size=(44,44),)
    doctorButton = ctk.CTkButton(
        sidebarFrame, text=" Doctors     ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=doctorIcon,
        command=redirectToClinicAdminDoctorWindow
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
    greetingLabel1 = ctk.CTkLabel(whiteFrame, text="Welcome, Someshwar Rao", font=("Inter", 36, "bold",), text_color="#000000")
    greetingLabel1.place(x=25, y=25)
    greetingLabel2 = ctk.CTkLabel(whiteFrame, text="Good Morning!  (January 26, 2024)", font=("Inter", 22,), text_color="#000000")
    greetingLabel2.place(x=25, y=72)
    roleLabel = ctk.CTkLabel(whiteFrame, text="(Clinic Admin)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=775, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Manage Appointment Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Manage Appointments", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="Manage the patient appointments after verifying with the doctor availability  ", 
        )
    descLabel.place(x=25, y=182)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
            whiteFrame, fg_color="#ffffff", text_color="gray", width=485, height=50, 
            border_color="#000", font=("Inter", 21), border_spacing=8,
            scrollbar_button_color="#1AFF75", border_width=2,
        )
    searchInputTextBox.insert('insert', "Search by Patient Name or Doctor Name ")
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
    approveButton.place(x=525, y=225)

    # Reject Button with Icon
    rejectIconPath = relative_to_assets("reject-icon.png")
    rejectIcon = ctk.CTkImage(light_image=Image.open(rejectIconPath), size=(33,33),)
    rejectButton = ctk.CTkButton(
        whiteFrame, text=" Reject  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=rejectIcon,
        # anchor=ctk.W 
    )
    rejectButton.place(x=695, y=225)


    # Reassign Button with Icon
    reassignIconPath = relative_to_assets("reassign-icon.png")
    reassignIcon = ctk.CTkImage(light_image=Image.open(reassignIconPath), size=(33,33),)
    reassignButton = ctk.CTkButton(
        whiteFrame, text=" Reassign  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=reassignIcon,
        # anchor=ctk.W 
    )
    reassignButton.place(x=850, y=225)


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
        'ID', 'Patient Name', 'Doctor Type',
        "Doctor Name", "Availability", "Confirmation Status"
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
    table.heading('ID', text='ID')
    table.heading('Patient Name', text='Patient Name')
    table.heading('Doctor Type', text='Doctor Type')
    table.heading('Doctor Name', text='Doctor Name')
    table.heading('Availability', text='Availability')
    table.heading('Confirmation Status', text='Confirmation Status')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("ID", width=43, anchor=ctk.CENTER)
    table.column("Patient Name", width=220, anchor=ctk.CENTER)
    table.column("Doctor Type", anchor=ctk.CENTER)
    table.column("Doctor Name", width=250, anchor=ctk.CENTER)
    table.column("Availability", width=270, anchor=ctk.CENTER,)
    table.column("Confirmation Status", width=260, anchor=ctk.CENTER)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")


    # <<<<<<<<<<<<<<<<<<<< AUTOMATED TESTING >>>>>>>>>>>>>>>>>>>>>
    # global count
    # count = 0
    # #     if count % 2 == 0:
    # #         table.insert(parent='', index=0, values=data, tags=("evenrow",))
    # #     else:
    # #         table.insert(parent='', index=0, values=data, tags=("oddrow",))

    # clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    # adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']



    # for i in range(15):
    #     num = (i+1)
    #     clinicID = ''.join(random.choices('0123456789', k=12))
    #     clinicName = choice(clinicNames)
    #     clinicContact = ''.join(random.choices('0123456789', k=8))
    #     clinicContact = f'+01{clinicContact}'
    #     adminName = choice(adminNames)
    #     adminEmail = f'{(adminName.replace(" ", "")).lower()}@email.com'

    #     data = (num, clinicID, clinicName, clinicContact, adminName, adminEmail)
    #     if count % 2 == 0:
    #         table.insert(parent='', index='end', values=data, tags=("evenrow",))
    #     else:
    #         table.insert(parent='', index='end', values=data, tags=("oddrow",))

    #     count += 1

    # # Test the insertion in table
    # def testTableInsertion():
    #     clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    #     clinicAddress = ["Kuala Lumpur", "George Town", "Ipoh", "Johor Bahru", "Kota Kinabalu", "Shah Alam", "Malacca City", "Alor Setar", "Kuantan", "Kuching"]
    #     adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']

    #     for name in adminNames:
    #         email = name.replace(" ", "")

    #     for i in range(10):
    #         num = i
    #         clinicID = ''.join(random.choices('0123456789', k=12))
    #         clinicName = choice(clinicNames)
    #         clinicContact = ''.join(random.choices('0123456789', k=8))
    #         clinicAddress = choice(clinicAddress)
    #         adminName = choice(adminNames)
    #         adminEmail = f'{email}@email.com'

    #         data = (num, clinicID, clinicName, clinicContact, clinicAddress, adminName, adminEmail)
    #         if count % 2 == 0:
    #             table.insert(parent='', index=0, values=data, tags=("evenrow",))
    #         else:
    #             table.insert(parent='', index=0, values=data, tags=("oddrow",))

    #         count += 1
    

    insertTreeview()
    window.mainloop()


# Only execute the Clinic Admin Dashboard Window if this script is run directly
if __name__ == "__main__":
    clinicAdminDashboardWindow(email=None)