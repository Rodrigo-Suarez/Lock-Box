
def get_existing(existing):
    if existing == "" or existing == None or existing.lower() == "false":
        return False
    if existing.lower() == "true":
        return True
    if type(existing) is not bool:
        raise ValueError("'existing' must be an boolean.")


def get_replace_existing(replace_existing):
    if replace_existing == "" or replace_existing == None or replace_existing.lower()== "false":
        return False
    if replace_existing.lower() == "true":
        return True
    if type(replace_existing) is not bool:
        raise ValueError("'replace_existing' must be an boolean.")
    

def get_folder(folder):
    if folder == "" or folder == None or int(folder) == 0:
        return None
    folder = int(folder)
    return folder


def get_change(change):
    if change == "" or change == None or change.lower()== "false":
        return False
    if change.lower() == "true":
        return True
    if type(change) is not bool:
        raise ValueError("'change' must be an boolean.")
    

def get_new_folder(folder):
    if folder == "" or folder == None:
        return
    if int(folder) == 0:
        return "root"
    folder = int(folder)
    return folder


