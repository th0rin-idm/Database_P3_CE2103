import os

def folder_generator(path, name):
    # Granting write permissions
    os.chmod(path, 0o777)
    # Create the folder
    folder_path = os.path.join(path, name)
    os.makedirs(folder_path)

    
