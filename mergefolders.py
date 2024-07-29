import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

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
    folder_path = filedialog.askdirectory(title="Select a Folder to Merge")
    if folder_path:
        selected_folders.append(folder_path)
        update_folders_label()

# Function to select the destination folder
def select_destination_folder():
    return filedialog.askdirectory(title="Select Destination Folder")

# Function to start merging process
def start_merge():
    if not selected_folders:
        messagebox.showwarning("Warning", "Please select folders to merge.")
        return
    destination_folder = select_destination_folder()
    if not destination_folder:
        messagebox.showwarning("Warning", "Please select a destination folder.")
        return
    source_folder_name = os.path.basename(selected_folders[0])
    destination_folder = os.path.join(destination_folder, f"{source_folder_name}_merged")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    merge_folders(selected_folders, destination_folder)
    print("Success!")
    messagebox.showinfo("Success", "Folders merged successfully!")

# Function to update the label with selected folders
def update_folders_label():
    folders_label.config(text="\n".join(selected_folders))

# Global variable to store selected folders
selected_folders = []

# Set up the GUI
root = tk.Tk()
root.title("Folder Merger")
root.geometry("400x300")

# Add a button to select folders
select_button = tk.Button(root, text="Add Folder to Merge", command=select_folders)
select_button.pack(pady=10)

# Label to show selected folders
folders_label = tk.Label(root, text="No folders selected.", justify="left")
folders_label.pack(pady=10)

# Add a button to start the merge process
merge_button = tk.Button(root, text="Start Merge", command=start_merge)
merge_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
