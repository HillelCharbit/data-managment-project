import os
from moviepy.editor import ImageSequenceClip
from PIL import Image


# Set the path to the directory containing your screenshots
image_folder = 'C:\\Users\\ASUS\\data-managment-project-1\\python-impl\\screenshots'

# Get a list of all image file names in the folder
image_files = [os.path.join(image_folder, img)
               for img in os.listdir(image_folder)
               if img.endswith(".png") or img.endswith(".jpg")]

# Find the maximum width and height of all images
max_width = 0
max_height = 0
for img_file in image_files:
    img = Image.open(img_file)
    max_width = max(max_width, img.width)
    max_height = max(max_height, img.height)

# Pad all images to the maximum width and height
for img_file in image_files:
    img = Image.open(img_file)
    padded_img = Image.new("RGB", (max_width, max_height), (255, 255, 255))  # White background
    padded_img.paste(img, (int((max_width - img.width) / 2), int((max_height - img.height) / 2)))
    padded_img.save(img_file)

# Set the output video file name
output_video_file = 'output_video.mp4'

# Get a sorted list of image file names
image_files = sorted([os.path.join(image_folder, img)
                      for img in os.listdir(image_folder)
                      if img.endswith(".png") or img.endswith(".jpg")])

# Create a video clip from the images
fps = 1  # Frames per second
clip = ImageSequenceClip(image_files, fps=fps)

# Write the video file
clip.write_videofile(output_video_file, codec='libx264', fps=fps)
