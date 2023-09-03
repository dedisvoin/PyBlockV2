from library.liball import *

from settings import UP_INTERFACE_COLOR

from library.liball import *
from settings import TEXT_BOX_COLOR, DX_VAL
from os import listdir


class TextBox:
    def __init__(self, win, pos, size) -> None:
        self.win: Window = win
        self.text_value = ""
        self.size = size

        self.pos = pos
        self.DX_VAL = DX_VAL * 1.2

        self.text_ = Text("arial", int(self.DX_VAL), bold=0)

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
    def __init__(self, win, pos, size) -> None:
        self.win = win
        self.text_box = TextBox(win, pos, size)
        self.input_text = ""
        self.vabor = False
        self.pressed = False
        self.timer = 0
        self.blink_render = False
        self.end_press_key = None

    def update_pos_and_size(self):
        self.timer += 1
        self.text_box.text_value = self.input_text

        if Mouse.press() and not self.pressed:
            if in_rect(self.text_box.pos, self.text_box.size, Mouse.position()):
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
        self.text_box.render()

        if self.vabor:
            Draw.draw_hline(
                self.win(),
                self.text_box.pos[1] + self.text_box.size[1],
                self.text_box.pos[0],
                self.text_box.pos[0] + self.text_box.size[0],
                2,
                (80, 240, 100),
            )
            if self.blink_render:
                Draw.draw_vline(
                    self.win(),
                    self.text_box.pos[0] + self.text_box.text_surf_size[0] + 5,
                    self.text_box.pos[1],
                    self.text_box.pos[1] + self.text_box.size[1],
                    2,
                    (255, 255, 255),
                )


class TextButton:
    def __init__(self, pos, size, text, text_size, surf) -> None:
        self.pos = pos
        self.size = size
        self.text = text
        self.text_size = text_size
        self.surf = surf
        self.press = False

        self.text_surf = Text("arial", text_size, text, bold=True)

    def render(self):
        self.press = False
        Draw.draw_rect_fast(self.surf(), self.pos, self.size, (160, 160, 160))

        if in_rect(self.pos, self.size, Mouse.position()):
            Draw.draw_rect(self.surf(), self.pos, self.size, (150, 150, 150))
            if Mouse.press():
                self.press = True

        self.text_surf.draw(
            self.surf(),
            center_rect(self.pos, self.size),
            True,
            text=self.text,
            color=(220, 220, 220),
        )


class SaveWindow:
    def __init__(self, win, size) -> None:
        self.size = size
        self.pos = [0, 0]
        self.win = win
        self.input_box = InputBox(win, [self.pos[0], self.pos[1]], [150, 20])
        self.view = False
        self.save_text = Text("arial", 18, "Save scratch", (200, 200, 200), True)
        self.save_bt = TextButton(self.pos, [50, 20], "save", 18, win)
        self.error = False

    def render(self):
        if self.view:
            Draw.draw_rect(self.win(), self.pos, self.size, (120, 120, 120))
            close_rect = [self.pos[0] + self.size[0] - 20, self.pos[1]]
            Draw.draw_rect(self.win(), self.pos, [self.size[0], 20], (170, 170, 170))
            Draw.draw_rect(self.win(), close_rect, [20], (200, 100, 100))
            self.save_text.draw(
                self.win(),
                [self.pos[0] + 7, self.pos[1]],
                text="Save scratch",
                color=(250, 250, 250),
            )
            if in_rect(close_rect, [20, 20], Mouse.position()):
                Draw.draw_rect(self.win(), close_rect, [20], (250, 150, 150))
                if Mouse.press():
                    self.view = False
            self.save_bt.pos = [self.pos[0] + 160, self.pos[1] + 30]
            self.input_box.text_box.pos = [self.pos[0] + 10, self.pos[1] + 30]
            self.input_box.render()
            self.input_box.update_pos_and_size()
            self.save_bt.render()
            if self.error:
                Draw.draw_hline(
                    self.win(),
                    self.pos[1] + self.size[1],
                    self.pos[0],
                    self.pos[0] + self.size[0],
                    3,
                    (250, 100, 100),
                )


