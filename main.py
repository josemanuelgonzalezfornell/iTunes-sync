from src.music_library import *
from src.music_sync import *
import tkinter as gui

# Window properties
APP = 'iTunes sync'
WIDTH = 600
HEIGHT = 400
SIZE = [600, 400]
MARGIN = 10

# Window configuration
main = gui.Tk()
main.title(APP)
# main.iconbitmap('./media/app.ico')
# main.geometry(str(SIZE[0]) + 'x' + str(SIZE[1]) +
#               '+' + str(MARGIN) + '+' + str(MARGIN))
main.resizable(False, False)

# Window content
panels = {'source': 'Source', 'destination': 'Destination'}
for panel in panels:
    # Frame
    frame = gui.Frame(main)
    frame['width'] = (SIZE[0] - MARGIN) / 2
    frame['height'] = SIZE[1]
    frame['borderwidth'] = 1
    frame.grid(column=2*int(panel == 'destination'), row=0)
    # Title
    title = gui.Label(frame)
    title['text'] = panels[panel]
    title['font'] = ('Arial Bold', 14)
    title.grid(column=0, row=0)
    # Path button
    select = gui.Button(frame)
    select['text'] = 'Select'
    select.grid(column=0, row=1)
    # Path label
    path = gui.Label(frame)
    # TODO: complete
# Sync button
sync = gui.Button(main)
sync['text'] = 'Sync'
sync.grid(column=1, row=1)
# Show window
main.mainloop()
