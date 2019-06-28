import os
import shutil

def replace_spaces_with_underscore(parent_path):
    # https://stackoverflow.com/questions/41176509/python-how-to-replace-whitespaces-by-underscore-in-the-name-of-all-files-folde
    # Renames the folder and file names within the (also relative) 
    # directory parent_path to be Unix friendly
    # -> Changes spaces to _
    """   
    for path, folders, files in os.walk(parent_path):
        for f in files:
            os.rename(os.path.join(path, f), os.path.join(path, f.replace(' ', '_')))
        for i in range(len(folders)):
            new_name = folders[i].replace(' ', '_')
            os.rename(os.path.join(path, folders[i]), os.path.join(path, new_name))
            folders[i] = new_name
    """
    # https://stackoverflow.com/questions/225735/batch-renaming-of-files-in-a-directory
    #[os.rename(f, f.replace(' ', '_')) for f in os.listdir(parent_path) if not f.startswith('.')]

    # https://askubuntu.com/questions/771225/remove-leading-whitespace-from-files-folders-and-their-subfolders
    for root, dirs, files in os.walk(parent_path, topdown=False):
        for f in files:
            if " " in f:
                shutil.move(root+"/"+f, root+"/"+f.replace(" ", "_"))
        for dr in dirs:
            if " " in dr:
                shutil.move(root+"/"+dr, root+"/"+dr.replace(" ", "_"))