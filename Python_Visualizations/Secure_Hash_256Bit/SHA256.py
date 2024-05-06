import hashlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import os

def sha256_visualization(data):
    h = hashlib.sha256()
    h.update(data.encode())
    digest = h.hexdigest()
    return digest

def update_plot(frame_data):
    global ax
    ax.clear()
    ax.axis('off')
    ax.text(0.5, 0.5, frame_data, fontsize=12, ha='center', va='center', color=get_color(frame_data))

def get_color(frame_data):
    # Convert the hexadecimal hash value to RGB color
    r = int(frame_data[:2], 16) / 255.0
    g = int(frame_data[2:4], 16) / 255.0
    b = int(frame_data[4:6], 16) / 255.0
    return (r, g, b)

# Example usage
data = "Hello, world!"
digest = sha256_visualization(data)

fig, ax = plt.subplots()
anim = FuncAnimation(fig, update_plot, frames=[digest[i:i+8] for i in range(0, len(digest), 8)], interval=1000)

frames_folder = "sha256_frames"
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

frame_count = 0

for frame_data in [digest[i:i+8] for i in range(0, len(digest), 8)]:
    update_plot(frame_data)
    plt.savefig(f"{frames_folder}/frame_{frame_count:03d}.png")
    frame_count += 1

images = []
for filename in sorted(os.listdir(frames_folder)):
    images.append(Image.open(os.path.join(frames_folder, filename)))

images[0].save("sha256_animation.gif",
               save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0)

plt.show()

for filename in os.listdir(frames_folder):
    os.remove(os.path.join(frames_folder, filename))
os.rmdir(frames_folder)

print("SHA-256 animation created successfully.")
