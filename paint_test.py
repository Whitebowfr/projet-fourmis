import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import os


# Define the function to upload and save the image
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)
        """image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection"""
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        messagebox.showinfo("Success", "Image uploaded successfully!")


def save_image(file_path):
    save_dir = "saved_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = os.path.basename(file_path)
    shutil.copy(file_path, os.path.join(save_dir, filename))
    print("Image saved to:", os.path.join(save_dir, filename))


# Create the main window
root = tk.Tk()
root.title("Image Uploader")

# Set window size
root.geometry("500x500")

# Create and pack widgets
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

"""image_label = tk.Label(root)
image_label.pack()"""

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Run the application
root.mainloop()