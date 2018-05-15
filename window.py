from contextlib import contextmanager
import curses

"""
configure and create curses window - the magic happens in game.py
"""
@contextmanager
def create_window(width, height):
     # intialize and draw window
     curses.initscr()
     window = curses.newwin(height,width, 1, 1)

     curses.noecho()
     curses.curs_set(False)
     window.scrollok(0)
     window.nodelay(True)
     window.keypad(True)

     yield window

     curses.endwin()
