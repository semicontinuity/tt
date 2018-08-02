import sys
from picotui.screen import Screen
from picotui.defs import *
from tt.picotui.grid import WGrid, screen_alt, screen_regular, cursor_position_save, cursor_position_restore

if __name__ == "__main__":
    s = Screen()
    try:
        cursor_position_save()
        screen_alt()
        s.init_tty()

        s.cls()
        s.attr_reset()

        screen_size = Screen.screen_size()
        g = WGrid(screen_size[0], screen_size[1], ["id", "time"], [0, 10])
        g.set_lines([
            ("Line 0", "lorem ipsum"),
            ("Line 1", "dolor"),
            ("Line 2", "sit"),
            ("Line 3", "amet"),
            ("Line 4", "consectetur")
        ])

        res = g.loop()
        sys.exit(g.cur_line if res == KEY_ENTER else 63)
    finally:
        s.attr_reset()
        s.cls()
        s.goto(0, 0)
        s.cursor(True)

        s.deinit_tty()
        screen_regular()
        cursor_position_restore()
