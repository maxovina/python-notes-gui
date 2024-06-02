import tkinter as tk
import logic
import gui


def main():
    root = tk.Tk()
    logic.CheckForConfigFile()
    gui.NoteGUI(root)
    logic.OpenNotesFolder()
    root.mainloop()


main()
