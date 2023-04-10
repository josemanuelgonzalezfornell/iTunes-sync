from src.music_sync import *
import tkinter as gui
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from platform import system
from datetime import datetime
from functools import partial

# Window properties
APP = 'iTunes sync'
PANELS = {'source': 'Source', 'destination': 'Destination'}
MARGIN = 5
WIDTH = {
    'button': 8,
    'path': 32
}
HEIGHT = {
    'sync': 10,
    'path': 3,
    'content': 15
}
OS = system()
window = {}  # List of elements in the main window.


def run() -> None:
    """It shows the main window.
    """
    # Window configuration
    window['root'] = gui.Tk()
    window['root'].title(APP)
    if OS == 'Darwin':
        icon_extension = '.icns'
    elif OS == 'Windows':
        icon_extension = '.ico'
    else:
        icon_extension = '.xbm'
    window['root'].iconbitmap('media/logo' + icon_extension)
    window['root'].resizable(False, False)
    width = WIDTH['button'] + WIDTH['path']
    for panel in PANELS:
        window[panel] = {}
        # Frame
        window[panel]['frame'] = gui.Frame(window['root'],
                                           width=width,
                                           relief='groove',
                                           borderwidth=1
                                           )
        window[panel]['frame'].grid(column=2*int(panel == 'destination'),
                                    row=0,
                                    padx=MARGIN,
                                    pady=MARGIN
                                    )
        # Title
        window[panel]['title'] = gui.Label(window[panel]['frame'],
                                           width=width,
                                           text=PANELS[panel],
                                           font=('Arial Bold', 14)
                                           )
        window[panel]['title'].grid(column=0,
                                    row=0,
                                    padx=MARGIN,
                                    pady=MARGIN,
                                    columnspan=2
                                    )
        # File button
        window[panel]['file button'] = gui.Button(window[panel]['frame'],
                                                  width=WIDTH['button'],
                                                  height=HEIGHT['path']
                                                  )
        window[panel]['file button'].grid(column=0,
                                          row=1,
                                          padx=MARGIN,
                                          pady=MARGIN
                                          )
        if panel == 'source':
            window[panel]['file button']['text'] = 'Library'
            window[panel]['file button']['command'] = set_library
        elif panel == 'destination':
            window[panel]['file button']['text'] = 'Log file'
            window[panel]['file button']['command'] = set_log
        # File label
        window[panel]['file label'] = gui.Label(window[panel]['frame'],
                                                width=WIDTH['path'],
                                                height=HEIGHT['path'],
                                                wraplength=10 *
                                                WIDTH['path']-MARGIN,
                                                relief='ridge',
                                                borderwidth=1
                                                )
        window[panel]['file label'].grid(column=1,
                                         row=1,
                                         padx=MARGIN,
                                         pady=MARGIN,
                                         sticky='w'
                                         )
        # Folder button
        window[panel]['folder button'] = gui.Button(window[panel]['frame'], width=WIDTH['button'],
                                                    height=HEIGHT['path'],
                                                    text='Folder',
                                                    command=partial(
                                                        set_folder, panel)
                                                    )
        window[panel]['folder button'].grid(column=0,
                                            row=2,
                                            padx=MARGIN,
                                            pady=MARGIN
                                            )
        # Folder label
        window[panel]['folder label'] = gui.Label(window[panel]['frame'],
                                                  width=WIDTH['path'],
                                                  height=HEIGHT['path'],
                                                  wraplength=10 *
                                                  WIDTH['path']-MARGIN,
                                                  relief='ridge',
                                                  borderwidth=1
                                                  )
        window[panel]['folder label'].grid(column=1,
                                           row=2,
                                           padx=MARGIN,
                                           pady=MARGIN,
                                           sticky='w'
                                           )
        # Content
        window[panel]['content'] = gui.Label(window[panel]['frame'],
                                             width=width,
                                             height=HEIGHT['content']
                                             )
        window[panel]['content'].grid(column=0,
                                      row=3,
                                      padx=MARGIN,
                                      pady=MARGIN,
                                      columnspan=2,
                                      sticky='w'
                                      )
    # Sync button
    window['sync'] = gui.Button(window['root'],
                                width=WIDTH['button'],
                                height=HEIGHT['sync'],
                                text='→',
                                command=sync,
                                activebackground='blue'
                                )
    window['sync'].grid(column=1,
                        row=0,
                        padx=MARGIN,
                        pady=MARGIN
                        )
    # Progress
    window['progress'] = ttk.Progressbar(window['root'],
                                         orient='horizontal',
                                         mode='determinate',
                                         length=10 *
                                         (2*width + WIDTH['button'])
                                         )
    window['progress'].grid(column=0,
                            row=1,
                            padx=MARGIN,
                            pady=MARGIN,
                            columnspan=3
                            )
    # Show window
    update_state()
    window['root'].mainloop()


