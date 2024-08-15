from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
from skimage import morphology
from skimage.filters import median
from skimage.util import random_noise
import numpy as np
import math

main_window = Tk()
main_window.title("GUI Window")
main_window.geometry("1200x600")
main_window.configure(bg="Black")

frame1 = LabelFrame(main_window, width=400, height=600,background="#f5f5f5",relief="flat")
frame2 = LabelFrame(main_window, width=400, height=600,background="#f5f5f5",relief="flat")
frame3 = LabelFrame(main_window, width=400, height=600,background="#f5f5f5",relief="flat")

def light_theme():
    frame1.config(bg=current_theme["background"])
    frame2.config(bg=current_theme["background"])
    frame3.config(bg=current_theme["background"])
    for widget in frame1.winfo_children():
        widget.config(
            bg=current_theme["background"],
            fg=current_theme["foreground"],
            activebackground=current_theme["accent"],
            activeforeground=current_theme["foreground"]
        )
    for widget in frame2.winfo_children():
        widget.config(
            bg=current_theme["background"],
            fg=current_theme["foreground"],
            activebackground=current_theme["accent"],
            activeforeground=current_theme["foreground"]
        )
    for widget in frame3.winfo_children():
        widget.config(
            bg=current_theme["background"],
            fg=current_theme["foreground"],
            activebackground=current_theme["accent"],
            activeforeground=current_theme["foreground"]
        )
def dark_theme():
    frame1.config(bg=dark_theme["background"])
    frame2.config(bg=dark_theme["background"])
    frame3.config(bg=dark_theme["background"])
    for widget in frame1.winfo_children():
        widget.config(
            bg=dark_theme["background"],
            fg=dark_theme["foreground"],
            activebackground=dark_theme["accent"],
            activeforeground=dark_theme["foreground"]
        )
    for widget in frame2.winfo_children():
        widget.config(
            bg=dark_theme["background"],
            fg=dark_theme["foreground"],
            activebackground=dark_theme["accent"],
            activeforeground=dark_theme["foreground"]
        )
    for widget in frame3.winfo_children():
        widget.config(
            bg=dark_theme["background"],
            fg=dark_theme["foreground"],
            activebackground=dark_theme["accent"],
            activeforeground=dark_theme["foreground"]
        )

menubar = Menu(main_window)
main_window.config(menu=menubar)
# Main option with sub-options
option_menu = Menu(menubar, tearoff=0)
option_menu.add_command(label="Light Mode", command=light_theme)
option_menu.add_command(label="Dark Mode", command=dark_theme)
menubar.add_cascade(label="Window Theme", menu=option_menu)

# Color schemes (modify as desired)
light_theme = {
    "background": "#f0f0f0",  # Background (6 parts)
    "foreground": "#000000",  # Text (1 part)
    "accent": "#3399ff",      # Active elements/highlights (3 parts)
}
dark_theme = {
    "background": "#222222",  # Background (6 parts)
    "foreground": "#ffffff",  # Text (1 part)
    "accent": "#ccccff",      # Active elements/highlights (3 parts)
}
# Current theme (initially light)
current_theme = light_theme

# Global variables (avoid if possible, consider using classes)
image_path = None
noisy_image = None
noisy_image_data = None
denoised_image = None

def image_resize(image):
    original_width, original_height = image.size
    # Target dimensions for resized image
    target_width = 256
    target_height = 256
    # Calculate resize ratios to fit within target dimensions while maintaining aspect ratio
    width_ratio = target_width / original_width
    height_ratio = target_height / original_height
    # Use the maximum ratio to ensure the entire image is displayed 
    resize_ratio = max(width_ratio, height_ratio)
    # Resize the image while maintaining aspect ratio (might lead to some cropping)
    new_width = int(original_width * resize_ratio)
    new_height = int(original_height * resize_ratio)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return image

def load_image():
    global image_path, noisy_image, noisy_image_data
    image_path = filedialog.askopenfilename(title="Select Image")
    if image_path:
        try:
            noisy_image = Image.open(image_path)  # Load the image
            noisy_image_data = noisy_image.copy() # Create a copy for noise removal
            noisy_image = image_resize(noisy_image)

            noisy_image_tk = ImageTk.PhotoImage(noisy_image)
            image_label1.config(image=noisy_image_tk)
            image_label1.image = noisy_image_tk  # Keep reference

            view_frame2_button.config(state=NORMAL)
            print("Image label width:", image_label1.winfo_width())
            print("Image label height:", image_label1.winfo_height())
        except Exception as e:
            messagebox.showerror("Error", str(e))

