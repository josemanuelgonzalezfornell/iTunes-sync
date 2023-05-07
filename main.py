from src.music_sync import *
import tkinter as gui
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from platform import system
from datetime import datetime
from functools import partial

# Window properties
APP = "iTunes sync"
PANELS = {"source": "Source", "destination": "Destination"}
MARGIN = 5
WIDTH = {"label": 10, "value": 32}
HEIGHT = {"sync": 10, "path": 3, "content": 15}
OS = system()
window = {}  # List of elements in the main window.


def run() -> None:
    """It shows the main window."""
    # Window configuration
    window["root"] = gui.Tk()
    window["root"].title(APP)
    if OS == "Darwin":
        icon_extension = ".icns"
    elif OS == "Windows":
        icon_extension = ".ico"
    else:
        icon_extension = ".xbm"
    window["root"].iconbitmap("media/logo" + icon_extension)
    window["root"].resizable(False, False)
    width = WIDTH["label"] + WIDTH["value"]
    for panel in PANELS:
        window[panel] = {}
        # Frame
        window[panel]["frame"] = gui.Frame(
            window["root"], width=width, relief="groove", borderwidth=1
        )
        window[panel]["frame"].grid(
            column=2 * int(panel == "destination"), row=0, padx=MARGIN, pady=MARGIN
        )
        # Title
        window[panel]["title"] = gui.Label(
            window[panel]["frame"],
            width=width,
            text=PANELS[panel],
            font=("Arial Bold", 14),
        )
        window[panel]["title"].grid(
            column=0, row=0, padx=MARGIN, pady=MARGIN, columnspan=2
        )
        # Language
        window[panel]["language label"] = gui.Label(
            window[panel]["frame"], width=WIDTH["label"], text="Language"
        )
        window[panel]["language label"].grid(
            column=0, row=1, padx=MARGIN, pady=MARGIN, sticky="w"
        )
        window[panel]["language value"] = ttk.Combobox(
            window[panel]["frame"], width=WIDTH["value"] - 3, values=LANGUAGES[panel]
        )
        window[panel]["language value"].current(0)
        window[panel]["language value"].bind("<<ComboboxSelected>>", update_state)
        window[panel]["language value"].grid(column=1, row=1, padx=MARGIN, pady=MARGIN)
        # Library
        window[panel]["library button"] = gui.Button(
            window[panel]["frame"], width=WIDTH["label"], height=HEIGHT["path"]
        )
        window[panel]["library button"].grid(column=0, row=2, padx=MARGIN, pady=MARGIN)
        if panel == "source":
            window[panel]["library button"]["text"] = "Library"
            window[panel]["library button"]["command"] = select_library
        elif panel == "destination":
            window[panel]["library button"]["text"] = "Log file"
            window[panel]["library button"]["command"] = create_log
        window[panel]["library label"] = gui.Label(
            window[panel]["frame"],
            width=WIDTH["value"],
            height=HEIGHT["path"],
            wraplength=10 * WIDTH["value"] - MARGIN,
            relief="ridge",
            borderwidth=1,
        )
        window[panel]["library label"].grid(
            column=1, row=2, padx=MARGIN, pady=MARGIN, sticky="w"
        )
        # Playlists
        window[panel]["playlists button"] = gui.Button(
            window[panel]["frame"],
            width=WIDTH["label"],
            height=HEIGHT["path"],
            text="Playlists",
            command=select_playlists,
        )
        if panel == "source":
            window[panel]["playlists button"]["command"] = select_playlists
        elif panel == "destination":
            window[panel]["playlists button"]["command"] = create_playlists
        window[panel]["playlists button"].grid(
            column=0, row=3, padx=MARGIN, pady=MARGIN
        )
        window[panel]["playlists label"] = gui.Label(
            window[panel]["frame"],
            width=WIDTH["value"],
            height=HEIGHT["path"],
            wraplength=10 * WIDTH["value"] - MARGIN,
            relief="ridge",
            borderwidth=1,
        )
        window[panel]["playlists label"].grid(
            column=1, row=3, padx=MARGIN, pady=MARGIN, sticky="w"
        )
        # Music folder
        window[panel]["folder button"] = gui.Button(
            window[panel]["frame"],
            width=WIDTH["label"],
            height=HEIGHT["path"],
            text="Music folder",
            command=partial(select_folder, panel),
        )
        window[panel]["folder button"].grid(column=0, row=4, padx=MARGIN, pady=MARGIN)
        window[panel]["folder label"] = gui.Label(
            window[panel]["frame"],
            width=WIDTH["value"],
            height=HEIGHT["path"],
            wraplength=10 * WIDTH["value"] - MARGIN,
            relief="ridge",
            borderwidth=1,
        )
        window[panel]["folder label"].grid(
            column=1, row=4, padx=MARGIN, pady=MARGIN, sticky="w"
        )
        # Content
        window[panel]["content"] = gui.Label(
            window[panel]["frame"], width=width, height=HEIGHT["content"]
        )
        window[panel]["content"].grid(
            column=0, row=5, padx=MARGIN, pady=MARGIN, columnspan=2, sticky="w"
        )
    # Sync button
    window["sync"] = gui.Button(
        window["root"],
        width=WIDTH["label"],
        height=HEIGHT["sync"],
        text="→",
        command=sync,
        activebackground="blue",
    )
    window["sync"].grid(column=1, row=0, padx=MARGIN, pady=MARGIN)
    # Progress
    window["progress"] = ttk.Progressbar(
        window["root"],
        orient="horizontal",
        mode="determinate",
        length=10 * (2 * width + WIDTH["label"]),
    )
    window["progress"].grid(column=0, row=1, padx=MARGIN, pady=MARGIN, columnspan=3)
    # Show window
    update_state()
    window["root"].mainloop()


