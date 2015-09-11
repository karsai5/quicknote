import curses
import subprocess
import re
import ntpath
from os.path import expanduser
import sys, tempfile, os
from subprocess import call

searchTerm = ""
selectedItem = -1
documentSet = []
results = []
notationalDir = expanduser("~/Dropbox/Documents/Notational/")
EDITOR = os.environ.get('EDITOR','vim') #that easy!

def setupScreen():
    global screen
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)


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

def findFiles(term):
    files = []
    for document in documentSet:
        # print(document[1])
        if any(term.lower() in s for s in document[1]) or term.lower() in document[0].lower():
            files.append(document[0])
    return files

def drawPage():
    global selectedItem
    global results
    screen.clear()
    screen.addstr("Search Term: %s\n" % searchTerm, curses.A_REVERSE)
    results = findFiles(searchTerm)
    if selectedItem > len(results): 
        selectedItem = len(results)-1
    elif selectedItem < -1:
        selectedItem = -1
    for x in range(len(results)):
        try:
            basename = os.path.splitext(ntpath.basename(results[x]))[0]
            if x == selectedItem:
                screen.addstr(basename + '\n', curses.A_STANDOUT)
            else:
                screen.addstr(basename + '\n')
        except curses.error:
            pass

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
