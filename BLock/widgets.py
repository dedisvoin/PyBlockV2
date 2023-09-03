from library.liball import *
from settings import TEXT_BOX_COLOR, DX_VAL


class TextBox:
    def __init__(self, block_, dx_=1, width_=5) -> None:
        self.__block = block_
        self.win: Window = block_.win
        self.text_value = ""
        self.__dx = dx_
        self.__dy = width_

        self.pos = [0, 0]
        self.DX_VAL = DX_VAL * 1.2
        self.size = [0, self.DX_VAL]

        self.text_ = Text("arial", int(self.DX_VAL), bold=0)

    def update_pos_and_size(self):
        self.pos[0] = self.__block.pos[0] + self.__dy
        self.pos[1] = (
            self.__block.pos[1]
            + self.__block.HEADER_SIZE
            + self.__dx * DX_VAL
            - self.DX_VAL / 2
        )

        self.size[0] = self.__block.size[0] - self.__dy * 2
        # if self.text_value != "None":
        #    self.__block.size[0] = self.size[0]

    def render(self):
        self._surf = pygame.Surface([self.size[0], self.size[1]]).convert_alpha()
        # self._surf.set_colorkey((0, 0, 0))
        self._surf.fill(TEXT_BOX_COLOR.rgb)
        self.size[0] = self._surf.get_width()
        self.text_surf_size = self.text_.draw(
            self._surf,
            [5, 0],
            text=str(self.text_value),
            color="white",
        )
        self.win().blit(self._surf, self.pos)


class InputBox:
    def __init__(self, block_, dx_=1, width_=5) -> None:
        self.win = block_.win
        self.__text_box = TextBox(block_, dx_, width_)
        self.input_text = ""
        self.vabor = False
        self.pressed = False
        self.timer = 0
        self.blink_render = False
        self.end_press_key = None

    def update_pos_and_size(self):
        self.timer += 1
        self.__text_box.update_pos_and_size()
        self.__text_box.text_value = self.input_text

        if Mouse.press() and not self.pressed:
            if in_rect(self.__text_box.pos, self.__text_box.size, Mouse.position()):
                self.pressed = True
                self.vabor = not self.vabor
            else:
                self.vabor = False

        if not Mouse.press():
            self.pressed = False

        if self.vabor:
            if self.win.press_key is not None:
                key = pygame.key.name(self.win.press_key)
                if self.end_press_key == "left shift" and key == "8":
                    key = "*"
                if self.end_press_key == "left shift" and key == "=":
                    key = "+"
                if self.end_press_key == "left shift" and key == "9":
                    key = "("
                if self.end_press_key == "left shift" and key == "0":
                    key = ")"
                if key == "backspace":
                    self.input_text = self.input_text[:-1]
                elif key == "space":
                    self.input_text += " "

                else:
                    if key != "left shift":
                        self.input_text += key

                self.end_press_key = key

        if self.timer % 80 == 0:
            self.blink_render = not self.blink_render

    def render(self):
        self.__text_box.render()

        if self.vabor:
            Draw.draw_hline(
                self.win(),
                self.__text_box.pos[1] + self.__text_box.size[1],
                self.__text_box.pos[0],
                self.__text_box.pos[0] + self.__text_box.size[0],
                2,
                (80, 240, 100),
            )
            if self.blink_render:
                Draw.draw_vline(
                    self.win(),
                    self.__text_box.pos[0] + self.__text_box.text_surf_size[0] + 5,
                    self.__text_box.pos[1],
                    self.__text_box.pos[1] + self.__text_box.size[1],
                    2,
                    (255, 255, 255),
                )


