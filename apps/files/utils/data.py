from apps.files.models import File

def generate_file_data(file, user_id, unique_filename, folder):
    data = {
            "name": file.name,
            "unique_name": unique_filename,
            "type": file.content_type,
            "author": user_id,
            "folder": folder,
            "content": File.generate_url(unique_filename),
            "size": file.size 
        }
    return data


def generate_history_data(file_db, unique_filename, user_id):
    data = {
            "file": file_db.id,
            "history_author": user_id,
            "history_unique_name": unique_filename,
            "history_version": file_db.version,
            "history_content": File.generate_url(unique_filename),
            "history_size": file_db.size
        }
    return data

def generate_folder_data(name, user_id, parent_folder):
    data = {
            "name": name, 
            "author": user_id, 
            "parent_folder": parent_folder
        }
    return data