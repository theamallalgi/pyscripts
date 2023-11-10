import os
import re
from datetime import datetime
import random
import string

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

# # Define a regular expression pattern to match the original filenames
# pattern = r'IMG_(\d{8})_(\d{6})'

# # Function to convert the filename
# def convert_filename(filename):
#     match = re.search(pattern, filename)
#     if match:
#         date_part, time_part = match.groups()
#         date = datetime.strptime(date_part, "%Y%m%d").strftime("%d-%m-%Y")
#         time = time_part[:2] + "-" + time_part[2:4] + "-" + time_part[4:]
#         base_name, extension = os.path.splitext(filename)
#         new_filename = f"IMG-({date})-[{time}]{extension}"
#         return new_filename
#     else:
#         return None

# # Create a 'skipped' subfolder if it doesn't already exist
# skipped_folder = os.path.join(directory, 'skipped')
# if not os.path.exists(skipped_folder):
#     os.mkdir(skipped_folder)

# # List all files in the directory
# files = os.listdir(directory)

# # Rename the files with the new format and handle duplicates
# for filename in files:
#     new_filename = convert_filename(filename)
#     if new_filename:
#         base_name, extension = os.path.splitext(new_filename)
#         original_path = os.path.join(directory, filename)
#         while os.path.exists(os.path.join(directory, new_filename)):
#             # Handle duplicates by incrementing the sequence number
#             base_name, extension = os.path.splitext(new_filename)
#             index = 1
#             while True:
#                 new_filename = f"{base_name} ({index}){extension}"
#                 if not os.path.exists(os.path.join(directory, new_filename)):
#                     break
#                 index += 1
#         new_path = os.path.join(directory, new_filename)
#         os.rename(original_path, new_path)
#         print(f'Renamed: {filename} -> {new_filename}')
#     else:
#         original_path = os.path.join(directory, filename)
#         # Check if it's not a directory before moving
#         if not os.path.isdir(original_path):
#             # Move the skipped file to the 'skipped' subfolder
#             skipped_path = os.path.join(skipped_folder, filename)
#             os.rename(original_path, skipped_path)
#             print(f'Skipped: {filename} (moved to "skipped" subfolder)')

# Define a regular expression pattern to match the original filenames
pattern = r'IMG-(\d{8})-WA00(\d+)\.\w+'

# Function to convert the filename
def convert_filename(filename):
    match = re.search(pattern, filename)
    if match:
        date_part, random_part = match.groups()
        date = datetime.strptime(date_part, "%Y%m%d")
        new_date = date.strftime("%d-%m-%Y")
        # Generate random time components (hh-MM-ss)
        random_time = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        new_filename = f"IMG-({new_date})[{random_time}]{os.path.splitext(filename)[1]}"
        return new_filename
    else:
        return None

# Create a 'skipped' subfolder if it doesn't already exist
skipped_folder = os.path.join(directory, 'skipped')
if not os.path.exists(skipped_folder):
    os.mkdir(skipped_folder)

# List all files in the directory
files = os.listdir(directory)

# Rename the files with the new format and handle duplicates
for filename in files:
    new_filename = convert_filename(filename)
    if new_filename:
        base_name, extension = os.path.splitext(new_filename)
        original_path = os.path.join(directory, filename)
        while os.path.exists(os.path.join(directory, new_filename)):
            # Handle duplicates by incrementing the sequence number
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
        original_path = os.path.join(directory, filename)
        # Check if it's not a directory before moving
        if not os.path.isdir(original_path):
            # Move the skipped file to the 'skipped' subfolder
            skipped_path = os.path.join(skipped_folder, filename)
            os.rename(original_path, skipped_path)
            print(f'Skipped: {filename} (moved to "skipped" subfolder)')