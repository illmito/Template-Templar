import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import os
import pyautogui
import pyperclip
import subprocess
import webbrowser

# Reads all the text files that has been located in templates directory

## **************There needs to be a files in ONEDRIVE folder named "templates" in order for it to register.************


def read_text_files(directory):
    templates = {}
    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                key = os.path.splitext(filename)[0]
                with open(os.path.join(directory, filename), 'r') as file:
                    content = file.read()
                templates[key] = content
    else:
        print(f"Directory '{directory}' doesn't exist or is not accessible.")
    return templates

def load_templates(directory):
    templates = read_text_files(directory)
    return dict(sorted(templates.items(), reverse=False))

def display_selected_template(event=None):
    selected_template = selected_template_dropdown.get()
    selected_directory = directories[template_dropdown.get()]
    selected_templates = load_templates(selected_directory)
    template_text = selected_templates.get(selected_template, "No option selected.")
    
    text_display.config(state='normal')
    text_display.delete(1.0, tk.END)
    text_display.insert(tk.END, template_text)
    text_display.config(state='normal')

def display_template_directory(event=None):
    selected_directory = directories[template_dropdown.get()]
    selected_templates = load_templates(selected_directory)
    template_options = list(selected_templates.keys())
    selected_template_dropdown.config(values=template_options)
    selected_template_dropdown.current(0)  # Select the first template by default
    display_selected_template()  # Display the selected template after changing the directory

# Toggles between the templates/files in directory chosen.
def toggle_templates(event=None):
    display_template_directory()
    display_selected_template()

# Functions that handle the copy buttons functions bottom of GUI
def copy_to_clipboard():
    template_text = text_display.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(template_text)
    root.update()

    # This Function will launch Notepad and paste the text displayed from the file dropdown
def copy_to_clipboard_and_open_notepad():
    # Retrieve the text displayed in the GUI
    template_text = text_display.get(1.0, tk.END)
    # Copy the text to clipboard
    pyperclip.copy(template_text)
    # Launch Notepad
    subprocess.Popen(["notepad.exe"])
    # Wait for a moment to ensure Notepad has opened
    root.after(1000)
    # Simulate the keyboard shortcut for paste with timestamp added (Ctrl + V)
    pyautogui.hotkey('F5')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('ctrl', 'v')
    
#Exit button - will prompt a confirmation message        
def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()
#Displays Version info 
def version_app():
    version = "1.4.1"  # Change this to your application's version
    messagebox.showinfo("Version", f"This is version {version}")

# function that change dark/light mode
def toggle_theme_function():
    current_theme = root.style.theme_use()
    if current_theme == "darkly":
       root.style.theme_use("united")
    else:
        root.style.theme_use("darkly")


# # Menubar - Top left - (File, Edit)
# # create - add - edit - delete 
def menubar_functions():
   
    file_menu = tk.Menu(menubar, tearoff=0,)
    menubar.add_cascade(label="File", menu=file_menu,)
    file_menu.add_command(label="Version ", command=version_app,)
    file_menu.add_command(label="Exit", command=exit_app,)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=file_menu,)
    file_menu.add_command(label="Copy All", command=copy_to_clipboard,)
    file_menu.add_command(label="Copy to Notepad", command=copy_to_clipboard_and_open_notepad,)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Appearance", menu=file_menu,)
    file_menu.add_command(label="Dark/Light mode", command=toggle_theme_function) # TO BE DIRECTORY SELECTION FOR TEMPLATES


root = tb.Window(themename="cosmo")

root.title("Template: Terminal")
my_themes = root.style.theme_names()


# list of themes
# print(root.style.theme_use('flatly'))
# print(my_themes)

# toggle_theme = root.style.theme_use("darkly")



# Menu Bar creation and setting to root 
menubar = tk.Menu(root)


# Calls function, creating Menubar and items within.
menubar_functions()

# confirms path variable on windows machine - assigns the users onedrive
# # looks for the templates within OneDrive directory
one_drive_path = os.environ.get('OneDrive')
templates_path = os.path.join(one_drive_path, 'templates') if one_drive_path else None

# searches the path in template and creates paths from folders in directory
directories = {}
if templates_path and os.path.exists(templates_path) and os.path.isdir(templates_path):
    for folder_name in os.listdir(templates_path):
        folder_path = os.path.join(templates_path, folder_name)
        if os.path.isdir(folder_path):
            directories[folder_name] = folder_path


template_options = list(directories.keys())

# Frame Label
lf_directory = ttk.LabelFrame(root, text="Directory")
lf_directory.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="")

# Drop down selection/ populater
template_dropdown = ttk.Combobox(lf_directory, values=template_options, state="readonly", width=70)
template_dropdown.grid(row=0, column=0, columnspan=1, padx=10, pady=5, sticky="")
template_dropdown.current(0)
template_dropdown.bind("<<ComboboxSelected>>", toggle_templates)


# Second dropdown box settings.
lf_select = ttk.LabelFrame(root, text="Choice")
lf_select.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="")

selected_template_dropdown = ttk.Combobox(lf_select, state="readonly", width=70,)
selected_template_dropdown.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="")
selected_template_dropdown.bind("<<ComboboxSelected>>", display_selected_template,)


# Display text box 
text_font = font.Font(family="Consolas", size=12)
text_display = tk.Text(root, height=25, width=78, font=text_font )
text_display.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="")
text_display.config(state='normal')


# Scroll bar 
scrollbar = ttk.Scrollbar(root, command=text_display.yview,)
scrollbar.grid(row=2, column=3, sticky='ns')
text_display.config(yscrollcommand=scrollbar.set)

# Contains the COPY text option buttons in GUI
def copy_button_widgets():
    # Copy to clipboard button
    copy_button = tk.Button(root, text=" Copy to Clipboard ", command=copy_to_clipboard)
    copy_button.grid(row=3, column=0, columnspan=3, pady=5, padx=15)
    # buton line separator
    tb.Separator().grid(row=4, column=0, columnspan=3, pady=4, padx=20)
    # Copy and paste into NOTEPAD
    copy_and_open_notepad_button = tk.Button(root, text="  Open in Notepad  ", command=copy_to_clipboard_and_open_notepad)
    copy_and_open_notepad_button.grid(row=5, column=0, columnspan=3, pady=5, padx=10)

      

copy_button_widgets()

# Populate selected_template_dropdown with options on program startup
display_template_directory()



# # Logo top right placement
# logo_image = tk.PhotoImage(file="/ttkbootstrap/tt.png")  # Replace "logo.png" with the path to your image file
# # Create a Label widget to display the image
# logo_label = tk.Label(root, image=logo_image,)
# # Add the label to the root and place it at the top-right corner
# logo_label.grid(row=0, column=2, pady=5, padx=0, sticky="se")  # Adjust x, y, and padding as needed


# photo = tk.PhotoImage(file="/ttkbootstrap/tt.png")
# root.wm_iconphoto(False, photo)


# bottom_right = tk.Label(root, text="Template:")
# bottom_right.grid(row=4, column=1, padx=5, pady=5, sticky='')


root.config(menu=menubar, )
root.mainloop()

