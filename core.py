import numpy as np
from PIL import Image
import math
import struct
import os
import zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from crypto import generate_key

def file_to_image(file_path, output_image_path, is_crypto=False, password=None):
    _, extension = os.path.splitext(file_path)
    extension_bytes = extension.encode('utf-8')
    extension_length = len(extension_bytes)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    compressed_data = zlib.compress(data, level=9)
    is_crypto_byte = 1 if is_crypto else 0
    
    if is_crypto:
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = generate_key(password, salt)
        aesgcm = AESGCM(key)
        processed_data = aesgcm.encrypt(nonce, compressed_data, None)
        data_size = len(processed_data)
        
        header = struct.pack(f'>BB{extension_length}s16s12sQ', 
                             is_crypto_byte, extension_length, extension_bytes, salt, nonce, data_size)
    else:
        processed_data = compressed_data
        data_size = len(processed_data)
        
        header = struct.pack(f'>BB{extension_length}sQ', 
                             is_crypto_byte, extension_length, extension_bytes, data_size)
        
    full_data = bytearray(header) + bytearray(processed_data)
    total_bytes = len(full_data)
    
    required_pixels = math.ceil(total_bytes / 3)
    width = math.ceil(math.sqrt(required_pixels))
    height = math.ceil(required_pixels / width) if width > 0 else 1
    
    missing_bytes = (width * height * 3) - total_bytes
    if missing_bytes > 0:
        full_data += bytearray(missing_bytes)
    
    array = np.array(full_data, dtype=np.uint8).reshape((height, width, 3))
    image = Image.fromarray(array, 'RGB')
    
    if not output_image_path.lower().endswith('.png'):
        output_image_path += '.png'
        
    image.save(output_image_path, 'PNG', compress_level=9)
    
    status = "Encrypted" if is_crypto else "Normal"
    print(f"Task Successful! {status} data converted to image -> {output_image_path}")

def extract_file_from_image(image_path, output_folder=".", password=None):
    try:
        with Image.open(image_path) as image:
            array = np.array(image, dtype=np.uint8).flatten()
    except Exception as e:
        print(f"Error: Could not open image: {e}")
        return
        
    if len(array) < 2:
        print("Error: Image contains insufficient data.")
        return
        
    is_crypto = array[0]
    extension_length = array[1]
    offset = 2
    
    if offset + extension_length > len(array):
        print("Error: Image data is corrupted.")
        return
        
    extension = bytes(array[offset:offset+extension_length]).decode('utf-8', errors='ignore')
    offset += extension_length
    
    if is_crypto == 1:
        if not password:
            print("This file is encrypted! You must enter a key to extract it.")
            return
            
        if offset + 16 + 12 + 8 > len(array):
            print("Error: Image data is corrupted.")
            return

        salt = bytes(array[offset:offset+16])
        offset += 16
        nonce = bytes(array[offset:offset+12])
        offset += 12
        size_bytes = bytes(array[offset:offset+8])
        data_size = struct.unpack('>Q', size_bytes)[0]
        offset += 8
        
        if offset + data_size > len(array):
            print("Error: Extracted data size mismatch! Image may be corrupted.")
            return

        encrypted_data = bytes(array[offset:offset+data_size])
        key = generate_key(password, salt)
        aesgcm = AESGCM(key)
        
        try:
            compressed_data = aesgcm.decrypt(nonce, encrypted_data, None)
        except Exception:
            print("Error: Incorrect password or corrupted file!")
            return
    else:
        if offset + 8 > len(array):
            print("Error: Image data is too short.")
            return

        size_bytes = bytes(array[offset:offset+8])
        data_size = struct.unpack('>Q', size_bytes)[0]
        offset += 8
        
        if offset + data_size > len(array):
            print("Error: Extracted data size mismatch! Image may be corrupted.")
            return
            
        compressed_data = bytes(array[offset:offset+data_size])
        
    try:
        original_data = zlib.decompress(compressed_data)
    except Exception:
        print("Error: Decompression failed. Data may be corrupted.")
        return
    
    output_filename = f"extracted_data{extension}"
    output_filepath = os.path.join(output_folder, output_filename)
    
    try:
        with open(output_filepath, 'wb') as f:
            f.write(original_data)
        print(f"Data successfully extracted -> {output_filepath}")
    except OSError as e:
        print(f"Error while writing file: {e}")
