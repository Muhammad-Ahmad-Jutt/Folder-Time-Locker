import os
import shutil
from datetime import datetime
from tqdm import tqdm

def zip_with_progress(location, password, output_zip_file_path):
    # Check if the input is a file or a folder
    if os.path.isfile(location):
        # Compress a single file
        file_name = os.path.basename(location)
        with pyzipper.AESZipFile(output_zip_file_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            with open(location, 'rb') as f:
                zipf.writestr(file_name, f.read())
    elif os.path.isdir(location):
        # Compress an entire folder
        with pyzipper.AESZipFile(output_zip_file_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            for foldername, subfolders, filenames in os.walk(location):
                for filename in tqdm(filenames, desc="Compressing", unit="file"):
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, location)
                    zipf.write(file_path, arcname)
    else:
        print("Invalid input. The location must be a valid file or folder.")

def unzip_with_progress(zip_file_path, password, extraction_path=None):
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r', encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            file_list = zipf.namelist()

            # Create the extraction directory if it doesn't exist
            if extraction_path is None:
                extraction_path = os.path.dirname(zip_file_path)
            os.makedirs(extraction_path, exist_ok=True)

            # Extract the contents of the zip file with progress tracking
            for file_name in tqdm(file_list, desc="Extracting", unit="file"):
                file_data = zipf.read(file_name)
                with open(os.path.join(extraction_path, file_name), 'wb') as f:
                    f.write(file_data)

        print("Unzipped successfully.")
    except ValueError as e:
        print("Error: Incorrect password.")
    except Exception as e:
        print(f"Error: {str(e)}")
