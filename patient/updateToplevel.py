import sys
from pathlib import Path
from PIL import Image
import sqlite3
from datetime import datetime
from tkintermapview import TkinterMapView
from tkcalendar import *
from patientDashboard import patientDashboardWindow
from patientDashboardWindow import insertTreeView

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\patient\assets\frame0")


def updateAppointmentTopLevel():

    def updateAppointment():  
        clinicName = clinicNameDropdown.get()
        doctorType = doctorTypeDropdown.get()
        painDetails = painDetailsTextBox.get(0.0, 'end').strip()
        doctorName = doctorDropdown.get()
        date = calendar.get_date()
        time = consultationTimeDropdown.get()
        duration = consultationDurationDropdown.get()

        if (clinicName != '' and doctorType != '' and painDetails != '' and doctorName != '' and date != '' and 
            time != '' and duration != ''):

            if clinicName == 'Clinic Name':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select a Clinic.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            
            if doctorType == 'Select Type':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select the Type of Doctor.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            
            if doctorName == 'Select Doctor':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select a Doctor.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            
            if time == 'Select Time':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select the Consultaion Time.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            
            if duration == 'Select Duration':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select the Consultaion Duration.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            

            updateQuery = '''
                UPDATE appointments
                SET DoctorName = ?, DoctorType = ?, ClinicName = ?, AppointmentDate = ?, AppointmentTime = ?, AppointmentDuration = ?, PainDetails = ?
                WHERE AppointmentID = ? '''

            appointmentCursor.execute(
                updateQuery, (doctorName, doctorType, clinicName, date, time, duration, painDetails, appointmentID))
            appointmentConn.commit()

            toplevel.attributes("-topmost",False)
            messagebox.showinfo('Success', 'Appointment updated successfully.')
            toplevel.destroy()
            insertTreeview()
            
        
        else:
            toplevel.attributes("-topmost",False)
            messagebox.showerror('Error',"Please fill up all the fields.")
            if messagebox:
                toplevel.attributes("-topmost",True)


    now = datetime.now()  # Get the current date and time
    todayInt = now.day # Get the current date in integer
    thisMonth = now.month # Get the current month in integer
    thisYear = now.year # Get the current year in integer
    formatted_date = now.strftime("%B %d, %Y") # Format the date as 'Month Day, Year'
    current_hour = now.hour # Get the current hour
    current_time = now.strftime("%H:%M:%S") # Get the current time

    selectedItem = table.focus()
    if not selectedItem:
        messagebox.showerror('Error', 'Select an Appointment first.')
        return
    
    appointmentData = table.item(selectedItem)["values"]
    print(appointmentData)
    appointmentID = appointmentData[6]
    print(appointmentID)


    toplevel = ctk.CTkToplevel(window)
    toplevel.title("Update Appointment")
    toplevel.geometry("800x600+460+100")
    toplevel.resizable(False, False)
    toplevel.attributes("-topmost",True)
    toplevel.configure(fg_color = "#fff")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    parentFrame = ctk.CTkScrollableFrame(toplevel, width=800, height=600, fg_color="#fff", scrollbar_fg_color="#000", scrollbar_button_color="#000",)
    parentFrame.place(x=0, y=0)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    topFrame = ctk.CTkFrame(parentFrame, width=650, height=500, fg_color="#FFFDFD" )
    topFrame.pack(side='top', fill='x', expand=False, padx=(65, 80), pady=(20,0))
    
    # Select Clinic Dropdown Menu
    clinicNameLabel = ctk.CTkLabel(topFrame, text="Select Clinic", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    clinicNameLabel.pack(side='top', fill='x', expand=False)
    clinicNameDropdown = ctk.CTkComboBox(
        topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Clinic Name', 'Panmedic', 'Health Sync', 'Clinic Sungai Ara'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    clinicNameDropdown.pack(side='top', fill='x', expand=False,)

    gMapsWidget = TkinterMapView(topFrame, width=650, height=400)
    gMapsWidget.pack(side='top', fill='x', expand=True, pady=(10,0), padx=(0,5))
    gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
    gMapsWidget.set_address("Bayan Lepas, Penang, Malaysia", marker=True)
    gMapsWidget.set_zoom(12)

    # gMapsWidget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
    # gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=e...{x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
    # gMapsWidget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
    # marker.set_text("Select A Clinic")
    

    doctorTypeLabel = ctk.CTkLabel(topFrame, text="Select Type Of Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    doctorTypeLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
    doctorTypes = [
        "Select Type","Allergist", "Cardiologist", "Dermatologist", "Endocrinologist", 
        "Gastroenterologist", "Geriatrician", "Internist", "Nephrologist", "Neurologist", 
        "Obstetrician/Gynecologist", "Oncologist", "Ophthalmologist", "Orthopedic Surgeon", 
        "Pediatrician", "Podiatrist", "Psychiatrist", "Pulmonologist", "Rheumatologist", 
        "General Practitioner", "Family Medicine Doctor", "Home Health Care Doctor", 
        "Emergency Medicine Specialist"]
    doctorTypeDropdown = ctk.CTkComboBox(
        topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=doctorTypes, border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    doctorTypeDropdown.pack(side='top', fill='x', expand=False, pady=(0,0), padx=(0,5))

    painDetailsLabel = ctk.CTkLabel(topFrame, text="Explain Pain Details", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    painDetailsLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
    painDetailsTextBox = ctk.CTkTextbox(
        topFrame, fg_color="#ffffff", text_color="#000000", width=648, height=88, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    painDetailsTextBox.pack(side='top', fill='none', expand=False, pady=(0, 10), anchor="w")


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSDIE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
    leftFrame.pack(side='left', fill='both', expand=False, padx=65, pady=30)

    doctorDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    doctorDropdownLabel.pack(side='top', fill='x', expand=False,)
    doctorDropdown = ctk.CTkComboBox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Select Doctor', 'Maisarah Majdi', 'Someshwar Rao', 'Karen Khor Siew Li'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    doctorDropdown.pack(side='top', fill='x', expand=False,)

    times = [
        "Select Time",'9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM'
    ]
    consultationTimeDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Consultation Time", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    consultationTimeDropdownLabel.pack(side='top', fill='x', expand=False, pady=(150,0))
    consultationTimeDropdown = ctk.CTkComboBox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=times, border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    consultationTimeDropdown.pack(side='top', fill='x', expand=False,)

    # Cancel Button with Icon
    cancelIconPath = relative_to_assets("reject-icon.png")
    cancelIcon = ctk.CTkImage(light_image=Image.open(cancelIconPath), size=(33,33),)
    cancelButton = ctk.CTkButton(
        leftFrame, text=" Cancel ", width=280, height=60, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelIcon,
        command=toplevel.destroy # anchor=ctk.W 
    )
    cancelButton.pack(side='top', fill='x', expand=False,pady=(40,15))


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RIGHT FRAME INSIDE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    rightFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD",)
    rightFrame.pack(side='left', fill='both', expand=False, padx=(0,0), pady=30)
    

    # Select Consultation Date Widget
    consultationDateLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Date", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    consultationDateLabel.pack(side='top', fill='x', expand=False,)
    calendar = Calendar(
        rightFrame, selectmode="day", year=thisYear, font=("Inter", 12),
        month=thisMonth, day=todayInt, background="#1AFF75", 
        selectbackground="#36D8B7", foreground="black"
    )
    calendar.pack(side='top', fill='x', expand=False,)

    # Select Consultation Duration Dropdown Menu
    durationArray = [
        'Select Duration', '1 hour', '1 hour 30 Minutes',
        '2 hours', '2 hours 30 Minutes', '3 hours', '3 hour 30 Minutes', '4 hours', 
        '4 hours 30 Minutes', '5 hours'
    ]
    consultationDurationDropdownLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Duration", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    consultationDurationDropdownLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
    consultationDurationDropdown = ctk.CTkComboBox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=durationArray, border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    consultationDurationDropdown.pack(side='top', fill='x', expand=False,)

    # Book Button 2 with Icon
    updateIconPath = relative_to_assets("update-icon.png")
    updateIcon = ctk.CTkImage(light_image=Image.open(updateIconPath), size=(33,33),)
    updateButton = ctk.CTkButton(
        rightFrame, text=" Update Appointment Details", height=48, width=378,
        font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=updateIcon,
        command=updateAppointment # anchor=ctk.W 
    )
    updateButton.pack(side='top', fill='x', expand=False,pady=(40,15))

    # Connecting to Appointment DB
    appointmentConn = sqlite3.connect('appointments.db')
    appointmentCursor = appointmentConn.cursor()

    appointmentCursor.execute('SELECT * FROM appointments WHERE AppointmentID=?', [appointmentID])
    result = appointmentCursor.fetchone()
    print(result)

    clinicName = clinicNameDropdown.set(result[7])
    doctorType = doctorTypeDropdown.set(result[6])
    painDetails = painDetailsTextBox.insert('insert', result[13])
    doctorName = doctorDropdown.set(result[3])
    date = calendar.selection_set(result[9])
    time = consultationTimeDropdown.set(result[10])
    duration = consultationDurationDropdown.set(result[11])