def update_state() -> None:
    """It updates the state of the window according to the available data. For example, it enables sync button if source and destination path folder is already indicated.
    """
    state = ['normal']
    # Sync button
    for panel in PANELS:
        if window[panel]['folder label']['text'] == '':
            state = ['disabled']
            break
    library_file_name = window['source']['file label']['text']
    if library_file_name == '':
        state = ['disabled']
    window['sync']['state'] = (state)
    # Library
    content = ''
    if library_file_name:
        global library
        library = Library(library_file_name)
        content += 'The selected music library contains:'
        content += '\n' + str(library.get_artists_number()) + ' artist(s)'
        content += '\n' + str(library.get_albums_number()) + ' album(s)'
        content += '\n' + str(len(library.songs)) + ' song(s)'
        content += '\n' + str(len(library.playlists)) + ' playlist(s)'
    window['source']['content']['text'] = content


def set_library(default: str = None) -> None:
    """It opens a dialog to select the library XML file in the file system.

    Args:
        default (str, optional): Default file path name.
    """
    file = filedialog.askopenfilename(parent=window['root'],
                                      initialdir=default,
                                      title='Select the iTunes music library XML file',
                                      filetypes=[("XML File", "*.xml")]
                                      )
    if file:
        window['source']['file label']['text'] = file
    update_state()


def set_log(default: str = None) -> None:
    """It opens a dialog to create the log file of the sync process.

    Args:
        default (str, optional): Default file path name.
    """
    file = filedialog.asksaveasfilename(parent=window['root'],
                                        initialdir=default,
                                        title='Create log file',
                                        defaultextension='.txt'
                                        )
    if file:
        window['destination']['file label']['text'] = file


def set_folder(panel: str, default: str = None) -> str:
    """It opens a dialog to select a folder in the file system.

    Args:
        panel (str): Panel name (origin or destination).
        default (str, optional): Default folder path name.

    Returns:
        str: Path name to the selected folder.
    """
    folder = filedialog.askdirectory(parent=window['root'],
                                     initialdir=default,
                                     title='Select ' +
                                     PANELS[panel] + ' folder'
                                     )
    if folder:
        window[panel]['folder label']['text'] = folder
    update_state()


def sync() -> None:
    """It starts the sync process.
    """
    print('Sync button clicked')
    window['sync']['state'] = 'disabled'
    library_path = window['source']['file label']['text']
    source_path = window['source']['folder label']['text']
    destination_path = window['destination']['folder label']['text']
    # Sync process
    process = Sync(library_path, source_path,  destination_path, window)
    process.start()
    # Log file
    if window['destination']['file label']['text']:
        log = open(window['destination']['file label']['text'], 'w')
        log.write('Sync process was completed at ' +
                  str(datetime.now()) + ' with the following errors:\n')
        for error in process.errors[:14]:
            if isinstance(error, Song):
                log.write('\n' + get_file_path(error))
            elif isinstance(error, Playlist):
                log.write('\nPlaylist: ' + error.name)
        log.close()
    # Result
    if len(process.errors) == 0:
        content = 'The music library has been successfully synced.'
    else:
        content = 'The music library has been synced with ' + \
            str(len(process.errors)) + ' error(s).'
    window['destination']['content']['text'] = content
    messagebox.showinfo(
        icon='info', title='Music library synced', message=content)
    # Sync button
    window['sync']['state'] = 'normal'


def confirm(action: str) -> bool:
    """It shows a dialog to confirm an user action.

    Args:
        action (str): Text of the action to be prompted.

    Returns:
        bool: User answer.
    """
    return messagebox.askyesno(icon='question', title='User confirmation', message='Are you sure you want to ' + action + '?')


if __name__ == "__main__":
    run()
