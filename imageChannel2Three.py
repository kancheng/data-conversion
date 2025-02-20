import os
import cv2
from PIL import Image

"""
Automatic image channel conversion
Convert all images to 3-channel (RGB)
"""

colpath = []
path = './imgs'

for root, dirs, files in os.walk(path):
    print("ROOT : ", root)
    print("DIRS : ", dirs)
    print("FILES : ", files)

# Collect all image file paths
for root, dirs, files in os.walk(path):
    for img in files:
        if img.endswith((".png", ".jpg", ".jpeg", ".bmp")):
            colpath.append(root + "/" + img)

print("ALL PATH : ", colpath)

for c in colpath:
    img = Image.open(c)
    # Directly output the number of channels of the image
    print("INFO. IMG.: ", img, "; Channels : ", len(img.split()), "; Details : ", img.split())
    
    # Convert to 3 channels (RGB)
    if len(img.split()) != 3:
        img = img.convert("RGB")
    
    # Save the converted image
    img.save(c)