import os

ICON_PATH = "C:/Users/maxov/Desktop/projects/tkinter notes/icon/icon.ico"
BACKGROUND_COLOR = "#000000"  # Black background
FOREGROUND_COLOR = "#00FF00"  # Green background
FONT_HELVETICA = ("Helvetica", 16)
FONT_COURIER = ("Courier", 16)  # Monospaced font
CONFIG_FOLDER_PATH = os.path.join(os.getenv("APPDATA"), "maxovina_notes")
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, "config.txt")
