import os
import shutil
import tkinter as tk
from tkinter import filedialog

# Function to merge folders
def merge_folders(source_folders, dest_folder):
    for folder in source_folders:
        for item in os.listdir(folder):
            source_path = os.path.join(folder, item)
            destination_path = os.path.join(dest_folder, item)

            if os.path.isdir(source_path):
                if not os.path.exists(destination_path):
                    shutil.copytree(source_path, destination_path)
                else:
                    merge_folders([source_path], destination_path)
            else:
                if not os.path.exists(destination_path):
                    shutil.copy2(source_path, destination_path)
                else:
                    # Rename and move if a file with the same name exists
                    base, extension = os.path.splitext(item)
                    i = 1
                    new_name = f"{base}_{i}{extension}"
                    new_destination_path = os.path.join(dest_folder, new_name)
                    while os.path.exists(new_destination_path):
                        i += 1
                        new_name = f"{base}_{i}{extension}"
                        new_destination_path = os.path.join(dest_folder, new_name)
                    shutil.copy2(source_path, new_destination_path)

# Function to select folders
def select_folders():
    folder_paths = filedialog.askdirectory(multiple=True)
    return folder_paths

# Function to start merging process
def start_merge():
    source_folders = select_folders()
    if source_folders:
        source_folder_name = os.path.basename(source_folders[0])
        destination_folder = filedialog.askdirectory(initialdir="/", title="Select Destination Folder")
        destination_folder = os.path.join(destination_folder, f"{source_folder_name}_merged")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        merge_folders(source_folders, destination_folder)
        print("Success!")
        tk.messagebox.showinfo("Success", "Folders merged successfully!")

# Set up the GUI
root = tk.Tk()
root.title("Folder Merger")
root.geometry("300x200")

# Add a button to start the merge process
merge_button = tk.Button(root, text="Select Folders to Merge", command=start_merge)
merge_button.pack(expand=True)

# Run the GUI event loop
root.mainloop()
