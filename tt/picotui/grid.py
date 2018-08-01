from picotui.basewidget import FocusableWidget, ACTION_CANCEL
from picotui.defs import *
from picotui.screen import Screen
from picotui.editor import Editor

P_FIRST = 0
P_NONE  = 1
P_STOP  = 2
P_LAST  = 3

KIND_SINGLE = 0
KIND_DOUBLE = 1

# for every sub-array: [vertical position * 4 + horizontal position]
# contains duplicates, but easily addressable
CHARS = [
    # vertical: single, horizontal: single
    [
        b'\xe2\x94\x8c', b'\xe2\x94\x80', b'\xe2\x94\xac', b'\xe2\x94\x90',
        b'\xe2\x94\x82', b' ',            b'\xe2\x94\x82', b'\xe2\x94\x82',
        b'\xe2\x94\x9c', b'\xe2\x94\x80', b'\xe2\x94\xbc', b'\xe2\x94\xa4',
        b'\xe2\x94\x94', b'\xe2\x94\x80', b'\xe2\x94\xb4', b'\xe2\x94\x98'
    ],
    # vertical: single, horizontal: double
    [
        b'\xe2\x95\x92', b'\xe2\x95\x90', b'\xe2\x95\xa4', b'\xe2\x95\x95',
        b'\xe2\x94\x82', b' ',            b'\xe2\x94\x82', b'\xe2\x94\x82',
        b'\xe2\x95\x9e', b'\xe2\x95\x90', b'\xe2\x95\xaa', b'\xe2\x95\xa1',
        b'\xe2\x95\x98', b'\xe2\x95\x90', b'\xe2\x95\xa7', b'\xe2\x95\x9b'
    ],
    # vertical: double, horizontal: single
    [
        b'\xe2\x95\x93', b'\xe2\x94\x80', b'\xe2\x95\xa5', b'\xe2\x95\xa6',
        b'\xe2\x95\x91', b' ',            b'\xe2\x95\x91', b'\xe2\x95\x91',
        b'\xe2\x95\x9f', b'\xe2\x94\x80', b'\xe2\x95\xab', b'\xe2\x95\xa2',
        b'\xe2\x95\x99', b'\xe2\x94\x80', b'\xe2\x95\xa8', b'\xe2\x95\x9c'
    ],
    # vertical: double, horizontal: double
    [
        b'\xe2\x95\x94', b'\xe2\x95\x90', b'\xe2\x95\xa6', b'\xe2\x95\x97',
        b'\xe2\x95\x91', b' ',            b'\xe2\x95\x91', b'\xe2\x95\x91',
        b'\xe2\x95\xa0', b'\xe2\x95\x90', b'\xe2\x95\xac', b'\xe2\x95\xa3',
        b'\xe2\x95\x9a', b'\xe2\x95\x90', b'\xe2\x95\xa9', b'\xe2\x95\x9d'
    ]
]


def draw_grid(left, top, w, h, top_kind, bottom_kind, left_kind, right_kind, h_stops, v_stops):
    def draw_line(v_pos, y, current_h_kind):
        Screen.goto(left, y)
        h_stop = 0

        border_chars = CHARS[current_h_kind]
        Screen.wr(CHARS[2 * left_kind + current_h_kind][4 * v_pos + P_FIRST])
        x = left + 1
        while True:
            next_h_stop = (w - 1, right_kind) if h_stop >= len(h_stops) else h_stops[h_stop]
            next_x = left + next_h_stop[0]
            Screen.wr(border_chars[4 * v_pos + P_NONE] * (next_x - x))
            x = next_x
            if h_stop >= len(h_stops):
                break
            else:
                next_h_stop_v_kind = next_h_stop[1]
                Screen.wr(CHARS[2 * next_h_stop_v_kind + current_h_kind][4 * v_pos + P_STOP])
                x = x + 1
                h_stop = h_stop + 1
        Screen.wr(CHARS[2 * right_kind + current_h_kind][4 * v_pos + P_LAST])

    draw_line(P_FIRST, top, top_kind)
    y = top + 1
    v_stop = 0
    while True:
        next_v_stop = (h - 1, bottom_kind) if v_stop >= len(v_stops) else v_stops[v_stop]
        next_y = top + next_v_stop[0]

        while y < next_y:
            draw_line(P_NONE, y, 0)
            y = y + 1

        if v_stop >= len(v_stops):
            break
        else:
            next_v_stop_h_kind = next_v_stop[1]
            draw_line(P_STOP, y, next_v_stop_h_kind)
            y = y + 1
            v_stop = v_stop + 1
    draw_line(P_LAST, top + h - 1, bottom_kind)


class WGrid(Editor):
    def __init__(self, width, height, column_names, column_widths):
        super().__init__(0, 0, width, height)
        self.column_names = column_names
        self.column_widths = column_widths
        self.column_positions = self.compute_column_positions_except_first()
        self.h_stops = [(x, KIND_SINGLE) for x in self.column_positions]
        self.column_widths[0] = self.column_positions[0] - 1 if len(self.column_names) > 1 else width - 2
        self.column_positions.insert(0, 1)

    def compute_column_positions_except_first(self):
        """
        The first column occupies the remaining size, its specified size is ignored
        """
        i = len(self.column_widths) - 1
        x = self.width - 1
        column_positions = []
        while i > 0:
            x = x - 1 - self.column_widths[i]
            column_positions.append(x)
            i -= 1
        column_positions.reverse()
        return column_positions

    def redraw(self):
        self.cursor(False)
        self.attr_color(C_B_CYAN, C_BLUE)
        draw_grid(
            self.x, self.y, self.width, self.height,
            KIND_DOUBLE, KIND_DOUBLE, KIND_DOUBLE, KIND_DOUBLE,
            self.h_stops, []
        )

        self.attr_color(C_B_YELLOW, C_BLUE)
        self.redraw_column_headers()
        self.redraw_content()

    def redraw_column_headers(self):
        i = 0
        while i < len(self.column_positions):
            column_width = self.column_widths[i]
            column_text = self.column_names[i]
            text_len = len(column_text)
            used_text_len = min(text_len, column_width)
            self.goto(self.x + self.column_positions[i] + (column_width - used_text_len) / 2, self.y + 1)
            self.wr_fixedw(column_text, used_text_len)
            i += 1

    def redraw_content(self):
        i = self.top_line
        r = self.y + 1
        for c in range(self.height - 2):
            self.goto(self.x + 1, r)
            if i >= self.total_lines:
                self.show_line(None, i)
            else:
                self.show_line(self.content[i], i)
            i += 1
            r += 1

    def show_line(self, l, i):
        is_highlighted = self.cur_line == i
        if is_highlighted:
            self.attr_color(C_BLACK, C_CYAN)
        else:
            self.attr_color(C_B_CYAN, C_BLUE)
        for c in range(len(self.column_names)):
            if c > 0:
                self.wr(b'\xe2\x94\x82')    # |
            if l:
                self.wr_fixedw(l[c], self.column_widths[c])
            else:
                self.wr(' ' * self.column_widths[c])

    def handle_mouse(self, x, y):
        pass

    def handle_key(self, key):
        if key == KEY_QUIT:
            return key
        elif key == KEY_ESC:
            return ACTION_CANCEL
        elif key == KEY_ENTER:
            self.signal("enter")

    def on_enter(self):
        pass
