from picotui.screen import Screen

from tt.picotui.grid import WGrid

if __name__ == "__main__":
    s = Screen()
    try:
        s.init_tty()
        s.cls()
        s.attr_reset()

        screen_size = Screen.screen_size()
        g = WGrid(screen_size[0], screen_size[1], ["id", "time"], [0, 10])
        g.set_lines([("hello", "world"), ("hello", "again and again")])

        res = g.loop()
    finally:
        s.goto(0, 50)
        s.cursor(True)
        s.deinit_tty()

    print("Result:", res)
