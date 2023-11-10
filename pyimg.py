import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

print('''
┏━━━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ┏┓  ┳┳┳┓┏┓╻  ┃ ┃ Convert your images based on it's creation time!  ┃
┃ ┃┃┓┏┃┃┃┃┃┓┃  ┃ ┃ The images will be renamed in the format :        ┃
┃ ┣┛┗┫┻┛ ┗┗┛•  ┃ ┃ • IMG-(dd-mm-yyyy)[hh-MM-ss].file                 ┃
┃    ┛         ┃ ┃ • (.jpg, .png, .jpeg, .gif, .bmp)                 ┃
┗━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  ''')

# ┏━━━━━━━━━┓
# ┃    ┓┏   ┃
# ┫    ┗┛   ┣
# ┗━━━━━━━━━┛

# Get the current directory
current_directory = os.getcwd()

# List all the items (files and folders) in the current directory
items = os.listdir(current_directory)

# Filter the items to get only the folders
folders = [item for item in items if os.path.isdir(item)]

# Display the list of folders
print("  Folders in the current directory: ")
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
if not folders :
    print("ERROR: I Could'nt find any folders here :(")
else :
    for folder in folders:
        print(f' ━ {folder}/')
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

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

# Define the path for the 'failed' folder
failed_folder = os.path.join(script_dir, 'failed')

# Create the 'failed' folder if it doesn't exist
if not os.path.exists(failed_folder):
    os.makedirs(failed_folder)

# Function to get the creation date of an image
def get_image_creation_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "DateTimeOriginal":
                return value
        return None
    except (IOError, AttributeError):
        return None

# Search for image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

# Print the total number of images before conversion
total_images = len(image_files)
print(f"• Total number of images before conversion: {total_images}")

# Initialize counters for converted and failed images
converted_count = 0
failed_count = 0

# Move files without a creation date to the 'failed' folder
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    creation_date = get_image_creation_date(image_path)

    if creation_date:
        # print(f"{image_file}: Created on {creation_date}")
        # Convert the creation date string to a datetime object
        creation_date = datetime.strptime(creation_date, "%Y:%m:%d %H:%M:%S")
        # Rename the image file with the formatted creation date
        creation_date_str = creation_date.strftime("(%d-%m-%Y)-[%H-%M-%S]")
        new_filename = f"IMG-{creation_date_str}{os.path.splitext(image_file)[1]}"

        # Get the file extension
        file_extension = os.path.splitext(image_file)[1]
        
        # Create the new filename with a loop to handle duplicates
        new_filename = f"img-{creation_date_str}{file_extension}"
        count = 1
        while os.path.exists(os.path.join(folder_path, new_filename)):
            new_filename = f"img-{creation_date_str}({count}){file_extension}"
            count += 1
        new_path = os.path.join(folder_path, new_filename)
        os.rename(image_path, new_path)
        converted_count += 1
    else:
        # print(f"{image_file}: Creation date not found")
        # Move the image to the 'failed' folder
        failed_path = os.path.join(failed_folder, image_file)
        shutil.move(image_path, failed_path)
        failed_count += 1

# Display the number of converted and failed images
print(f"• Number of converted images: {converted_count}")
print(f"• Number of failed images: {failed_count}")
print(f"• unconverted image(s) moved to '{failed_folder}'")
print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')