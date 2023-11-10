import os
import re
from datetime import datetime

# Get the current directory
current_directory = os.getcwd()

# List all the items (files and folders) in the current directory
items = os.listdir(current_directory)

# Filter the items to get only the folders
folders = [item for item in items if os.path.isdir(item)]

# folder name
processingFolder = input("• Which folder should I check in? : ")

# Get the directory path of the script and join it with 'images' folder
script_dir = os.path.dirname(os.path.abspath(__file__))
# Check if the folder is in the list
if processingFolder not in folders:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"ERROR: Unable to find the folder '{processingFolder}'!")
    exit()
else:
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print(f"━ Checking for Images in '{processingFolder}'")
    folder_path = os.path.join(script_dir, processingFolder)

# Directory where your image files are located
directory = folder_path

# Define a regular expression pattern to match the original filenames
pattern = r'(\d{2})(\d{2})(\d{2})-(\d{4})'

# Function to convert the filename
def convert_filename(filename):
    base_name, extension = os.path.splitext(filename)
    match = re.search(pattern, base_name)
    if match:
        day, month, year, time = match.groups()
        # Convert the year from "yy" to "yyyy" format
        year = f"20{year}"
        # Construct the new filename with the original file extension
        new_filename = f"IMG-({day}-{month}-{year})-[{time[:2]}-{time[2:]}]{extension}"
        return new_filename
    else:
        return None

# Search for image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

# Create a dictionary to keep track of filename counts
filename_counts = {}

# List all files in the directory
files = os.listdir(directory)

# Create a 'skipped' subfolder if it doesn't already exist
skipped_folder = os.path.join(directory, 'skipped')
if not os.path.exists(skipped_folder):
    os.mkdir(skipped_folder)

# Rename the files with the new format
for filename in files:
    new_filename = convert_filename(filename)
    if new_filename:
        original_path = os.path.join(directory, filename)
        while os.path.exists(os.path.join(directory, new_filename)):
            # Handle duplicates by incrementing the index
            base_name, extension = os.path.splitext(new_filename)
            index = 1
            while True:
                new_filename = f"{base_name} ({index}){extension}"
                if not os.path.exists(os.path.join(directory, new_filename)):
                    break
                index += 1
        new_path = os.path.join(directory, new_filename)
        os.rename(original_path, new_path)
        print(f'Renamed: {filename} -> {new_filename}')
    else:
        # Move the skipped file to the 'skipped' subfolder
        skipped_path = os.path.join(skipped_folder, filename)
        original_path = os.path.join(directory, filename)
        os.rename(original_path, skipped_path)
        print(f'Skipped: {filename} (moved to "skipped" subfolder)')

