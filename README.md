# QuickNote

This is a command line note taking application based on [Notational Velocity](http://notational.net/) for OSX. Written in python it should work on most operating systems although I have only tested it in linux/osx.

## Installation
```
pip install quicknote
```

## Usage

To start the application with python
```
$ qn [notation directory]
```
If you keep your notes in a particular directory add that as an argument, otherwise it'll just start in your current working directory. 

You should be greeted with an interface like below (if you're starting a new notes directory it will be empty).
Start typing straight away and it'll start filtering the files that contain your search term either in the body or title of the file.
Use the arrow keys to highlight different files.
Hitting enter will open up that note in your favourite editor.
Hitting enter when no file is selected will create a new file with the search term as its name and open it in your editor

![new edited file](https://github.com/karsai5/notational_curses/raw/images/notational-example.gif)
