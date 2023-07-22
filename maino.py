import os
import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar
import zipfile
from datetime import datetime, timedelta
import ntplib

expiration_time_var = None  # Global variable to hold the expiration time

def zip_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Open the second window
        second_window(folder_path)

def second_window(folder_path):
    global expiration_time_var  # Make sure to access the global variable

    def set_unlock_date():
        cal_date = cal.get_date()
        expiration_time_var.set(cal_date.strftime("%m/%d/%y"))
        cal_label.config(text="Selected Unlock Date: " + expiration_time_var.get())
        cal.destroy()

    def zip_and_lock_folder():
        unlock_date_str = expiration_time_var.get()
        unlock_date = datetime.strptime(unlock_date_str, "%m/%d/%y")
        current_time = get_current_time()

        if current_time < unlock_date:
            lock_folder(folder_path, unlock_date)
        else:
            print("Unlock date must be in the future.")

    def lock_folder(folder_path, unlock_date):
        # Zip the folder and set a password
        zip_file_name = f"{folder_path}_{unlock_date.strftime('%y-%m-%d')}.zip"
        lock_info_file = os.path.join(folder_path, "lock_info.txt")

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

    def get_current_time():
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')

        if response:
            return datetime.fromtimestamp(response.tx_time)
        else:
            return datetime.now()

    second_window = tk.Toplevel(root)
    second_window.title("Zip and Lock Folder")

    # Display selected folder path
    selected_folder_label = tk.Label(second_window, text="Selected Folder:")
    selected_folder_label.pack()
    selected_folder_path_label = tk.Label(second_window, text=folder_path)
    selected_folder_path_label.pack()

    # Calendar for setting the unlock date
    cal = Calendar(second_window, selectmode="day")
    cal.pack(pady=10)

    # Button to set the unlock date
    unlock_date_button = tk.Button(second_window, text="Set Unlock Date", command=set_unlock_date)
    unlock_date_button.pack()

    # Label to display the selected unlock date
    cal_label = tk.Label(second_window, text="")
    cal_label.pack()

    # Zip and lock button
    zip_button = tk.Button(second_window, text="Zip and Lock", command=zip_and_lock_folder)
    zip_button.pack()

# Function to unzip the folder if the unlock date has arrived
def unzip_folder():
    zip_file_path = filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
    if zip_file_path:
        unlock_date_str = zip_file_path.split('_')[-1].split('.')[0]
        unlock_date = datetime.strptime(unlock_date_str, "%y-%m-%d")
        current_time = get_current_time()

        if current_time >= unlock_date:
            unzip_folder_with_password(zip_file_path)
        else:
            print("Unlock date not reached.")

def unzip_folder_with_password(zip_file_path):
    # Read the lock_info.txt file to check unlock date
    folder_path = os.path.dirname(zip_file_path)
    lock_info_file = os.path.join(folder_path, "lock_info.txt")

    with open(lock_info_file, 'r') as lock_info:
        lock_info_lines = lock_info.readlines()
        creation_date_str = lock_info_lines[0].split(': ')[1].strip()
        unlock_date_str = lock_info_lines[1].split(': ')[1].strip()

    creation_date = datetime.strptime(creation_date_str, "%Y-%m-%d %H:%M:%S")
    unlock_date = datetime.strptime(unlock_date_str, "%Y-%m-%d %H:%M:%S")
    current_time = get_current_time()

    if current_time >= unlock_date:
        # Unzip the folder
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            zipf.extractall(folder_path)
        print("Folder successfully unzipped.")
    else:
        print("Unlock date not reached.")

# Main window
root = tk.Tk()
root.title("Zip and Unzip Program")

# Zip button
zip_button = tk.Button(root, text="Zip", command=zip_folder)
zip_button.pack(pady=20)

# Unzip button
unzip_button = tk.Button(root, text="Unzip", command=unzip_folder)
unzip_button.pack(pady=20)

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()
