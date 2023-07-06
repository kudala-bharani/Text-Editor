import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox

# Light and Dark theme colors
LIGHT_BACKGROUND_COLOR = "#FFFFFF"
LIGHT_TEXT_COLOR = "#000000"
DARK_BACKGROUND_COLOR = "#333333"
DARK_TEXT_COLOR = "#FFFFFF"

# Default font size
DEFAULT_FONT_SIZE = 12

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get('1.0', tk.END))

def clear_text():
    text.delete('1.0', tk.END)

def toggle_theme():
    global BACKGROUND_COLOR, TEXT_COLOR, CURSOR_COLOR

    if BACKGROUND_COLOR == LIGHT_BACKGROUND_COLOR:
        BACKGROUND_COLOR = DARK_BACKGROUND_COLOR
        TEXT_COLOR = DARK_TEXT_COLOR
        CURSOR_COLOR = "white"  # Set cursor color to white for dark theme
    else:
        BACKGROUND_COLOR = LIGHT_BACKGROUND_COLOR
        TEXT_COLOR = LIGHT_TEXT_COLOR
        CURSOR_COLOR = "black"  # Set cursor color to black for light theme

    # Update GUI elements with new theme colors
    root.config(bg=BACKGROUND_COLOR)
    text.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    text.config(insertbackground=CURSOR_COLOR)  # Update cursor color
    menu.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    file_menu.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    edit_menu.config(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

def undo(event=None):
    try:
        text.edit_undo()
    except tk.TclError:
        messagebox.showinfo("Information", "Nothing to undo.")

def redo(event=None):
    try:
        text.edit_redo()
    except tk.TclError:
        messagebox.showinfo("Information", "Nothing to redo.")

def zoom_in(event=None):
    global CURRENT_FONT_SIZE

    if CURRENT_FONT_SIZE < MAX_FONT_SIZE:
        CURRENT_FONT_SIZE += 1
        update_font_size()

def zoom_out(event=None):
    global CURRENT_FONT_SIZE

    if CURRENT_FONT_SIZE > MIN_FONT_SIZE:
        CURRENT_FONT_SIZE -= 1
        update_font_size()

def update_font_size():
    font_name = DEFAULT_FONT_FAMILY
    font_size = CURRENT_FONT_SIZE
    font_style = font.Font(font=text['font'])
    font_style.configure(size=font_size, family=font_name)
    text.tag_configure('font', font=font_style)
    text.tag_add('font', '1.0', 'end')

def configure_zoom(event=None):
    root.bind('<Control-plus>', zoom_in)
    root.bind('<Control-minus>', zoom_out)
    root.bind('<Control-KeyPress-equal>', zoom_in)
    root.bind('<Control-KeyPress-plus>', zoom_in)
    root.bind('<Control-KeyPress-minus>', zoom_out)
    root.bind('<Control-0>', reset_zoom)

def reset_zoom(event=None):
    global CURRENT_FONT_SIZE

    CURRENT_FONT_SIZE = DEFAULT_FONT_SIZE
    update_font_size()

def change_font(font_name):
    global DEFAULT_FONT_FAMILY

    DEFAULT_FONT_FAMILY = font_name
    update_font_size()

# Set initial theme to dark
BACKGROUND_COLOR = DARK_BACKGROUND_COLOR
TEXT_COLOR = DARK_TEXT_COLOR
CURSOR_COLOR = "white"  # Cursor color for dark theme

# Configure root window
root = tk.Tk()
root.title("Toggleable Text Editor")

# Configure text area
DEFAULT_FONT_FAMILY = font.nametofont("TkDefaultFont").actual()["family"]
CURRENT_FONT_SIZE = DEFAULT_FONT_SIZE
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 48

text = tk.Text(root, bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(DEFAULT_FONT_FAMILY, CURRENT_FONT_SIZE))
text.config(insertbackground=CURSOR_COLOR)  # Set cursor color
text.pack(expand=True, fill=tk.BOTH)

# Configure menu
menu = tk.Menu(root, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
root.config(menu=menu)

file_menu = tk.Menu(menu, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Clear", command=clear_text)
edit_menu.add_command(label="Toggle Theme", command=toggle_theme)

# Configure font options
font_menu = tk.Menu(edit_menu, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
edit_menu.add_cascade(label="Font", menu=font_menu)
available_fonts = font.families()
for font_name in available_fonts:
    font_menu.add_command(label=font_name, command=lambda f=font_name: change_font(f))

# Configure theme options
theme_menu = tk.Menu(edit_menu, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
edit_menu.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light", command=toggle_theme)
theme_menu.add_command(label="Dark", command=toggle_theme)

# Configure undo and redo bindings
root.bind_all('<Control-z>', undo)
root.bind_all('<Control-y>', redo)

# Configure zoom bindings
configure_zoom()

root.mainloop()
