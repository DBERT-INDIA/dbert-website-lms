import os
import zipfile

ZIP_PATH = os.path.abspath('dbert-api-package-v1.zip')
SOURCE_DIR = os.path.abspath('dbert-api-package')

EXCLUDE_DIRS = {'__pycache__', '.pytest_cache', 'node_modules', '.next', '.git'}
EXCLUDE_EXTS = {'.pyc', '.pyo', '.DS_Store'}

def regenerate_zip():
    print(f"Regenerating {ZIP_PATH} from {SOURCE_DIR}...")
    temp_zip = ZIP_PATH + '.tmp'
    
    file_count = 0
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(SOURCE_DIR):
            # prune excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in sorted(files):
                ext = os.path.splitext(file)[1]
                if ext in EXCLUDE_EXTS or file in EXCLUDE_EXTS:
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, os.path.dirname(SOURCE_DIR))
                # Standardize to forward slashes for zip archive
                arc_name = rel_path.replace(os.sep, '/')
                z.write(full_path, arc_name)
                file_count += 1
                
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    os.rename(temp_zip, ZIP_PATH)
    print(f"Successfully created {ZIP_PATH} with {file_count} files.")

if __name__ == '__main__':
    regenerate_zip()
