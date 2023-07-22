import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import ntplib

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
    def set_unlock_date():
        unlock_date = selectiondate.get_date()
        zip_and_lock_folder(location, unlock_date)

    location = filedialog.askdirectory()
    if location:
        zipwindow = tk.Toplevel(root)
        location_label = tk.Label(zipwindow, text=location, bg='green')
        selectiondate = DateEntry(zipwindow)
        date_today = tk.Label(zipwindow, text=get_current_date_string)
        location_label.pack(padx=5, pady=5)
        selectiondate.pack(padx=5, pady=5)
        date_today.pack(padx=10, pady=10)
        # Button to set the unlock date
        unlock_date_button = tk.Button(zipwindow, text="Set Unlock Date", command=set_unlock_date)
        unlock_date_button.pack()

def zip_and_lock_folder(folder_path, unlock_date):
    # Zip the folder and set a password
    zip_file_name = f"{folder_path}_{unlock_date.strftime('%y-%m-%d')}.zip"
    lock_info_file = f"{folder_path}_lock_info.txt"

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file))

    # Create a lock_info.txt file with creation date and unlock date
    with open(lock_info_file, 'w') as lock_info:
        lock_info.write(f"Creation Date: {get_current_time().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lock_info.write(f"Unlock Date: {unlock_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # Save the unlock date in a file or database
    # For simplicity, we'll just print it for now.
    print(f"Folder locked until: {unlock_date}")

def unzip_window():
    print("unzip")

# Our main window and its widgets
root = tk.Tk()
root.geometry("150x150")
root.title("Lock folder app")

# Main buttons
zip_b = tk.Button(root, text="Zip", command=zip_window)
unzip_b = tk.Button(root, text="Unzip", command=unzip_window)
exit_b = tk.Button(root, text="Exit", bg='red', command=root.quit)
zip_b.grid(row=0, column=0, padx=10, pady=20)
unzip_b.grid(row=0, column=1, padx=10, pady=20)
exit_b.grid(row=1, column=1, padx=10, pady=20)

root.mainloop()
