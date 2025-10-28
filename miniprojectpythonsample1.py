import random
import tkinter as tk
from tkinter import messagebox
import os

# --- Game Data ---
colours = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Black', 'White']
score = 0
timeleft = 30


# --- Functions ---
def next_colour():
    """Go to the next colour and check the user's answer."""
    global score, timeleft

    if timeleft > 0:
        user_input = e.get().lower()
        correct_color = colours[1].lower()

        if user_input == correct_color:
            score += 1

        e.delete(0, tk.END)
        random.shuffle(colours)
        label.config(fg=colours[1], text=colours[0])
        score_label.config(text=f"Score: {score}")


def countdown():
    """Update the countdown timer."""
    global timeleft
    if timeleft > 0:
        timeleft -= 1
        time_label.config(text=f"Time left: {timeleft}")
        time_label.after(1000, countdown)
    else:
        scoreshow()


def record_highest_score():
    """Save the highest score to a file."""
    highest_score = load_highest_score()
    if score > highest_score:
        with open("highest_score.txt", "w") as file:
            file.write(str(score))


def load_highest_score():
    """Load the highest score from file."""
    try:
        with open("highest_score.txt", "r") as file:
            data = file.read()
            if data:
                return int(data)
            else:
                return 0
    except FileNotFoundError:
        return 0


def scoreshow():
    """Show the final and highest score."""
    record_highest_score()
    window2 = tk.Toplevel(window)
    window2.title("HIGH SCORE")
    window2.geometry("300x200")

    highest = load_highest_score()
    label2 = tk.Label(window2, text=f"Highest Score: {highest}", font=(font, 12))
    label2.pack(pady=40)

    tk.Button(window2, text="Close", command=window2.destroy).pack(pady=10)


def start_game(event):
    """Start the game when user presses Enter."""
    global timeleft
    if timeleft == 30:
        countdown()
    next_colour()


# --- Window Setup ---
window = tk.Tk()
font = 'Helvetica'
window.title("Color Game")
window.geometry("1000x1000")
window.resizable(False, False)

# Try to set the icon safely
icon_path = "color_game_icon.ico"
if os.path.exists(icon_path):
    try:
        window.iconbitmap(icon_path)
    except Exception:
        pass  # If loading fails, just skip
else:
    print("⚠️ Icon file not found, continuing without custom icon.")

# --- UI Elements ---
instructions = tk.Label(window, text="Enter the color of the text, not the word!", font=(font, 12))
instructions.pack(pady=10)

score_label = tk.Label(window, text="Press Enter to start", font=(font, 12))
score_label.pack()

time_label = tk.Label(window, text=f"Time left: {timeleft}", font=(font, 12))
time_label.pack()

label = tk.Label(window, font=(font, 60))
label.pack(pady=20)

e = tk.Entry(window)
e.pack()
e.focus_set()

# Bind Enter key
window.bind('<Return>', start_game)

window.mainloop()
