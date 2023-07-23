import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
import ntplib, os, pyzipper
from tqdm import tqdm
from datetime import datetime
import pandas as pd
def get_current_date_string():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        current_date = datetime.fromtimestamp(response.tx_time)
        date_string = current_date.strftime("%Y-%m-%d")
        return date_string
    except :
        return "2023-07-23"
def count_numbers(s):
    num_str = ""
    for char in s:
        if char.isdigit():
            num_str += char
        else:
            break
    return num_str if num_str else 0

def unzip_file_with_password(zip_file_path, password):
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r', encryption=pyzipper.WZ_AES) as zipf:
            zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]
            output_folder = os.path.join(os.path.dirname(zip_file_path), zip_file_name)
            os.makedirs(output_folder, exist_ok=True)

            zipf.setpassword(password.encode())
            zipf.extractall(path=output_folder)

        print("Unzipped successfully.")
    except ValueError as e:
        print("Error: Incorrect password.")
    except Exception as e:
        print(f"Error: {str(e)}")







def zip_file_or_folder(location, password, output_zip_file_name):
    # Check if the input is a file or a folder
    if os.path.isfile(location):
        # Compress a single file
        file_name = os.path.basename(location)
        with pyzipper.AESZipFile(output_zip_file_name, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            with open(location, 'rb') as f:
                zipf.writestr(file_name, f.read())
                print("Sucessfully write the file")
    elif os.path.isdir(location):
        # Compress an entire folder
        with pyzipper.AESZipFile(output_zip_file_name, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            for foldername, subfolders, filenames in os.walk(location):
                for filename in tqdm(filenames, desc="Compressing", unit="file"):
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, location)
                    zipf.write(file_path, arcname)
                    print("sucessfully write to folder")
    else:
        print("Invalid input. The location must be a valid file or folder.")



def zipfile(location, s_date, t_date):
    s_date = s_date.get_date()
    t_date = t_date["text"]
    t_date = datetime.strptime(t_date, "%Y-%m-%d").date()
    duration = s_date - t_date
    duration = count_numbers(str(duration))
    
    #selection date must be greater then the today date
    if s_date >= t_date:
        #Frist we will set the name of the file 
        start_date_str = s_date.strftime("%Y-%m-%d")
        today_date_str = t_date.strftime("%Y-%m-%d")
        file_name = f"Locked_From_{today_date_str}_To_{start_date_str}"
        # to remember when the file will be unlocked
        with open('date', 'w') as file:
            file.write(file_name)
        file.close
        try:
            s_date = datetime.strftime(s_date, "%Y-%m-%d")
            zip_file_or_folder(location, s_date, "output.zip")
        except:
            print("error while zipping")
    else:
        print("invalid date")
def zip_window():
    location = filedialog.askopenfilename()
    if location:
        zipwindow = tk.Toplevel(root)
        location_label = tk.Label(zipwindow, text=location, bg='green')
        selectiondate = DateEntry(zipwindow, date_pattern='dd-mm-yyyy')
        today_date = tk.Label(zipwindow, text=get_current_date_string())
        status_l = tk.Label(zipwindow, text=" ")
        start_b = tk.Button(zipwindow, text='Start Compression', command=lambda : zipfile(location, selectiondate, today_date))
        cancel_b = tk.Button(zipwindow, text='Cancel', command=zipwindow.destroy)
# now lets import date and time from the internet
        location_label.pack(padx=5, pady=5)
        selectiondate.pack(padx=5, pady=5)
        today_date.pack(padx=10, pady=10)
        status_l.pack(padx=10, pady=10)
        start_b.pack(padx=10, pady=10)
        cancel_b.pack(padx=10, pady=10)
def unzip_window():
    password = get_current_date_string()
    location = filedialog.askopenfilename()
    if location:
        unzip_file_with_password(location, password)
    else:
        print("can't find")
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