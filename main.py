import os
import shutil
import colorama
import numpy as np
from PIL import Image
from core import file_to_image, extract_file_from_image

ascii_art = r"""
   __ _ _      ___  _                            
  / _(_) |    |__ \(_)                           
 | |_ _| | ___   ) |_ _ __ ___   __ _  __ _  ___ 
 |  _| | |/ _ \ / /| | '_ ` _ \ / _` |/ _` |/ _ \
 | | | | |  __// /_| | | | | | | (_| | (_| |  __/
 |_| |_|_|\___|____|_|_| |_| |_|\__,_|\__, |\___|
                                       __/ |     
                                      |___/      """

def main():
    while True:
        print(ascii_art)
        print("\n--- TOOLS ---")
        print("1 - Convert Normal File / Folder to Image")
        print("2 - Create Encrypted File / Folder to image")
        print("3 - Extract File / Folder from Image")
        print("q - Quit")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            break
            
        if choice in ['1', '2']:
            path = input("Enter file or folder path: ").strip()
            
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]
            elif path.startswith("'") and path.endswith("'"):
                path = path[1:-1]
                
            if not os.path.exists(path):
                print("Error: The specified path could not be found!")
                continue
            
            output = input("Output image name (e.g., secret.png): ").strip()
            temp_to_delete = None
            process_path = path
            
            if os.path.isdir(path):
                print("Folder detected. Archiving in the background (ZIP)...")
                target_name = path.rstrip(os.sep)
                shutil.make_archive(target_name, 'zip', path)
                process_path = f"{target_name}.zip"
                temp_to_delete = process_path
            
            if choice == '1':
                file_to_image(process_path, output, is_crypto=False)
            elif choice == '2':
                key = input("Enter encryption key: ")
                file_to_image(process_path, output, is_crypto=True, password=key)
                
            if temp_to_delete and os.path.exists(temp_to_delete):
                try:
                    os.remove(temp_to_delete)
                    print("Temporary ZIP file created for the folder has been cleaned up.")
                except OSError as e:
                    print(f"Warning: Failed to clean up temporary ZIP file: {e}")
                
        elif choice == '3':
            path = input("Enter image path: ").strip()
            
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]
            elif path.startswith("'") and path.endswith("'"):
                path = path[1:-1]
                
            if not os.path.exists(path):
                print("Error: Image not found!")
                continue
                
            try:
                with Image.open(path) as image:
                    image_array = np.array(image, dtype=np.uint8).flatten()
                    if len(image_array) > 0:
                        first_byte = image_array[0]
                    else:
                        print("Error: Image is empty!")
                        continue
                
                if first_byte == 1:
                    key = input("This image is encrypted! Enter key: ")
                    extract_file_from_image(path, password=key)
                else:
                    extract_file_from_image(path)
            except Exception as e:
                print(f"Error processing image: {e}")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()