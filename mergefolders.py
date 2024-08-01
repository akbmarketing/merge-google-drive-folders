import os
import os.path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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
                    base, extension = os.path.splitext(item)
                    i = 1
                    new_name = f"{base}_{i}{extension}"
                    new_destination_path = os.path.join(dest_folder, new_name)
                    while os.path.exists(new_destination_path):
                        i += 1
                        new_name = f"{base}_{i}{extension}"
                        new_destination_path = os.path.join(dest_folder, new_name)
                    shutil.copy2(source_path, new_destination_path)

def select_folders():
    downloads_path = os.path.expanduser("~/Downloads")
    folder_path = filedialog.askdirectory(title="Select a Folder to Merge", initialdir=downloads_path)
    if folder_path:
        selected_folders.append(folder_path)
        update_folders_label()

def select_destination_folder():
    return filedialog.askdirectory(title="Select Destination Folder")

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
    messagebox.showinfo("Success", "Merged successfully!")

def update_folders_label():
    if selected_folders:
        folders_text = "\n".join(selected_folders)
        folders_label.config(text=folders_text, fg="black")
    else:
        folders_label.config(text="No folders selected.", fg="#333")

def reset_folders():
    global selected_folders
    selected_folders = []
    update_folders_label()

def on_enter(e):
    e.widget['style'] = 'Hover.Custom.TButton'

def on_leave(e):
    e.widget['style'] = 'Custom.TButton'

selected_folders = []

root = tk.Tk()
root.title("Folder Merger")
root.geometry("400x500")

style = ttk.Style()
style.configure('Custom.TButton', 
                font=('Arial', 10, 'bold'),
                padding=[12, 8],
                background='#488aec',
                foreground='#ffffff',
                borderwidth=0,
                relief='flat')
style.map('Custom.TButton', 
          background=[('active', '#488aec')],
          relief=[('pressed', 'flat'), ('!pressed', 'flat')])
style.configure('Hover.Custom.TButton', 
                background='#3a7cde')

main_frame = tk.Frame(root, bg="#F8F9FD")
main_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=25)

heading = tk.Label(main_frame, text="Folder Merger", font=("Arial", 24, "bold"), fg="#1089D3", bg="#F8F9FD")
heading.pack(pady=20)

select_button = ttk.Button(main_frame, text="Add Folders to Merge", command=select_folders, style='Custom.TButton')
select_button.pack(pady=10, fill=tk.X)

folders_label = tk.Label(main_frame, text="No folders selected.", justify="left", bg="#F8F9FD", wraplength=350, fg="#333")
folders_label.pack(pady=10)

merge_button = ttk.Button(main_frame, text="Start Merge", command=start_merge, style='Custom.TButton')
merge_button.pack(pady=10, fill=tk.X)

reset_button = ttk.Button(main_frame, text="Reset Folders", command=reset_folders, style='Custom.TButton')
reset_button.pack(pady=10, fill=tk.X)

for btn in (select_button, merge_button, reset_button):
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
