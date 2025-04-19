import os
import shutil

# Path to the original COCO dataset folder (train2017 images)
source_folder = r"C:\radna povrsina\materijal za fakultet\Cloud Computing and Big Data Technologies\coco2017\train2017"

# Path to your project images_subset/ folder
destination_folder = r"C:\radna povrsina\materijal za fakultet\Cloud Computing and Big Data Technologies\image-pipeline-project\images_subset"

# Limit the number of images to copy
MAX_IMAGES = 10000

# List all image filenames in the source folder
all_images = os.listdir(source_folder)

# Print how many images were found
print(f"Total images in COCO folder: {len(all_images)}")

# Copy only the first MAX_IMAGES files
for i, image_name in enumerate(all_images[:MAX_IMAGES]):
    src_path = os.path.join(source_folder, image_name)
    dest_path = os.path.join(destination_folder, image_name)
    shutil.copy2(src_path, dest_path)

    if i % 1000 == 0:
        print(f"[+] Copied {i} images...")

print("✅ Done! Images successfully copied.")