def update_state(event=None) -> None:
    """It updates the state of the window according to the available data. For example, it enables sync button if source and destination path folder is already indicated.

    Args:
        event (Tkinter event, optional): Event object when called by the graphical user interface. Defaults to None.
    """
    state = ["normal"]
    # Labels
    for panel in PANELS:
        if (
            window[panel]["library label"]["text"] == ""
            or window[panel]["folder label"]["text"] == ""
        ):
            state = ["disabled"]
        if window[panel]["language value"].get() == "Rhythmbox":
            if window[panel]["playlists label"]["text"] == "":
                state = ["disabled"]
            window[panel]["playlists button"]["state"] = ["normal"]
        else:
            window[panel]["playlists button"]["state"] = ["disabled"]
    # Content
    content = ""
    source_folder = [window["source"]["library label"]["text"]]
    if window["source"]["language value"].get() == "Rhythmbox":
        source_folder.append(window["source"]["playlists label"]["text"])
    if not "" in source_folder:
        try:
            global library
            library = Library(source_folder, window["source"]["language value"].get())
            content += "The selected music library contains:"
            content += "\n" + str(library.get_artists_number()) + " artist(s)"
            content += "\n" + str(library.get_albums_number()) + " album(s)"
            content += "\n" + str(len(library.songs)) + " song(s)"
            content += "\n" + str(len(library.playlists)) + " playlist(s)"
            if len(library.songs) == 0:
                state = ["disabled"]
        except:
            content = "Music library not valid"
            print("The selected music library is not valid.")
            state = ["disabled"]
    window["source"]["content"]["text"] = content
    # Sync button
    window["sync"]["state"] = state


def select_library(default: str = None) -> None:
    """It opens a dialog to select the library XML file in the file system.

    Args:
        default (str, optional): Default file path name.
    """
    file = filedialog.askopenfilename(
        parent=window["root"],
        initialdir=default,
        title="Select the "
        + window["source"]["language value"].get()
        + " music library XML file",
        filetypes=[("XML File", "*.xml")],
    )
    if file:
        window["source"]["library label"]["text"] = file
    update_state()


