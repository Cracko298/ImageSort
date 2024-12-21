import os
import shutil
import hashlib
from PIL import Image

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.avif', '.heif'}

def calculate_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            img_hash = hashlib.md5(img.tobytes()).hexdigest()
        return img_hash
    except Exception as e:
        print(f"Error calculating hash for {image_path}: {e}")
        return None

def copy_unique_images(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    seen_hashes = set()
    copied_count = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                image_hash = calculate_image_hash(file_path)

                if image_hash and image_hash not in seen_hashes:
                    seen_hashes.add(image_hash)
                    dest_path = os.path.join(target_dir, file)

                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                        counter += 1

                    shutil.copy2(file_path, dest_path)
                    copied_count += 1
                elif image_hash:
                    print(f"Duplicate found: {file_path}")

    print(f"Total unique images copied: {copied_count}")

source_directory = str(input("Give the Head Directory for the Images: ")).replace("\\", "/")
target_directory = ".\\imagesOut"
copy_unique_images(source_directory, target_directory)
