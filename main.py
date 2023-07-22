import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
import ntplib
from datetime import datetime

def get_current_date_string():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        current_date = datetime.fromtimestamp(response.tx_time)
        date_string = current_date.strftime("%d--%m--%Y")
        return date_string
    except ntplib.NTPException:
        return "Error: Unable to fetch current date from NTP server."

def zip_window():
    location = filedialog.askdirectory()
    if location:
        zipwindow = tk.Toplevel(root)
        location_label = tk.Label(zipwindow, text=location, bg='green')
        selectiondate = DateEntry(zipwindow)
        today_date = tk.Label(zipwindow, text=get_current_date_string())

        
# now lets import date and time from the internet
        location_label.pack(padx=5, pady=5)
        selectiondate.pack(padx=5, pady=5)
        today_date.pack(padx=10, pady=10)

def unzip_window():
    print("unzip")

#out main window and its widgets
root = tk.Tk()
root.geometry("150x150")
root.title("Lock folder app")
# we will create the main buttons
zip_b = tk.Button(root, text="Zip", command=zip_window)
unzip_b = tk.Button(root, text="Unzip", command=unzip_window)
exit_b = tk.Button(root, text="Exit",bg='red', command=root.quit)
zip_b.grid(row=0, column=0, padx=10, pady=20)
unzip_b.grid(row=0, column=1, padx=10, pady=20)
exit_b.grid(row=1, column=1, padx=10, pady=20)




root.mainloop()