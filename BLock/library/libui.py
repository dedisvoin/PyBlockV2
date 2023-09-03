from copy import copy
from library.Lowlevelib import Color
from library.Lowlevelib import Vector2
from library.Lowlevelib import Window
from library.Lowlevelib import Draw
from library.Lowlevelib import in_rect
from library.Lowlevelib import Mouse

from typing import overload, NewType, Tuple

_Float_int = NewType("Float_or_Int", [int, float])
_Sized_vector = NewType("Sized_Vector", tuple[_Float_int, _Float_int])


_Box_Type = NewType("Box", "Box")
_Style_Type = NewType("Style", "Style")


class _StylePropertes:
    size: _Sized_vector
    pos: _Sized_vector
    outline: _Float_int = 1
    outline_color: Color = Color([10, 10, 10])

    color: Color = Color([100, 100, 100])
    radius: _Float_int = 100
    width: _Float_int = 0
    rect_radius: _Float_int | Tuple[_Float_int, _Float_int, _Float_int, _Float_int] = -1

    pos_prperty: str = "Any"
    size_proprety: str = "Any"

    pos_dx: _Float_int = 0
    pos_dy: _Float_int = 0
    size_dw: _Float_int = 0
    size_dh: _Float_int = 0

    reflect_pos: _Sized_vector = []
    reflect_size: _Sized_vector = []
    reflect_color: Color = None

    sub_box: _Box_Type = None

    mouse_pressed: bool = False
    mouse_press_color: Color = Color([50, 50, 50])
    mouse_release_color: Color = Color([150, 150, 150])


class Style(_StylePropertes):
    def __init__(self, object_type_: any) -> _Style_Type:
        self.object_type_ = object_type_


class Box:
    @overload
    def __init__(
        self, width_: _Float_int, height_: _Float_int, x_: _Float_int, y_: _Float_int
    ) -> _Box_Type:
        ...

    @overload
    def __init__(self, size_: _Sized_vector, pos_: _Sized_vector) -> _Box_Type:
        ...

    def __init__(self, *args, Window_: Window) -> None:
        self.__wrapper__(*args)

        self.style = Style("Box")
        self._window = Window_

        self.style.pos = [self._x, self._y]
        self.style.size = [self._width, self._height]

    def __wrapper__(self, *args):
        if len(args) == 4:
            self._width = args[0]
            self._height = args[1]
            self._x = args[2]
            self._y = args[3]
        elif len(args) == 2:
            self._width = args[0][0]
            self._height = args[0][1]
            self._x = args[1][0]
            self._y = args[1][1]

    @property
    def __center__(self):
        return [
            self.style.reflect_pos[0] + self.style.reflect_size[0] / 2,
            self.style.reflect_pos[1] + self.style.reflect_size[1] / 2,
        ]

    def update(self):
        if self.style.sub_box is None:
            if "win_width" in self.style.size_proprety:
                self.style.size[0] = self._window.size[0]
            if "win_height" in self.style.size_proprety:
                self.style.size[1] = self._window.size[1]

            self.style.reflect_size = [
                self.style.size[0] - self.style.size_dw,
                self.style.size[1] - self.style.size_dh,
            ]

            if "center" in self.style.pos_prperty:
                win_center = self._window.center
                win_center[0] -= self.style.size[0] / 2
                win_center[1] -= self.style.size[1] / 2
                self.style.pos = copy(win_center)

            if "top" in self.style.pos_prperty:
                self.style.pos[1] = 0
            if "down" in self.style.pos_prperty:
                self.style.pos[1] = self._window.size[1] - self.style.size[1]
            if "left" in self.style.pos_prperty:
                self.style.pos[0] = 0
            if "right" in self.style.pos_prperty:
                self.style.pos[0] = self._window.size[0] - self.style.size[0]

            self.style.reflect_pos = [
                self.style.pos[0] + self.style.pos_dx,
                self.style.pos[1] + self.style.pos_dy,
            ]
            self.style.reflect_size = [
                self.style.size[0] - self.style.size_dw,
                self.style.size[1] - self.style.size_dh,
            ]

        else:
            if "box_width" in self.style.size_proprety:
                self.style.size[0] = self.style.sub_box.style.reflect_size[0]
            if "box_height" in self.style.size_proprety:
                self.style.size[1] = self.style.sub_box.style.reflect_size[1]

            self.style.reflect_size = [
                self.style.size[0] - self.style.size_dw,
                self.style.size[1] - self.style.size_dh,
            ]

            if "center" in self.style.pos_prperty:
                win_center = self.style.sub_box.__center__
                win_center[0] -= self.style.reflect_size[0] / 2
                win_center[1] -= self.style.reflect_size[1] / 2
                self.style.pos = copy(win_center)

            if "top" in self.style.pos_prperty:
                self.style.pos[1] = self.style.sub_box.style.reflect_pos[1]
            if "down" in self.style.pos_prperty:
                self.style.pos[1] = (
                    self.style.sub_box.style.reflect_pos[1]
                    + self.style.sub_box.style.reflect_size[1]
                    - self.style.size[1]
                )
            if "left" in self.style.pos_prperty:
                self.style.pos[0] = self.style.sub_box.style.reflect_pos[0]
            if "right" in self.style.pos_prperty:
                self.style.pos[0] = (
                    self.style.sub_box.style.reflect_pos[0]
                    + self.style.sub_box.style.reflect_size[0]
                    - self.style.size[0]
                )

            self.style.reflect_pos = [
                self.style.pos[0] + self.style.pos_dx,
                self.style.pos[1] + self.style.pos_dy,
            ]

        self.style.reflect_color = self.style.color
        if self.style.mouse_pressed:
            if in_rect(self.style.reflect_pos, self.style.reflect_size, Mouse.position):
                self.style.reflect_color = self.style.mouse_release_color
                if Mouse.press():
                    self.style.reflect_color = self.style.mouse_press_color

    def render(self):
        Draw.draw_rect(
            self._window(),
            self.style.reflect_pos,
            self.style.reflect_size,
            self.style.reflect_color.rgb,
            self.style.width,
            self.style.rect_radius,
            outline=[self.style.outline_color, self.style.outline],
        )
