from songstransfer import *
from tkinter import *
from tkinter import filedialog, messagebox
from re import sub

# Songs sync


def obtainOriginalPathAndSync():
    librarylocation = filedialog.askopenfilename(
        title="Open file to export", initialdir="/Users/administrador/Documents/Proyectos programación/Python/iTunes-sync/Test", filetypes=((".xml", "*.xml"), ("All files", "*.*")))
    if librarylocation != "":
        library = sub("iTunes Music Library.xml", "Music", librarylocation)
        filefinalpath = filedialog.askdirectory(
            title="Choose final folder", initialdir="./")
        songsTransferer(librarylocation, filefinalpath, library)
        messagebox.showinfo("Songs synchronized",
                            "Songs synchronized correctly")

# Playlist sync


def playlistsSync():
    librarylocation = filedialog.askopenfilename(
        title="Open file to export", initialdir="/Users/administrador/Documents/Proyectos programación/Python/iTunes-sync/Test", filetypes=((".xml", "*.xml"), ("All files", "*.*")))
    if librarylocation != "":
        filefinalpath = filedialog.askdirectory(
            title="Choose final folder", initialdir="./")
        playlistTransferer(librarylocation, filefinalpath)
        messagebox.showinfo("Playlists synhronized",
                            "Playlists synchronized correctly")

# Close App


def CloseApp(root):
    confirmation = messagebox.askquestion(
        "Close", "Do you want to close the App?")
    if confirmation == "yes":
        root.destroy()


root = Tk()
root.resizable(False, False)
# Center the window on the screen when the program is initializated
root.eval("tk::PlaceWindow . center")
root.title("iTunes Sync")

# Menu and action buttons

menu = Frame(root)
menu.pack()

# Button which synchronizing songs files
syncfiles = Button(menu, text="Sync songs files", width=15,
                   command=lambda: obtainOriginalPathAndSync())
syncfiles.grid(column=0, row=2, pady=2)

# Button wich synchronizing playlists
syncplaylists = Button(menu, text="Sync playlists", width=15,
                       command=lambda: playlistsSync())
syncplaylists.grid(column=0, row=3, pady=2)

# Button wich close the App
close = Button(menu, text="Close", width=15, command=lambda: CloseApp(root))
close.grid(column=0, row=4, pady=2)

# Menubar of root
menubar = Menu(root)
root.config(menu=menubar, width=300, height=300)

# App Menu
appmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="iTunes Sync", menu=appmenu)
appmenu.add_command(label="Close", command=lambda: CloseApp(root))

# Action Menu
actionmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Action", menu=actionmenu)
actionmenu.add_command(
    label="Sync songs files", command=lambda: obtainOriginalPathAndSync())
actionmenu.add_command(
    label="Sync playlists", command=lambda: playlistTransferer())

mainloop()
