# file2image

file2image is a Python-based utility that allows you to easily embed and hide files or folders inside PNG images. It supports optional strong AES-GCM encryption to securely protect your embedded files.

## Features

- **Convert File/Folder to Image:** Compress and encode any file or entire directory structure into a pixel array saved as a PNG image.
- **Encrypt Data:** Add an extra layer of security by encrypting your files with a password before they are embedded into the image.
- **Extract Data:** Quickly decode and extract your original files or folders back from the generated images using your password (if encrypted).
- **Directory Support:** Automatically archives (ZIP) directories in the background before processing.

## Requirements

Ensure you have Python 3 installed. Then, install the required dependencies from the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Dependencies Included:
- `numpy`
- `Pillow`
- `colorama`
- `cryptography`

## Usage

Start the interactive Command Line Interface (CLI) by running:

```bash
python main.py
```

### Main Menu Options:

When you run the script, you will be presented with a menu.
1. **Convert Normal File / Folder to Image:** Enter `1`, then provide the path to the file/folder and the desired output image name.
2. **Create Encrypted File / Folder to Image:** Enter `2`, provide the path, output name, and a secure encryption key to encrypt the data before steganography.
3. **Extract File / Folder from Image:** Enter `3`, provide the path to the image. If the image is encrypted, you will be prompted for the password to extract and decrypt the original data.
4. **Quit:** Enter `q` to exit the tool.

## Disclaimer

This project is created for educational purposes. Make sure you remember your encryption key, as it is impossible to retrieve encrypted data without it.
