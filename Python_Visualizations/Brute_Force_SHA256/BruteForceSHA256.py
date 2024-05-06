import hashlib
import itertools
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import os
import string

def sha256_hash(data):
    h = hashlib.sha256()
    h.update(data.encode())
    return h.hexdigest()

def update_plot(ax, guess):
    ax.clear()
    ax.axis('off')
    ax.text(0.5, 0.5, f"Guess: {guess}", fontsize=12, ha='center', va='center', color='black')

def brute_force_attack(target_hash, charset, max_length, ax=None):
    if ax is not None:
        ax.axis('off')

    for length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=length):
            guess_str = ''.join(guess)
            hashed_guess = sha256_hash(guess_str)
            #hashed_guess = guess_str
            if hashed_guess == target_hash:
                return guess_str
            if ax is not None:
                update_plot(ax, guess_str)
                plt.savefig(f"brute_force_frames/frame_{length:03d}.png")  # Save each guess with correct length

    return None

def create_animation(frames_folder, duration=500):
    images = [Image.open(os.path.join(frames_folder, filename)) for filename in sorted(os.listdir(frames_folder))]
    images[0].save("brute_force_animation.gif",
                   save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)

def main(target_password, charset, max_length, frames_folder):
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    fig, ax = plt.subplots()
    guess = brute_force_attack(target_password, charset, max_length, ax)

    while guess is None:
        guess = brute_force_attack(target_password, charset, max_length, ax)

    if guess:
        print(f"Password cracked: {guess}")
    else:
        print("Failed to crack the password.")

    create_animation(frames_folder)
    plt.show()

# Example usage
if __name__ == "__main__":
    target_password = "1"
    #charset = "0123456789"  # Character set for brute force
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~"
    max_length = 3  # Maximum length of the password (increased for better demonstration)
    frames_folder = "brute_force_frames"

    main(target_password, charset, max_length, frames_folder)
