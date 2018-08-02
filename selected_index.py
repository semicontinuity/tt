import json
import sys

from picotui.defs import *
from picotui.screen import Screen

from tt.picotui.grid import WGrid, screen_alt, screen_regular, cursor_position_save, cursor_position_restore

# arguments:
# argument 1: header
# argument 2: grid data in json format [[c1, c2 .. cN], ... [c1, c2 .. cN]]
# argument 3: column titles in json format ['name1', 'name2', ...]
# argument 4: column widths in json format [w1, w2, ...]
# prints result to STDERR (cannot use STDOUT)
title = sys.argv[1]
data = json.loads(sys.argv[2])
column_titles = json.loads(sys.argv[3])
column_widths = json.loads(sys.argv[4])

if __name__ == "__main__":
    s = Screen()
    try:
        cursor_position_save()
        screen_alt()
        s.init_tty()

        s.cls()
        s.attr_reset()

        screen_size = Screen.screen_size()
        g = WGrid(title, screen_size[0], screen_size[1], column_titles, column_widths)
        g.set_lines(data)

        res = g.loop()
        sys.exit(g.cur_line if res == KEY_ENTER else 128)
    finally:
        s.attr_reset()
        s.cls()
        s.goto(0, 0)
        s.cursor(True)

        s.deinit_tty()
        screen_regular()
        cursor_position_restore()
