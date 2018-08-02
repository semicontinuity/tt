import json
import sys

from picotui.defs import *
from picotui.screen import Screen

from tt.picotui.grid import WGrid, screen_alt, screen_regular, cursor_position_save, cursor_position_restore

# arguments:
# argument 1: number of column to print value from (1: first, 2: second, etc.) 0: print index
# argument 2: grid data in json format [[c1, c2 .. cN], ... [c1, c2 .. cN]]
# arguments 3+: column titles
# prints result to STDERR (cannot use STDOUT)
selector = int(sys.argv[1])
data = json.loads(sys.argv[2])
column_titles = sys.argv[3:]

if __name__ == "__main__":
    s = Screen()
    try:
        cursor_position_save()
        screen_alt()
        s.init_tty()

        s.cls()
        s.attr_reset()

        screen_size = Screen.screen_size()
        g = WGrid(screen_size[0], screen_size[1], column_titles, [0, 10])
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
