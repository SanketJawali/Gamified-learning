import os

def get_chapter_content(filename):
    # Define the base directory
    chapters_dir = os.path.join("templates", "chapters")

    # Construct full file path
    filepath = os.path.join(chapters_dir, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Chapter '{filename}' not found in {chapters_dir}/ directory"
        )
    except PermissionError:
        raise PermissionError(
            f"Permission denied reading {filepath}"
        )
    except UnicodeDecodeError:
        # Fallback to binary if UTF-8 fails
        with open(filepath, 'rb') as file:
            return file.read().decode('utf-8', errors='replace')
