import config
import os
import tkinter as tk
from tkinter import filedialog

selected_item = None

def CheckForConfigFile():
    if os.path.exists(config.CONFIG_FILE_PATH):
        print(config.CONFIG_FILE_PATH)
        print('hello world')
    else:
        os.mkdir(config.CONFIG_FOLDER_PATH)
        with open(config.CONFIG_FILE_PATH, 'w') as file:
            pass
        print(config.CONFIG_FILE_PATH)
        print('goodbye world')

def CheckForPathInConfigFile():
    with open(config.CONFIG_FILE_PATH, 'r') as file:
        content = file.read()
        if not content:
            print(content)
            return False
        else:
            print(content)
            return True

def OpenNotesFolder():
    if CheckForPathInConfigFile():
        with open(config.CONFIG_FILE_PATH, 'r') as file:
            notes_folder_path = file.read()
    else:
        notes_folder_path = filedialog.askdirectory()
        with open(config.CONFIG_FILE_PATH, 'w') as file:
            file.write(notes_folder_path)
    os.chdir(notes_folder_path)

def GetNotesFolder():
    with open(config.CONFIG_FILE_PATH, 'r') as file:
        notes_folder_path = file.read()
    return notes_folder_path

def ChangeNotesFolder():
    notes_folder_path = filedialog.askdirectory()
    with open(config.CONFIG_FILE_PATH, 'w') as file:
        file.write(notes_folder_path)
    os.chdir(notes_folder_path)
    print(notes_folder_path)

def CreateNewNote(name):
    with open(f'{name}.txt', 'w') as file:
        pass

def GetArrayOfNoteNames():
    array_without_extension = []
    notes_folder_path = GetNotesFolder()
    array_with_extensions = os.listdir(notes_folder_path)
    for note_name in array_with_extensions:
        note_name = os.path.splitext(note_name)[0]
        array_without_extension.append(note_name)
    return array_without_extension

def ShowNoteNamesInListbox():
    note_names = GetArrayOfNoteNames()
    print(note_names)

def ListBoxHighlightFunction(event, text_editor):
    global selected_item
    item = GetSelectedNoteFromEvent(event)
    if item is not None:
        selected_item = item
        note_content = GetTextFileContent(selected_item)
        UpdateTextEditor(note_content, text_editor)

def GetSelectedNoteFromEvent(event):
    global selected_item
    listbox = event.widget
    index_of_highlighted = listbox.curselection()
    if index_of_highlighted:
        item = f"{listbox.get(index_of_highlighted)}.txt"
        selected_item = item
        return selected_item
    else:
        return None

def GetTextFileContent(item):
    notes_folder_path = GetNotesFolder()
    path = os.path.join(notes_folder_path, item)
    with open(path, 'r') as file:
        content = file.read()
        return content

def UpdateTextEditor(content, text_editor):
    text_editor.delete(1.0, tk.END)
    text_editor.insert(1.0, content)

def SaveTextEditorContent(text_editor, sidebar):
    global selected_item
    text_content = text_editor.get('1.0', tk.END)
    notes_folder = GetNotesFolder()
    note_file_path = os.path.join(notes_folder, selected_item)
    with open(note_file_path, 'w') as file:
        file.write(text_content)

def GetSelectedNoteFromListbox(listbox):
    global selected_item
    index_of_highlighted = listbox.curselection()
    if index_of_highlighted:
        item = f"{listbox.get(index_of_highlighted)}.txt"
        selected_item = item
        return selected_item
    else:
        return None

def SideBarPopUp(listbox):
    index_of_highlighted = listbox.curselection()
    if not index_of_highlighted:
        return None
    bbox = listbox.bbox(index_of_highlighted)
    if bbox:
        x, y, _, _ = bbox
        x += listbox.winfo_rootx()
        y += listbox.winfo_rooty()
        return (x+25, y+10)

def DeleteNote():
    global selected_item
    if selected_item:
        note_folder = GetNotesFolder()
        note_path = os.path.join(note_folder, selected_item)
        os.remove(note_path)