def select_playlists(default: str = None) -> None:
    """It opens a dialog to select the playlists XML file in the file system.

    Args:
        default (str, optional): Defaults file path name.
    """
    file = filedialog.askopenfilename(
        parent=window["root"],
        initialdir=default,
        title="Select the "
        + window["source"]["language value"].get()
        + " playlists XML file",
        filetypes=[("XML File", "*.xml")],
    )
    if file:
        window["source"]["playlists label"]["text"] = file
    update_state()


def select_folder(
    panel: str,
    default: str = None,
) -> str:
    """It opens a dialog to select a folder in the file system.

    Args:
        panel (str): Panel name (origin or destination).
        default (str, optional): Default folder path name.

    Returns:
        str: Path name to the selected folder.
    """
    folder = filedialog.askdirectory(
        parent=window["root"],
        initialdir=default,
        title="Select the " + PANELS[panel] + " folder",
    )
    if folder:
        window[panel]["folder label"]["text"] = folder
    update_state()


def create_log(default: str = None) -> None:
    """It opens a dialog to create the log file of the sync process.

    Args:
        default (str, optional): Default file path name.
    """
    file = filedialog.asksaveasfilename(
        parent=window["root"],
        initialdir=default,
        initialfile="Music sync log",
        title="Create the log file",
        defaultextension=".txt",
    )
    if file:
        window["destination"]["library label"]["text"] = file
    update_state()


def create_playlists(default: str = None) -> None:
    """It opens a dialog to create the playlists XML file.

    Args:
        default (str, optional): Default file path name.
    """
    file = filedialog.asksaveasfilename(
        parent=window["root"],
        initialdir=default,
        initialfile="playlists",
        title="Create the "
        + window["source"]["language value"].get()
        + " playlists XML file",
        defaultextension=".xml",
    )
    if file:
        window["destination"]["playlists label"]["text"] = file
    update_state()


def sync() -> None:
    """It starts the sync process."""
    print("Sync button clicked")
    window["sync"]["state"] = "disabled"
    source_language = window["source"]["language value"].get()
    source_files = [window["source"]["library label"]["text"]]
    if source_language == "Rhythmbox":
        source_files.append(window["source"]["playlists label"]["text"])
    source_folder = window["source"]["folder label"]["text"]
    destination_language = window["destination"]["language value"].get()
    destination_folder = window["destination"]["folder label"]["text"]
    destination_playlists = None
    if destination_language == "Rhythmbox":
        destination_playlists = window["destination"]["playlists label"]["text"]
    # Sync process
    process = Sync(
        source_language,
        source_files,
        source_folder,
        destination_folder,
        destination_playlists=destination_playlists,
        window=window,
    )
    process.start()
    # Log file
    if window["destination"]["library label"]["text"]:
        log = open(window["destination"]["library label"]["text"], "w")
        log.write(
            "Sync process was completed at "
            + str(datetime.now())
            + " with the following errors:\n"
        )
        for error in process.errors:
            if isinstance(error, Song):
                log.write("\n" + get_file_path(error))
            elif isinstance(error, Playlist):
                log.write("\nPlaylist: " + error.name)
        log.close()
    # Result
    if len(process.errors) == 0:
        content = "The music library has been successfully synced."
    else:
        content = (
            "The music library has been synced with "
            + str(len(process.errors))
            + " error(s)."
        )
    window["destination"]["content"]["text"] = content
    messagebox.showinfo(icon="info", title="Music library synced", message=content)
    # Sync button
    window["sync"]["state"] = "normal"


def confirm(action: str) -> bool:
    """It shows a dialog to confirm an user action.

    Args:
        action (str): Text of the action to be prompted.

    Returns:
        bool: User answer.
    """
    return messagebox.askyesno(
        icon="question",
        title="User confirmation",
        message="Are you sure you want to " + action + "?",
    )


if __name__ == "__main__":
    run()