def view_frame2():
    global noisy_image
    #Enable widgets within frame2 
    for widget in frame2.winfo_children():
        widget.config(state=NORMAL)
    # Update the image label with the resized image
    noisy_image_tk = ImageTk.PhotoImage(noisy_image)
    image_label2.config(image=noisy_image_tk)
    image_label2.image = noisy_image_tk

def add_noise():
    global image_path,noisy_image_data,noisy_image_tk,image_data

    if noisy_image_data is None:
        messagebox.showerror("Error", "Please load an image first!")
        return
    try:
        image_data = np.array(Image.open(image_path), dtype=np.uint8)
        # Add noise using skimage's random_noise
        noise_amount = noise_level_scale.get() / 100
        noisy_image_data = random_noise(image_data, mode='s&p', amount=noise_amount)
        noisy_image_data = (noisy_image_data * 255).astype(np.uint8)
        # Convert noisy NumPy array back to PIL Image for display
        noisy_image = Image.fromarray(noisy_image_data)
        noisy_image = image_resize(noisy_image)
        # Create PhotoImage for displaying the noisy image in Frame 2
        noisy_image_tk = ImageTk.PhotoImage(noisy_image)
        image_label2.config(image=noisy_image_tk)
        image_label2.image = noisy_image_tk  # Keep reference
    except Exception as e:
        messagebox.showerror("Error", "Noise addition failed: " + str(e))

def view_frame3():
    global noisy_image_tk
    #Enable widgets within frame3 
    title_label3.config(state=NORMAL)
    image_label3.config(state=NORMAL)
    remove_noise_button.config(state=NORMAL)
    view_metrics_button.config(state=NORMAL)
    Result_label.config(state=NORMAL)
    image_label3.config(image=noisy_image_tk)
    image_label3.image = noisy_image_tk
       
