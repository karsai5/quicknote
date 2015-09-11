#Notational Velocity CLI
This is a command line interface of the note taking application for OSX. Written in python it should work on most operating systems although I have only tested it in linux.

To start the application with python
```
$ python notational.py [notation directory]
```
If you keep your notes in a particular directory add that as an argument, otherwise it'll just start in your current working directory. 

You should be greeted with an interface like the following (if you're starting a new notes directory it won't have all my messy files).
![home view](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-171701_956x501_scrot.png?raw=true)
Start typing straight away and it'll start filtering the files that contain your search term either in the body or title of the file.
![searching](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-171909_956x501_scrot.png)
Use the arrow keys to highlight different files.
![highlighting](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-172822_956x501_scrot.png?raw=true)
Hitting enter will open up that note in your favourite editor.
![editing file](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-171931_956x501_scrot.png?raw=true)
Hitting enter when no file is selected
![no files](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-172011_956x501_scrot.png)
Will create a new file with the search term as its name and open it in your editor
![new edited file](https://github.com/karsai5/notational_curses/blob/master/2015-09-11-172021_956x501_scrot.png)
