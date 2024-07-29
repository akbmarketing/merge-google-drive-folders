import os
import shutil


folders_to_merge = [
    "/Users/andrewbourguignon/Downloads/drive-download-20240728T194731Z-001",
    "/Users/andrewbourguignon/Downloads/drive-download-20240728T194731Z-002",
]
destination_folder = '/Users/andrewbourguignon/Downloads/Merged Emu GDrive'


if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)


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

# Merge the folders
merge_folders(folders_to_merge, destination_folder)

print("Success!")
