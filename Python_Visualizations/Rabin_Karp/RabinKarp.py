import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

def rabin_karp_search(text, pattern, d, q):
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0
    t = 0
    positions = []
    comparisons = 0

    for i in range(m):  # Preprocessing
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):  # Search
        if p == t:
            match = True
            for j in range(m):
                if pattern[j] != text[s+j]:
                    match = False
                    comparisons += 1
                    break
            if match:
                comparisons += 1
                positions.append(s)
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s+m])) % q
            if t < 0:
                t += q
            comparisons += 1

        yield s, comparisons

    yield -1, comparisons

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
    ax.set_title(f'Rabin-Karp Algorithm - Comparisons: {comparisons}')

# Example usage
text = "AABAACAADAABAABA"
pattern = "AABA"
d = 256
q = 101
n = len(text)
m = len(pattern)

indices_found = []
comparisons_total = 0

for index, comparisons in rabin_karp_search(text, pattern, d, q):
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
anim = FuncAnimation(fig, update_plot, frames=rabin_karp_search(text, pattern, d, q), interval=1000)

frame_count = 0

# Save each frame as an image
for frame_data in rabin_karp_search(text, pattern, d, q):
    update_plot(frame_data)
    plt.savefig(f"frames/frame_{frame_count:03d}.png")
    frame_count += 1

# Combine frames into a GIF using Pillow
images = []
for filename in sorted(os.listdir("frames")):
    images.append(Image.open(os.path.join("frames", filename)))

images[0].save("rabin_karp_animation.gif",
               save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0)

# Display the animation
plt.show()

# Cleanup: Remove the frames folder
for filename in os.listdir("frames"):
    os.remove(os.path.join("frames", filename))
os.rmdir("frames")

print("GIF animation created successfully.")
