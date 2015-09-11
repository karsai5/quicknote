from os.path import expanduser
from subprocess import call
import curses
import ntpath
import os
import re
import subprocess
import sys
import time

searchTerm = ""
selectedItem = -1
documentSet = []
results = []
notationalDir = expanduser("~/Dropbox/Documents/Notational/")
EDITOR = os.environ.get('EDITOR','vim') #that easy!

""" Setup cursors screen
Set up screen with no echo settings etc.
""" 
def setupScreen():
    global screen
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)

""" Update keyword search
Read all the files in the notational folder and update the interal document list
to reflect their contents. Note: for lots of files this could cause a hang.
"""
def updateDocumentSet():
    global documentSet
    documentSet =  []
    for note in os.listdir(notationalDir):
        if note != 'Notes & Settings' and note[0] != '.':
            filePath = notationalDir + note
            with open(notationalDir + note, 'r') as f:
                words = []
                for line in f:
                    line = re.sub(r'[^a-zA-Z0-9]',' ', line) # remove non-alphanumeric
                    line = line.lower() # make all lowercase
                    for word in line.split():
                        words.append(word)
                documentSet.append((filePath, set(words)))

""" Search for a term in files
Using the internally generated document set, search for any files that contain
the term, or have the term in the header. Returns the files as a list of paths.
"""
def findFiles(term):
    files = []
    for document in documentSet:
        # print(document[1])
        if any(term.lower() in s for s in document[1]) or term.lower() in document[0].lower():
            files.append(document[0])
    return files

""" Main page drawing function
Clears the screen and updates it with the current search term at the top
as well as a list of notes that contain the searched term. It also highlights
the currently selected file for editing.
"""
def drawPage():
    global selectedItem
    global results

    h,w = screen.getmaxyx()
    screen.clear()

    screen.addstr("Search Term: %s\n" % searchTerm, curses.A_REVERSE)
    results = findFiles(searchTerm)

    maxh = len(results) if len(results) < h else h-1
    if selectedItem > maxh: 
        selectedItem = maxh-1

    elif selectedItem < -1:
        selectedItem = -1

    for x in range(maxh):
        try:
            basename = os.path.splitext(ntpath.basename(results[x]))[0]
            if x == selectedItem:
                screen.addstr(basename + '\n', curses.A_STANDOUT)
            else:
                screen.addstr(basename + '\n')
        except curses.error:
            pass

""" Note editing function
If a file is selected it will open it in your favourite editor, otherwise it'll
create a new file with the searchterm as its name and open that.
"""
def editPage():
    global results
    global selectedFile
    curses.endwin() # close curses app
    if selectedItem < 0: # if new file
        selectedFile = notationalDir + searchTerm + '.txt'
        if not os.path.isfile(selectedFile):
            open (selectedFile, 'a').close()
    else: #otherwise use selected file
        selectedFile = results[selectedItem]

    with open(selectedFile, 'r+') as tempfile:
      tempfile.flush()
      call([EDITOR, tempfile.name])
      # do the parsing with `tempfile`
    setupScreen()
    updateDocumentSet()
    drawPage()

if __name__ == "__main__":
    # Initial page draw
    setupScreen()
    updateDocumentSet()
    drawPage()

    while True: 
        event = screen.getch() 
        if event == 27:
            screen.nodelay(True)
            n = screen.getch()
            if n == -1:
                print("hit escape")
                break
            screen.nodelay(False)
        elif event == curses.KEY_BACKSPACE:
            searchTerm = searchTerm[:-1]
            drawPage()
        elif event == curses.KEY_UP:
            selectedItem = selectedItem - 1
            drawPage()
        elif event == curses.KEY_DOWN:
            selectedItem = selectedItem + 1
            drawPage()
        elif event == 10:
            editPage()
            drawPage()
        else:
            searchTerm = searchTerm + str(chr(event))
            drawPage()

    curses.endwin()