class OpenWindow:
    def __init__(self, win, size) -> None:
        self.size = size
        self.pos = [0, 0]
        self.win = win
        self.view = False

        self.text_box = TextBox(self.win, self.pos, [300, 20])
        self.open_bt = TextButton(self.pos, [60, 20], "open", 18, win)

        self.open_text = Text("arial", 18, "Save scratch", (200, 200, 200), True)
        self.files_text = Text("arial", 16, color=(120, 120, 120), bold=True)
        self.files = []
        self.text_surf = pygame.Surface([360, 400])
        self.text_surf_pos = [0, 0]

    def render(self, SPC):
        if self.view:
            Draw.draw_rect(self.win(), self.pos, self.size, (120, 120, 120))
            close_rect = [self.pos[0] + self.size[0] - 20, self.pos[1]]
            Draw.draw_rect(self.win(), self.pos, [self.size[0], 20], (170, 170, 170))
            Draw.draw_rect(self.win(), close_rect, [20], (200, 100, 100))
            self.open_text.draw(
                self.win(),
                [self.pos[0] + 7, self.pos[1]],
                text="Open file",
                color=(250, 250, 250),
            )
            if in_rect(close_rect, [20, 20], Mouse.position()):
                Draw.draw_rect(self.win(), close_rect, [20], (250, 150, 150))
                if Mouse.press():
                    self.view = False
            self.text_surf.fill((80, 80, 80))

            json_files = list(filter(lambda elem: ".json" in elem, self.files))
            for i, filename in enumerate(json_files):
                file_rect = [self.pos[0] + 20 + 10, self.pos[1] + 40 + i * 20]
                if in_rect(file_rect, [360 - 30, 20], Mouse.position()):
                    Draw.draw_rect(
                        self.text_surf,
                        [self.text_surf_pos[0], self.text_surf_pos[1] + i * 20],
                        [360, 20],
                        (130, 130, 130),
                    )

                    if Mouse.press():
                        self.text_box.text_value = filename

                Draw.draw_rect(
                    self.text_surf,
                    [self.text_surf_pos[0] + 340, self.text_surf_pos[1] + i * 20],
                    [20, 20],
                    (250, 100, 100),
                )
                if in_rect(
                    [file_rect[0] + 360 - 30, file_rect[1]], [20, 20], Mouse.position()
                ):
                    Draw.draw_rect(
                        self.text_surf,
                        [self.text_surf_pos[0] + 340, self.text_surf_pos[1] + i * 20],
                        [20, 20],
                        (250, 150, 150),
                    )
                    if Mouse.click():
                        os.remove(filename)
                        self.get_files()

                self.files_text.draw(
                    self.text_surf,
                    [self.text_surf_pos[0] + 10, self.text_surf_pos[1] + i * 20],
                    text=filename,
                    color=(220, 220, 220),
                )

                self.files_text.draw(
                    self.text_surf,
                    [self.text_surf_pos[0] + 280, self.text_surf_pos[1] + i * 20],
                    text=str(
                        int(int(str(os.path.getsize("saves\\" + filename))) / 1024)
                    )
                    + " кб",
                    color=(220, 220, 220),
                )

            self.win().blit(self.text_surf, [self.pos[0] + 20, self.pos[1] + 40])
            self.text_box.pos = [self.pos[0] + 20, self.pos[1] + 460]
            self.open_bt.pos = [
                self.pos[0] + 20 + self.text_box.size[0],
                self.pos[1] + 460,
            ]
            self.text_box.render()
            self.open_bt.render()

            if self.open_bt.press:
                if ".json" in self.text_box.text_value:
                    SPC.load(self.text_box.text_value)
                    self.view = False

    def get_files(self):
        self.files = [f for f in listdir("saves")]


class UpInterface:
    def __init__(self, win: Window) -> None:
        self.pos = [0, 0]
        self.size = [1920, 20]
        self.win = win
        self.bt_OPENFILE = TextButton([0, 0], [60, 20], "open", 18, self.win)
        self.bt_SAVEFILE = TextButton([60, 0], [60, 20], "save", 18, self.win)
        self.fps_text = Text("arial", 16, color=(120, 120, 120), bold=True)

    def render(self):
        Draw.draw_rect(self.win(), self.pos, self.size, UP_INTERFACE_COLOR.rgb)
        self.bt_OPENFILE.render()
        self.bt_SAVEFILE.render()
        ws = self.win.get_size
        self.fps_text.draw(
            self.win(),
            [ws[0] - 60, 0],
            text="fps " + str(int(self.win.fps)),
            color=(200, 200, 200),
        )