class DropDown:
    def __init__(self, block_, dx_=1, width_=5, values=[], start_value=0) -> None:
        self.win: Window = block_.win
        self.__block = block_
        self.__dx = dx_
        self.__dy = width_
        self.pos = [0, 0]
        self.DX_VAL = DX_VAL * 1.3
        self.size = [0, self.DX_VAL]

        self.values = values
        self.vabor_value = start_value
        self.opened = False
        self.pressed = False

        self.texts = []
        for value in values:
            t = Text("arial", int(self.DX_VAL), str(value), "white", True)
            self.texts.append(t.render(str(value))._surface)

    def update_pos_and_size(self):
        self.pos[0] = self.__block.pos[0] + self.__dy
        self.pos[1] = (
            self.__block.pos[1]
            + self.__block.HEADER_SIZE
            + self.__dx * DX_VAL
            - self.DX_VAL / 2
        )

        self.size[0] = self.__block.size[0] - self.__dy * 2

        if Mouse.press() and not self.pressed:
            if in_rect(self.pos, self.size, Mouse.position()):
                self.pressed = True
                self.opened = not self.opened

        if not Mouse.press():
            self.pressed = False

        if Mouse.press():
            self.pressed = True

    def render(self):
        Draw.draw_rect(self.win(), self.pos, self.size, TEXT_BOX_COLOR.rgb)
        vabor_surf = self.texts[self.vabor_value]

        self.win().blit(
            vabor_surf,
            [
                self.pos[0] + self.size[0] / 2 - vabor_surf.get_width() / 2,
                self.pos[1] + self.size[1] / 2 - vabor_surf.get_height() / 2,
            ],
        )
        if self.opened:
            Draw.draw_rect_fast(self.win(), self.pos, self.size, (0, 255, 0))
            for i in range(len(self.texts)):
                pos = [self.pos[0], self.pos[1] + self.size[1] + self.size[1] * i]
                Draw.draw_rect(
                    self.win(),
                    pos,
                    self.size,
                    TEXT_BOX_COLOR.rgb,
                )
                surf = self.texts[i]
                Draw.draw_hline(
                    self.win(),
                    pos[1] - 1,
                    pos[0],
                    pos[0] + self.size[0],
                    1,
                    (200, 200, 200),
                )
                self.win().blit(
                    surf,
                    [
                        pos[0] + self.size[0] / 2 - surf.get_width() / 2,
                        pos[1] + self.size[1] / 2 - surf.get_height() / 2,
                    ],
                )
                if i == self.vabor_value:
                    Draw.draw_circle(
                        self.win(), [pos[0] + 10, pos[1] + self.size[1] / 2], 2, "green"
                    )
                if Rect(pos, self.size).collide_point(Mouse.position()):
                    if Mouse.press():
                        self.vabor_value = i
                        self.opened = False


class Slider:
    def __init__(self, block_, dx_=1, width_=5, max_=100, min_=0, size=20) -> None:
        self.win: Window = block_.win
        self.__block = block_
        self.__dx = dx_
        self.__dy = width_
        self.pos = [0, 0]
        self.size = [0, size]
        self.DX_VAL = DX_VAL * 1.3
        self.max = max_
        self.min = min_

        self.value = 0
        self.togle_pos = [0, 0]
        self.pressed = False

    def update_pos_and_size(self, ws=0, zws=0):
        self.pos[0] = self.__block.pos[0] + self.__dy + ws
        self.pos[1] = (
            self.__block.pos[1]
            + self.__block.HEADER_SIZE
            + self.__dx * DX_VAL
            - self.DX_VAL / 2
        )

        self.size[0] = (self.__block.size[0] - self.__dy * 2) - ws - zws

        if Mouse.press(Mouse.left):
            if in_rect(self.pos, self.size, Mouse.position()):
                self.pressed = True
        if not Mouse.press(Mouse.left):
            self.pressed = False

        if self.pressed:
            self.togle_pos[0] = Mouse.position()[0]

        self.togle_pos[0] += self.__block.speed[0]

        self.togle_pos[1] = self.pos[1]
        self.togle_pos[0] = max(
            min(self.pos[0] + self.size[0], self.togle_pos[0]), self.pos[0]
        )

        max_lenght = self.size[0]
        lenght = self.togle_pos[0] - self.pos[0]
        d = (self.max - self.min) / max_lenght
        self.value = int(lenght * d) + self.min

    def render(self):
        Draw.draw_rect(self.win(), self.pos, self.size, (120, 120, 120))
        x = max(min(self.pos[0] + self.size[0], self.togle_pos[0] - 10), self.pos[0])
        Draw.draw_rect(
            self.win(), [x, self.togle_pos[1]], [10, self.size[1]], (170, 170, 170)
        )
