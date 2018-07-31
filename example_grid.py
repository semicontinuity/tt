from tt.picotui.grid import WGrid

from picotui.defs import *
from picotui.screen import Screen
from picotui.widgets import *


if __name__ == "__main__":
    s = Screen()
    try:
        s.init_tty()
        s.enable_mouse()
        s.cls()
        s.attr_reset()
        d = Dialog(5, 5, 50, 12)

        d.add(11, 1, WGrid(20, 10))


        b = WButton(8, "OK")
        d.add(10, 16, b)

        b.finish_dialog = ACTION_OK

        res = d.loop()
    finally:
        s.goto(0, 50)
        s.cursor(True)
        s.disable_mouse()
        s.deinit_tty()

    print("Result:", res)
