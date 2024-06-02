import tkinter as tk
import config
import logic
from tkinter import simpledialog

class NoteGUI():
    def __init__(self, window):
        self.window = window
        self.window.title('Notes')
        self.window.iconbitmap(config.ICON_PATH)
        self.window.geometry('1200x660')
        self.CreateMenu()
        self.CreateWidgets()
        self.CreateListItems()
        self.window.bind('<Control-s>', lambda event: logic.SaveTextEditorContent(self.text_editor, self.sidebar))

    def CreateMenu(self):
        self.menu = tk.Menu(self.window, tearoff=False, font=config.FONT_COURIER)
        self.window.config(menu=self.menu)
        
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=False, font=config.FONT_COURIER)
        self.menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label="New", command=self.createNewNoteWidget)
        file_menu.add_command(label="Save", command=lambda: logic.SaveTextEditorContent(self.text_editor, self.sidebar))
        file_menu.add_command(label="Change Notes Folder", command=self.ChangeNotesFolder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
    
    def CreateWidgets(self):
        # Middle frame
        self.middle_frame = tk.Frame(self.window, background='#999')
        
        # Middle frame layout
        self.middle_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # Sidebar frame
        self.sidebar_frame = tk.Frame(self.middle_frame, background='black')
        self.add_button = tk.Button(self.sidebar_frame, text='Add Note', font=config.FONT_HELVETICA, command=self.createNewNoteWidget)
        self.sidebar_scroll = tk.Scrollbar(self.sidebar_frame, highlightbackground=config.FOREGROUND_COLOR)
        self.sidebar = tk.Listbox(self.sidebar_frame, background='white', yscrollcommand=self.sidebar_scroll.set, font=('Arial', 15))
        
        # Sidebar layout
        self.add_button.pack(side=tk.TOP, fill=tk.X, ipady=5)
        self.sidebar_scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_scroll.config(command=self.sidebar.yview)
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.sidebar_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.sidebar.bind('<Button-3>', self.PopUpMenuFunction)
        self.ListBoxHighlightFunc()
        
        # Text editor frame
        self.text_editor_frame = tk.Frame(self.middle_frame)
        self.text_editor_scroll = tk.Scrollbar(self.text_editor_frame)
        self.text_editor = tk.Text(self.text_editor_frame, width=70, height=30, font=config.FONT_COURIER,
                                   bg=config.BACKGROUND_COLOR, fg=config.FOREGROUND_COLOR,
                                   selectbackground='black', selectforeground='green',
                                   undo=True, yscrollcommand=self.text_editor_scroll.set, insertbackground=config.FOREGROUND_COLOR)
        
        # Text editor layout
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=5, ipady=5)
        self.text_editor_scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.text_editor_scroll.config(command=self.text_editor.yview)
        self.text_editor_frame.pack(side=tk.LEFT)
    
        # Popup menu
        self.pop_up_menu = tk.Menu(self.window, tearoff=False)
        self.pop_up_menu.add_command(label='Rename')
        self.pop_up_menu.add_command(label='Delete', command=self.DeleteSelectedNote)
    
    def createNewNoteWidget(self):
        answer = simpledialog.askstring("New note", "Enter a name for your new note", parent=self.window)
        if answer:
            logic.CreateNewNote(answer)
            self.CreateListItems()
    
    def CreateListItems(self):
        self.sidebar.delete(0, tk.END)
        array_of_names = logic.GetArrayOfNoteNames()
        for item_name in array_of_names:
            self.sidebar.insert(tk.END, item_name)
        self.SelectFirstItem()
        
    def ListBoxHighlightFunc(self):
        self.sidebar.bind('<<ListboxSelect>>', self.OnListboxSelect)
    
    def OnListboxSelect(self, event):
        logic.ListBoxHighlightFunction(event, self.text_editor)
    
    def PopUpMenuFunction(self, event):
        pos = logic.SideBarPopUp(self.sidebar)
        if pos is not None:
            x, y = pos
            self.pop_up_menu.tk_popup(x, y)
    
    def SelectFirstItem(self):
        if self.sidebar.size() > 0:
            self.sidebar.select_set(0)  # Select the first item
            
    def ChangeNotesFolder(self):
        logic.ChangeNotesFolder()
        self.CreateListItems()
    
    def DeleteSelectedNote(self):
        selected_item = logic.GetSelectedNoteFromListbox(self.sidebar)
        if selected_item:
            logic.DeleteNote()
            self.CreateListItems()