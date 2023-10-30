import subprocess
import tkinter as tk
import time
import random
import threading

# Function to shuffle poker icons and colors
def shuffle_icons_and_colors():
    icons = ['♦', '♥', '♠', '♣']  # Poker icons for diamonds, hearts, spades, and clubs
    colors = ['red', 'red', 'grey', 'grey']  # Corresponding colors
    random_index = random.randint(0, len(icons) - 1)
    
    icon = icons[random_index]
    color = colors[random_index]
    
    return icon, color

# Function to slide icons across the screen one at a time
def slide_icon():
    slide_x = 0
    icon, color = shuffle_icons_and_colors()
    icon_label.config(text=icon, fg=color)
    
    for slide_x in range(screen_width):
        icon_label.place(x=slide_x)
        window.update()  # Update the window to see the changes
        time.sleep(.000005)
    # After sliding all icons, start closing the splash screen
    slide_icon()

# Animating Text to make it appear on screen
def animate_text_typing():
    current_text = ""
    for char in text:
        current_text += char
        text_label.config(text=current_text)
        window.update()
        time.sleep(0.02)

# Function to close the splash screen and Start main screen
def close_splash_screen():
    switch = subprocess.Popen(["python", "main.py"])
    switch.wait()
    window.destroy()


# Create the main window
window = tk.Tk()
#window.overrideredirect(True)

text = "We aim to provide players with an engaging and intellectually stimulating poker experience while also incorporating the values of compassion, integrity, and mindfulness that are central to Christian faith. Our goal is to create a space where players can not only enjoy the strategic elements of poker but also reflect on the importance of faith and morality, fostering a deeper connection between entertainment and spirituality."

# Calculate the size based on the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Create a dark green background frame
input_frame = tk.Frame(window, bg="black")  # Use the color #006400 for dark green
input_frame.pack_propagate(False)

# Create a frame to hold the icon labels
icon_frame = tk.Frame(input_frame, bg="black")

# Create the title label
text_label = tk.Label(input_frame, text=text, font=("Helvetica", 24), bg="black", fg="white",wraplength=800, justify="center")

# Load an image
church_image = tk.PhotoImage(file="assets/church1.png")
church_image = church_image.subsample(6)

# Create an image label
church_image_label = tk.Label(input_frame, image=church_image, bg="black")

# Create labels for displaying poker icons
icon_labels = [tk.Label( icon_frame, text="", font=("Helvetica", 36), bg="black", fg="white") for i in range(4)]
for icon_label in icon_labels:
    icon_label.pack(side="left", fill="both", expand=True)
    #icon_label.place(y=screen_height - 50)

input_frame.pack(fill = "both", expand=True)
text_label.pack(pady=50)
church_image_label.pack(side="right")
icon_frame.pack(side="bottom", fill="x", expand=True)

# After 5 seconds, close the splash screen
window.after(10000, close_splash_screen)

threading.Thread(target=animate_text_typing).start()
threading.Thread(target=slide_icon).start()

# Start the Tkinter main loop
window.mainloop()