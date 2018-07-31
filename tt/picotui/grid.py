from picotui.basewidget import Widget
from picotui.screen import Screen

P_FIRST = 0
P_NONE  = 1
P_STOP  = 2
P_LAST  = 3

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


def draw_box(left, top, w, h, top_kind, bottom_kind, left_kind, right_kind, h_stops, v_stops):

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




class WGrid(Widget):

    def __init__(self, w, h):
        self.w = w
        self.h = h

    def redraw(self):
        draw_box(self.x, self.y, self.w, self.h, 1, 0, 1, 0, [(10, 1), (15, 0)], [(3,1), (5,0)])
