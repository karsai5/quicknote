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
EDITOR = os.environ.get('EDITOR','vim') #that easy!
notationalDir = os.getcwd()

""" Setup cursors screen
Set up screen with no echo settings etc.
""" 
def setupScreen():
    global screen
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return reversed(list(sorted(os.listdir(path), key=mtime)))

""" Update keyword search
Read all the files in the notational folder and update the interal document list
to reflect their contents. Note: for lots of files this could cause a hang.
"""
def updateDocumentSet():
    global documentSet
    documentSet =  []
    for note in sorted_ls(notationalDir):
        if note != 'Notes & Settings' and note[0] != '.':
            filePath = notationalDir + '/' + note
            with open(filePath, 'r') as f:
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
        basename = os.path.splitext(ntpath.basename(document[0]))[0].lower()
        if any(term.lower() in s for s in document[1]) or term.lower() in basename:
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
            # only show file title
            modTime = time.ctime(os.path.getmtime(results[x]))
            basename = os.path.splitext(ntpath.basename(results[x]))[0] 
            space = w - len(modTime) - len(basename) -1
            lineItem = basename + ' ' * space + modTime
            if x == selectedItem:
                screen.addstr(lineItem + '\n', curses.A_STANDOUT)
            else:
                screen.addstr(lineItem + '\n')
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
        selectedFile = notationalDir + '/' + searchTerm + '.txt'
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
    # If argument given use that as notational directory, otherwise just use
    # current directory
    if len(sys.argv) > 1:
        print(sys.argv[1])
        if not os.path.isdir(expanduser(sys.argv[1])):
            print("That doesn't seem to be a directory...")
            print("python notational.py [notaional directory]")
            sys.exit(1)
        notationalDir = expanduser(sys.argv[1])


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
