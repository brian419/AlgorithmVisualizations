import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    j = 0
    
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j
    
    return lps

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    j = 0
    
    positions = []
    comparisons = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            comparisons += 1
            j = lps[j - 1]
        if text[i] == pattern[j]:
            comparisons += 1
            j += 1
        if j == m:
            positions.append(i - m + 1)
            j = lps[j - 1]
            yield i - m + 1, comparisons  # Yield the position of the match and comparisons made
    
    yield -1, comparisons  # Indicate end of search

def update_plot(frame_data):
    frame, comparisons = frame_data
    if frame == -1:
        return
    ax.clear()
    ax.set_xlim(-1, n)
    ax.set_ylim(-1, 1)
    
    for i in range(n):
        ax.text(i, 0, text[i], ha='center', va='center')
    
    for i in range(frame, frame + m):
        ax.text(i, -0.5, pattern[i - frame], ha='center', va='center', color='red')
    
    ax.plot([frame, frame + m - 1], [-0.5, -0.5], 'g-', linewidth=2)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'KMP Algorithm - Comparisons: {comparisons}')

# Example usage
text = "AABAACAADAABAABA"
pattern = "AABA"
n = len(text)
m = len(pattern)

indices_found = []
comparisons_total = 0

for index, comparisons in kmp_search(text, pattern):
    if index == -1:
        break
    indices_found.append(index)
    comparisons_total += comparisons

print(f"Pattern found at indices: {indices_found}")
#print(f"Total comparisons made: {comparisons_total}")

# Create a frames folder if it doesn't exist
if not os.path.exists("frames"):
    os.makedirs("frames")

fig, ax = plt.subplots()
anim = FuncAnimation(fig, update_plot, frames=kmp_search(text, pattern), interval=1000)

frame_count = 0

# Save each frame as an image
for frame_data in kmp_search(text, pattern):
    update_plot(frame_data)
    plt.savefig(f"frames/frame_{frame_count:03d}.png")
    frame_count += 1

# Combine frames into a GIF using Pillow
images = []
for filename in sorted(os.listdir("frames")):
    images.append(Image.open(os.path.join("frames", filename)))

images[0].save("kmp_animation.gif",
               save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0)

# Display the animation
plt.show()

# Cleanup: Remove the frames folder
for filename in os.listdir("frames"):
    os.remove(os.path.join("frames", filename))
os.rmdir("frames")

print("GIF animation created successfully.")