def remove_noise(window_size):
    global denoised_image
    window_size = int(window_size)
    method_choosen = selected_denoising_method.get()
    if method_choosen == "median_filter":
        median_filtered_image = median(noisy_image_data, selem=np.ones((window_size,window_size)))
        denoised_image = Image.fromarray(median_filtered_image)
        denoised_image = image_resize(denoised_image)
        denoised_image_tk = ImageTk.PhotoImage(denoised_image)
        image_label3.config(image=denoised_image_tk)
        image_label3.image = denoised_image_tk
    elif method_choosen == "opening":
        # Create structuring element (disk shape)
        se = morphology.disk(window_size // 2)
        # Perform opening (erosion followed by dilation)
        opened_image = morphology.opening(noisy_image_data, se)
        denoised_image = Image.fromarray(opened_image)
        denoised_image = image_resize(denoised_image)
        denoised_image_tk = ImageTk.PhotoImage(denoised_image)
        image_label3.config(image=denoised_image_tk)
        image_label3.image = denoised_image_tk
    elif method_choosen == "closing":
        # Create structuring element (disk shape)
        se = morphology.disk(window_size // 2)
        # Perform opening (erosion followed by dilation)
        closed_image = morphology.closing(noisy_image_data, se)
        denoised_image = Image.fromarray(closed_image)
        denoised_image = image_resize(denoised_image)
        denoised_image_tk = ImageTk.PhotoImage(denoised_image)
        image_label3.config(image=denoised_image_tk)
        image_label3.image = denoised_image_tk
    else:
        # Create structuring element (disk shape)
        se = morphology.disk(window_size // 2)
        # Perform opening (erosion followed by dilation)
        opened_image = morphology.opening(noisy_image_data, se)
        closed_image = morphology.closing(opened_image, se)
        denoised_image = Image.fromarray(closed_image)
        denoised_image = image_resize(denoised_image)
        denoised_image_tk = ImageTk.PhotoImage(denoised_image)
        image_label3.config(image=denoised_image_tk)
        image_label3.image = denoised_image_tk
    
def view_metrics():
    global noisy_image,denoised_image
    if (noisy_image.size) != (denoised_image.size):
        raise ValueError("Images must have the same shape.")
    noisy_image_data = np.array(noisy_image)
    denoised_image_data = np.array(denoised_image)
    # Calculate MSE
    squared_differences = np.square(noisy_image_data - denoised_image_data)
    # sum of squared differences
    sum_squared_differences = np.sum(squared_differences)
    # Get (m) (n)
    m , n = noisy_image.size
    # MSE
    mse = (1.0 / (m * n)) * sum_squared_differences
    # PSNR
    max_pixel_value = np.max(image_data)
    psnr = 10 * math.log10(max_pixel_value**2 / mse) 
    Result_label.configure(text="MSE is : " + str(mse)+"\nPSNR is : "+str(psnr))
    
  
# Frame 1 begin
title_label1 = Label(frame1, text="Load Image", font=("Monotype Corsiva", 20),padx=27,pady=15, background="snow")# Fixed-size title label
title_label1.pack(fill=X)

image_label1 = Label(frame1, text="Image will be loaded here:",padx=100, pady=100 , background="snow")# Image label with red background (resized image will be displayed here)
image_label1.pack(fill=X,pady=10)

load_button = Button(frame1, text="Load Image", command=load_image)# Load image button
load_button.pack(padx=10,pady=10)

view_frame2_button = Button(frame1, text="Add Noise", command=view_frame2, state=DISABLED)# "Add Noise" button (initially disabled)
view_frame2_button.pack(padx=10,pady=10)
# Frame 1 ends

# Frame 2 begins
title_label2 = Label(frame2, text="Add Noise",pady=15, font=("Monotype Corsiva", 20), background="snow",state=DISABLED)# Fixed-size title label
image_label2 = Label(frame2, text="Image will be loaded here:", padx=100, pady=100, background="snow",state=DISABLED)# Image label with red background (resized image will be displayed here)
noise_level_label = Label(frame2, text="Noise Level:",state=DISABLED)#slider label
noise_level_scale = Scale(frame2,orient=HORIZONTAL, from_=0, to=100, length=200,state=DISABLED)# Noise slider
noise_level_scale.set(20)  # Set initial noise level
add_noise_button = Button(frame2, text="Add Salt & Pepper Noise", command=add_noise, state=DISABLED)# button to Add noise
view_removenoise_button = Button(frame2, text="Remove Salt & Pepper Noise", command=view_frame3, state=DISABLED)# button to Add noise

title_label2.pack(fill=X)
image_label2.pack(fill=BOTH,pady=10)
noise_level_label.pack()
noise_level_scale.pack()
add_noise_button.pack(pady=15)
view_removenoise_button.pack(pady=15)
# Frame 2 ends

# Frame 3 begins
window_size_options = [3,5,7,9]
win_size = StringVar(main_window)
win_size.set(window_size_options[0])  # Set default window size
frame3_1 = LabelFrame(frame3, width=194, height=130,background="#f5f5f5",relief="flat")#internal frame for widget placing
frame3_2 = LabelFrame(frame3, width=194, height=130,background="#f5f5f5",relief="flat")#internal frame for widget placing
frame3_1.pack_propagate(False)
frame3_2.pack_propagate(False)

option_menu = OptionMenu(frame3_2, win_size, *window_size_options)
title_label3 = Label(frame3, text="Remove Noise", font=("Monotype Corsiva", 20),pady=15, background="snow",state=DISABLED)# Fixed-size title label
image_label3 = Label(frame3, text="Image will be loaded here:", padx=100, pady=100, background="snow",state=DISABLED)# Image label with red background (resized image will be displayed here)
selected_denoising_method = StringVar(value="median_filter")  # Default selection
median_filter_button = Radiobutton(frame3_1, text="Median Filtering", variable=selected_denoising_method, value="median_filter") # Radio buttons for different methods
opening_button = Radiobutton(frame3_1, text="Opening", variable=selected_denoising_method, value="opening") # Radio buttons for different methods
closing_button = Radiobutton(frame3_1, text="Closing", variable=selected_denoising_method, value="closing") # Radio buttons for different methods
opening_closing_button = Radiobutton(frame3_1, text="Opening & Closing", variable=selected_denoising_method, value="opening_closing") # Radio buttons for different methods
remove_noise_button = Button(frame3_2, text="Remove Noise", command=lambda: remove_noise(win_size.get()), state=DISABLED)
view_metrics_button = Button(frame3_2, text="View metrics", command=view_metrics, state=DISABLED)
Result_label = Label(frame3, text="Image metrics here:" ,background="snow", state=DISABLED)# Fixed-size title label

image_label3.pack_propagate(False)
Result_label.pack_propagate(False)

title_label3.pack(fill=X)
image_label3.pack(fill=BOTH,pady=10)
median_filter_button.pack(anchor=W) 
opening_button.pack(anchor=W)
closing_button.pack(anchor=W)
opening_closing_button.pack(anchor=W)
option_menu.pack(padx=10)
option_menu.config(font=("Harlow Solid", 12,"italic"))
remove_noise_button.pack(pady=10)
view_metrics_button.pack(pady=5)
Result_label.place(x=0,y=520,width=400,height=100)
frame3_1.pack(side=LEFT,padx=5)
frame3_2.pack(side=LEFT,padx=5)
# Frame 3 ends

frame1.place(x=0,y=0,width=400,height=600)
frame2.place(x=400,y=0,width=400,height=600)
frame3.place(x=800,y=0,width=400,height=600)

main_window.mainloop()