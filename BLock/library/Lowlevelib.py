# imports ---------------------------------------
import pygame_shaders
import threading
import keyboard
import pygame
import socket
import random
import typing
import pickle
import mouse
import types
import math
import time
import sys
import os


from .libtypes import Color
from dataclasses import dataclass
from colorama import Fore, Style
from io import TextIOWrapper
from ast import literal_eval
from threading import Thread
from typing import overload
from typing import Iterable
from pygame import gfxdraw
from typing import NewType
from typing import Tuple
from typing import Dict

from time import sleep
from typing import Any
from copy import copy

# imports ---------------------------------------


class Vector2:
    @overload
    def __init__(self, x_y: typing.Tuple[float, float]) -> "Vector2":
        ...

    @overload
    def __init__(self, x_: float, y_: float) -> "Vector2":
        ...

    def __init__(self, *_args) -> "Vector2":
        self.__args_manager__(*_args)

    def __args_manager__(self, *args):
        if len(args) == 1:
            self._x = args[0][0]
            self._y = args[0][1]
        elif len(args) == 2:
            self._x = args[0]
            self._y = args[1]

    def __str__(self) -> str:
        return f"Vector2 {self._x, self._y}"

    @property
    def lenght(self):
        return vector_lenght(self._x, self._y)

    @lenght.setter
    def lenght(self, _value: int):
        self._x *= _value / self.lenght
        self._y *= _value / self.lenght

    def rotate(self, angle: int):
        angle = math.radians(angle)
        _x = self._x * math.cos(angle) - self._y * math.sin(angle)
        _y = self._x * math.sin(angle) + self._y * math.cos(angle)
        self._x = _x
        self._y = _y

    def set_angle(self, angle: int):
        lenght = self.lenght
        angle = math.radians(angle)
        self._x = math.cos(angle) * lenght
        self._y = math.sin(angle) * lenght

    def get_angle(self) -> float:
        return angle_to_float([0, 0], [self._x, self._y])

    def normalyze(self):
        lenght = self.lenght
        self._x /= lenght
        self._y /= lenght

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def xy(self) -> typing.Tuple[int, int]:
        return [self._x, self._y]

    @xy.setter
    def xy(self, pos_: typing.Tuple[int, int]):
        self._x = pos_[0]
        self._y = pos_[1]

    def __iadd__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __isub__(self, vector_: "Vector2") -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y
        return self

    def __imul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_
        return self

    def __add__(self, vector_: "Vector2") -> "Vector2":
        self.x += vector_.x
        self.y += vector_.y
        return self

    def __mul__(self, value_: float) -> "Vector2":
        self.x *= value_
        self.y *= value_

        return self

    def __sub__(self, vector_: float) -> "Vector2":
        self.x -= vector_.x
        self.y -= vector_.y

        return self


# shader ----------------------------------------


class Shader:
    def __init__(self, size, pos, vertex_file_, fragment_file_) -> None:
        self.shader_ = pygame_shaders.Shader(
            size, size, pos, vertex_file_, fragment_file_, 0
        )

    def clear(self, color=(0, 0, 0)):
        pygame_shaders.clear(color)

    def render(self, surf: pygame.Surface):
        self.shader_.render(surf)

    def send(self, name, data):
        self.shader_.send(name, data)


# shader ----------------------------------------


# base decorators -------------------------------


def NewProcess(name: str = None):
    if name is None:
        name = random.randint(0, 99999999999)

    def NewProcessInner(func: typing.Callable):
        def wrapper(*args, **kvargs):
            Thread(target=func, args=args, kwargs=kvargs, name=name).start()

        return wrapper

    return NewProcessInner


def TimeProcess(func: typing.Callable):
    def wrapper(*args, **kvargs):
        start = time.time()
        func(*args, **kvargs)
        end = time.time()
        print(f"Time ({func.__name__}): {end - start}")

    return wrapper


def get_thread_count():
    return threading.active_count()


def get_threads():
    return threading.enumerate()


# base decorators -------------------------------

# sound class -----------------------------------


class Sound:
    def __init__(self, file_name_: str) -> "Sound":
        self._sound = pygame.mixer.Sound(file_name_)

    def play(self):
        self._sound.play()


# sound class -----------------------------------

# base window class -----------------------------


class Window:
    def __init__(
        self,
        size: list[int, int] = [800, 650],
        win_name: str = "Main",
        flag: typing.Any = None,
        cursor: Any = None,
    ) -> None:
        self.__size = size
        self.__win_name = win_name
        self.__flag = flag
        self._win_opened = False
        self._delta = 0
        self.__delta_velosity = 60
        self.__timer = 0
        self.size = [0, 0]

        self.__create_win_with_params(self.__size, self.__win_name, self.__flag)
        if cursor is not None:
            pygame.mouse.set_cursor(cursor)

        self._win_opened = True
        self._fps_surf = Text("Arial", 12, bold=True)
        self._exit_hot_key = "esc"
        self.press_key = None

    def __any_full__(self, _flag: typing.Any) -> bool:
        if type(_flag) == list:
            if _flag[0] == "anyfull":
                return True
        return False

    def __call__(self) -> pygame.Surface:
        return self._win

    def __create_win_with_params(
        self, _p_size: list, _p_win_name: str, _p_flag: typing.Any
    ) -> None:
        pygame.init()
        if self.__any_full__(_p_flag):
            _flag = _p_flag[1]
            _p_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        else:
            _flag = 0 if _p_flag is None else _p_flag
        self._win = pygame.display.set_mode(_p_size, _flag)
        pygame.display.set_caption(_p_win_name)
        self._clock = pygame.time.Clock()

    def __mathing_delta(self):
        fps = self.fps
        try:
            self._delta = self.__delta_velosity / fps
        except Exception:
            ...

    @property
    def delta(self) -> float:
        return self._delta

    @property
    def get_size(self) -> typing.Tuple[int, int]:
        return self._win.get_size()

    @property
    def center(self) -> typing.Tuple[int, int]:
        return [*self._win.get_rect().center]

    @property
    def fps(self):
        return self._clock.get_fps()

    @property
    def timer(self):
        return self.__timer

    @fps.setter
    def fps(self, _framerate: int):
        if _framerate == "max":
            _framerate = 5000
        elif _framerate == "min":
            _framerate = 30
        else:
            ...
        self._clock.tick(_framerate)

    def __events_handling(self):
        global mouse__wheel
        _events = pygame.event.get()
        mouse__wheel = [0, 0]
        self.press_key = None
        for event in _events:
            if event.type == pygame.QUIT:
                self._win_opened = False
                os._exit(0)
            elif event.type == pygame.MOUSEWHEEL:
                mouse__wheel = [event.x, event.y]
            if event.type == pygame.VIDEORESIZE:
                self.size = event.size  # or event.w, event.h

            if event.type == pygame.KEYDOWN:
                self.press_key = event.key

        if keyboard.is_pressed(self._exit_hot_key):
            self._win_opened = False
            os._exit(0)

    def fps_view(self):
        self._win.blit(
            self._fps_surf.render(f"FPS: {int( self.fps )}", "black")(), (10, 10)
        )

    def update(
        self,
        fps: int = 60,
        base_color: list | str = "white",
        fps_view: bool = True,
        exit_hot_key: str = "esc",
    ) -> None:
        self._exit_hot_key = exit_hot_key
        self.__events_handling()

        self.fps = fps
        self.__mathing_delta()
        try:
            self.__timer += 1 * self.delta
        except:
            ...

        pygame.display.flip()
        self._win.fill(base_color)

        if fps_view:
            self.fps_view()

        return self._win_opened

    def get_at(self, x: int, y: int) -> list:
        return self._win.get_at((x, y))


# base window class -----------------------------

# bin files -------------------------------------


def WirteBinaryFile(file_name_: str, data_: Any) -> Any:
    with open(file_name_, "wb") as file:
        pickle.dump(data_, file)


def LoadBinaryFile(file_name_: str) -> Any:
    file = open(file_name_, "rb")
    return pickle.load(file)


# bin files -------------------------------------

# collide ---------------------------------------


class Rect(Vector2):
    @overload
    def __init__(self, x: float, y: float, w: float, h: float) -> "Rect":
        ...

    @overload
    def __init__(self, pos: Tuple[float, float], size: Tuple[float, float]) -> "Rect":
        ...

    def __init__(self, *args):
        self.__args_wrapper(*args)
        self.colliding = True
        self.id = random.randint(0, 99999999999999)

    def __args_wrapper(self, *args):
        if len(args) == 4:
            _x = args[0]
            _y = args[1]
            self._w = args[2]
            self._h = args[3]
        elif len(args) == 2:
            _x = args[0][0]
            _y = args[0][1]
            self._w = args[1][0]
            self._h = args[1][1]
        super().__init__(_x, _y)

    def draw(self, win: Window):
        Draw.draw_rect(win, self.xy, self.wh, "red", 1)

    def collide_point(self, point: Tuple[float, float] | Vector2) -> bool:
        px, py = 0, 0
        if isinstance(point, Vector2):
            px = point.x
            py = point.y
        if isinstance(point, (list, tuple)):
            px = point[0]
            py = point[1]

        if (
            self.x < px
            and px < self.x + self.w
            and self.y < py
            and py < self.y + self.h
        ):
            return True

        return False

    def collide_rect(self, rect: "Rect", win: None = None):
        if self.colliding:
            min_x = min(self._x, rect._x)
            min_y = min(self._y, rect._y)

            max_x = max(self._x + self._w, rect._x + rect._w)
            max_y = max(self._y + self._h, rect._y + rect._h)

            if win is not None:
                Draw.draw_rect(
                    win,
                    [min_x - 2, min_y - 2],
                    [max_x - min_x + 4, max_y - min_y + 4],
                    "Blue",
                    2,
                )

            dist_w = distance([min_x, min_y], [max_x, min_y])
            dist_h = distance([min_x, min_y], [min_x, max_y])
            if dist_w < self._w + rect._w and dist_h < self._h + rect._h:
                return True
        return False

    @property
    def wh(self) -> Tuple[float, float]:
        return [self._w, self._h]

    @wh.setter
    def wh(self, size_: Tuple[float, float]):
        self._w = int(size_[0])
        self._h = int(size_[1])

    @property
    def w(self) -> float:
        return self._w

    @w.setter
    def w(self, w: float):
        self._w = w

    @property
    def h(self) -> float:
        return self._h

    @h.setter
    def h(self, h: float):
        self._h = h

    @property
    def y_up(self) -> float:
        return self._y

    @y_up.setter
    def y_up(self, y: float):
        self._y = y

    @property
    def y_down(self) -> float:
        return self._y + self._h

    @y_down.setter
    def y_down(self, y: float):
        self._y = y - self._h

    @property
    def x_left(self) -> float:
        return self._x

    @x_left.setter
    def x_left(self, x: float):
        self._x = x

    @property
    def x_right(self) -> float:
        return self._x + self._w

    @x_right.setter
    def x_right(self, x: float):
        self._x = x - self._w

    @property
    def center(self):
        return [self._x + self._w / 2, self._y + self._h / 2]

    @property
    def center_x(self):
        return self._x + self._w / 2

    @property
    def center_y(self):
        return self._y + self._h / 2

    @center_x.setter
    def center_x(self, _x: int):
        self._x = _x - self._w / 2

    @center_y.setter
    def center_y(self, _y: int):
        self._y = _y - self._h / 2

    @center.setter
    def center(self, pos):
        self._x = pos[0] - self._w / 2
        self._y = pos[1] - self._h / 2


# collide ---------------------------------------

# flags -----------------------------------------


@dataclass
class Flags:
    win_full = pygame.FULLSCREEN
    win_resize = pygame.RESIZABLE
    win_scales = pygame.SCALED
    win_noframe = pygame.NOFRAME
    opengl = pygame.OPENGL
    win_anyfull = ["anyfull", pygame.FULLSCREEN]

    cursor_diamond = pygame.cursors.diamond
    cursor_ball = pygame.cursors.ball
    cursor_arrow = pygame.cursors.arrow
    cursor_broken = pygame.cursors.broken_x


# flags -----------------------------------------


# base surface class ----------------------------


class Surface:
    def __init__(self, size: typing.Tuple[int, int] = [1, 1]) -> None:
        self.__size = size
        self._surface = pygame.Surface(self.__size)

    def __call__(self) -> pygame.Surface:
        return self._surface

    def __set_surface__(self, surface_: pygame.Surface) -> "Surface":
        self._surface = surface_
        return self

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self._surface.get_size()

    def copy(self) -> "Surface":
        dummy_ = self._surface.copy()
        dummy_surface_ = Surface().__set_surface__(dummy_)
        del dummy_
        return dummy_surface_

    def pre_surf(self, pos, size) -> "Surface":
        dummy_ = self._surface.subsurface(pos, size)
        dummy_surf_ = Surface().__set_surface__(dummy_)
        return dummy_surf_


# base surface class ----------------------------

# base text class -------------------------------


class Text:
    def __init__(
        self,
        font: pygame.Font,
        font_size: int,
        text: str = None,
        color: list | str = "white",
        bold: bool = False,
    ) -> None:
        pygame.font.init()

        self.__font = font
        self.__font_size = font_size
        self.__bold = bold
        self.__font_object = pygame.font.SysFont(
            self.__font, self.__font_size, self.__bold
        )
        if text is not None:
            self.__text = text
            self.__font_surf = self.__font_object.render(self.__text, True, color)

    def draw(
        self,
        surface: pygame.Surface,
        pos: list[int, int] = [0, 0],
        centering: bool = False,
        text: str = "",
        color: list | str = "white",
    ) -> None:
        self.__font_surf = self.__font_object.render(text, True, color)
        if centering:
            pos = [
                pos[0] - self.__font_surf.get_width() // 2,
                pos[1] - self.__font_surf.get_height() // 2,
            ]

        surface.blit(self.__font_surf, pos)
        return self.__font_surf.get_size()

    def render(self, text: str, color: list | str = "white") -> Surface:
        self.__text = text
        self.__font_surf = self.__font_object.render(self.__text, True, color)
        return Surface().__set_surface__(self.__font_surf)


# base text class -------------------------------


# ! image methods -------------------------------


def load_image(file_name_: str) -> pygame.Surface:
    return pygame.image.load(file_name_).convert_alpha()


top_left_ = NewType("top_left", "Sprite")
top_middle_ = NewType("top_middle", "Sprite")
top_right_ = NewType("top_right", "Sprite")
center_left_ = NewType("center_left", "Sprite")
center_middle_ = NewType("center_middle", "Sprite")
center_right_ = NewType("center_right", "Sprite")
down_left_ = NewType("down_left", "Sprite")
down_middle_ = NewType("down_middle", "Sprite")
down_right_ = NewType("down_right", "Sprite")

top_vertical_ = NewType("top_vertical", "Sprite")
center_vertical_ = NewType("center_vertical", "Sprite")
down_vertical_ = NewType("down_vertical", "Sprite")

left_horizontal_ = NewType("left_horizontal", "Sprite")
center_horizontal_ = NewType("center_horizontal", "Sprite")
right_horizontal_ = NewType("right_horizontal", "Sprite")

left_down_yes_ = NewType("left_down", "Sprite")
right_down_yes_ = NewType("right_down", "Sprite")
left_right_down_yes_ = NewType("left_right_down", "Sprite")

left_top_yes_ = NewType("left_up", "Sprite")
right_top_yes_ = NewType("right_up", "Sprite")
left_right_top_yes_ = NewType("left_right_up", "Sprite")

left_right_top_down_yes_ = NewType("left_right_up_down", "Sprite")


one_ = NewType("one", "Sprite")


# TODO New <> !!!!!!!!!
def load_block_cheat(
    file_name_: str, block_cheat_size_: int = 4, block_size_: Tuple[int, int] = [8, 8]
) -> Tuple[
    top_left_,
    top_middle_,
    top_right_,
    center_left_,
    center_middle_,
    center_right_,
    down_left_,
    down_middle_,
    down_right_,
    one_,
    top_vertical_,
    center_vertical_,
    down_vertical_,
    left_horizontal_,
    center_horizontal_,
    right_horizontal_,
    left_down_yes_,
    right_down_yes_,
    left_right_down_yes_,
    left_top_yes_,
    right_top_yes_,
    left_right_top_yes_,
    left_right_top_down_yes_,
]:
    sprite_image_ = load_image(file_name_)
    midle_image_ = sprite_image_.subsurface(
        [0, 0, block_size_[0] * 3, block_size_[1] * 3]
    )

    vertical_image_ = sprite_image_.subsurface(
        [block_size_[0] * 3, 0, block_size_[0], block_size_[1] * 3]
    )
    horizontal_image_ = sprite_image_.subsurface(
        [0, block_size_[1] * 3, block_size_[0] * 3, block_size_[1]]
    )
    one_image_ = sprite_image_.subsurface(
        [block_size_[0] * 3, block_size_[1] * 3, block_size_[0], block_size_[1]]
    )

    left_down_image = sprite_image_.subsurface(
        [block_size_[0] * 4, 0, block_size_[0], block_size_[1]]
    )
    right_down_image = sprite_image_.subsurface(
        [block_size_[0] * 4, block_size_[1], block_size_[0], block_size_[1]]
    )

    left_up_image = sprite_image_.subsurface(
        [block_size_[0] * 4, block_size_[1] * 3, block_size_[0], block_size_[1]]
    )
    right_up_image = sprite_image_.subsurface(
        [block_size_[0] * 4, block_size_[1] * 2, block_size_[0], block_size_[1]]
    )

    left_right_up_image = sprite_image_.subsurface(
        [block_size_[0] * 5, 0, block_size_[0], block_size_[1]]
    )
    left_right_down_image = sprite_image_.subsurface(
        [block_size_[0] * 5, block_size_[1], block_size_[0], block_size_[1]]
    )
    left_right_down_up_image = sprite_image_.subsurface(
        [block_size_[0] * 5, block_size_[1] * 2, block_size_[0], block_size_[1]]
    )

    sprites = {}
    sp_ = []
    for i in range(3):
        for j in range(3):
            sp_.append(
                midle_image_.subsurface(
                    [
                        j * block_size_[0],
                        i * block_size_[1],
                        block_size_[0],
                        block_size_[1],
                    ]
                )
            )

    sp_vertical_ = []
    for i in range(3):
        sp_vertical_.append(
            vertical_image_.subsurface(
                [0, i * block_size_[1], block_size_[0], block_size_[1]]
            )
        )

    sp_horizontal_ = []
    for i in range(3):
        sp_horizontal_.append(
            horizontal_image_.subsurface(
                [i * block_size_[0], 0, block_size_[0], block_size_[1]]
            )
        )

    sprites["top_left"] = Sprite(sp_[0])
    sprites["top_middle"] = Sprite(sp_[1])
    sprites["top_right"] = Sprite(sp_[2])
    sprites["center_left"] = Sprite(sp_[3])
    sprites["center_middle"] = Sprite(sp_[4])
    sprites["center_right"] = Sprite(sp_[5])
    sprites["down_left"] = Sprite(sp_[6])
    sprites["down_middle"] = Sprite(sp_[7])
    sprites["down_right"] = Sprite(sp_[8])

    sprites["top_vertical"] = Sprite(sp_vertical_[0])
    sprites["center_vertical"] = Sprite(sp_vertical_[1])
    sprites["down_vertical"] = Sprite(sp_vertical_[2])

    sprites["left_horizontal"] = Sprite(sp_horizontal_[0])
    sprites["center_horizontal"] = Sprite(sp_horizontal_[1])
    sprites["right_horizontal"] = Sprite(sp_horizontal_[2])

    sprites["one"] = Sprite(one_image_)

    sprites["left_down"] = Sprite(left_down_image)
    sprites["right_down"] = Sprite(right_down_image)

    sprites["left_up"] = Sprite(left_up_image)
    sprites["right_up"] = Sprite(right_up_image)

    sprites["left_right_up"] = Sprite(left_right_up_image)
    sprites["left_right_down"] = Sprite(left_right_down_image)
    sprites["left_right_up_down"] = Sprite(left_right_down_up_image)

    return sprites


class Sprite:
    # ? Sprite base methods

    def set_size(
        self,
        image_: pygame.Surface = None,
        scale_: float = 1,
        any_size_: Tuple[int, int] = None,
    ):
        if image_ is not None:
            if any_size_ is not None:
                _return_surf = pygame.transform.scale(image_, any_size_)
            else:
                _return_surf = pygame.transform.scale(
                    image_, [image_.get_width() * scale_, image_.get_height() * scale_]
                )
            return _return_surf
        else:
            if any_size_ is not None:
                _return_surf = pygame.transform.scale(self.image, any_size_)
            else:
                _return_surf = pygame.transform.scale(
                    self.image,
                    [self.image.get_width() * scale_, self.image.get_height() * scale_],
                )
            self.valid_image = copy(_return_surf)

    def set_angle(self, image_: pygame.Surface = None, angle_: float = 0):
        if image_ is not None:
            _return_surf = pygame.transform.rotate(image_, angle_)
            return _return_surf
        else:
            self.angle = angle_

    def set_mirror(self, x_=False, y_=False):
        self.valid_image = pygame.transform.flip(self.image, x_, y_)

    # ? Sprite base methods

    def __init__(self, start_sprite_: pygame.Surface) -> "Sprite":
        self.image = start_sprite_
        self.valid_image = copy(self.image)
        self.render_image = copy(self.image)
        self.pos = [0, 0]
        self.size = [0, 0]
        self.angle = 0

        self.__update_size__()

    def __update_size__(self):
        self.size = [*self.render_image.get_size()]

    @property
    def center(self):
        return self.pos

    @center.setter
    def center(self, center_pos_: Tuple[int, int]):
        self.pos = center_pos_

    @property
    def center_x(self):
        return self.pos[0]

    @center_x.setter
    def center_x(self, x_: int):
        self.pos[0] = x_

    @property
    def center_y(self):
        return self.pos[1]

    @center_y.setter
    def center_y(self, y_: int):
        self.pos[1] = y_

    def draw(self, win_: Window, centering: bool = True):
        self.render_image = pygame.transform.rotate(self.valid_image, self.angle)
        self.__update_size__()
        if centering:
            self.render_pos = [
                self.pos[0] - self.size[0] / 2,
                self.pos[1] - self.size[1] / 2,
            ]
        else:
            self.render_pos = self.pos
        win_().blit(self.render_image, self.render_pos)

    def draw_surf(self, surf_: pygame.Surface):
        self.render_image = pygame.transform.rotate(self.valid_image, self.angle)
        self.__update_size__()
        self.render_pos = [
            self.pos[0] - self.size[0] / 2,
            self.pos[1] - self.size[1] / 2,
        ]
        surf_.blit(self.render_image, self.render_pos)


# ? Succes!
class AnimatedSprite:
    # ? -----------------------------------------------------
    # ? | Colors                                            |
    # ? | Line color              -> (255,   0, 255)        |
    # ? | Colom color             -> (255, 255,   0)        |
    # ? | Size color              -> (  0,   0, 255)        |
    # ? -----------------------------------------------------
    @classmethod
    def load_sprites(self, file_name_: str) -> Tuple[pygame.Surface, ...]:
        canvas_ = pygame.image.load(file_name_)

        width_ = canvas_.get_size()[0]
        height_ = canvas_.get_size()[1]

        spritets_coloms = []
        sizes_poses = []

        for i in range(height_):
            c = canvas_.get_at([0, i])
            color = (c[0], c[1], c[2])
            if color == (255, 0, 255):
                spritets_coloms.append(i)

        for col in spritets_coloms:
            for line in range(width_):
                c = canvas_.get_at([line, col])
                color = (c[0], c[1], c[2])
                if color == (255, 255, 0):
                    pos = [line + 1, col]
                    spw = 0
                    sph = 0
                    for sw in range(width_ - line):
                        c = canvas_.get_at([line + sw, col])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            spw = sw
                            break
                    for sh in range(height_ - col):
                        c = canvas_.get_at([line, col + sh])
                        color = (c[0], c[1], c[2])
                        if color == (0, 0, 255):
                            sph = sh
                            break
                    sizes_poses.append([[pos[0], pos[1] + 1], [spw, sph]])
        textures = []
        for sp in sizes_poses:
            canvas_.set_clip(sp[0], sp[1])
            texture = canvas_.get_clip()
            surft = canvas_.subsurface(texture)
            textures.append(surft)
        return textures

    def __create_sprites__(self, file_name_: str) -> Tuple[Sprite, ...]:
        _sprites = self.load_sprites(file_name_)

        _new_sprites = [Sprite(_image) for _image in _sprites]
        return _new_sprites

    def __init__(self, file_name_: str, speed_: int = 10, stoped: bool = False) -> None:
        self._sprites = self.__create_sprites__(file_name_)
        self._time = 0
        self._run = False
        self._speed = speed_
        self._stoped = stoped
        self._render = True
        self.pos = [0, 0]

        self.index = 0

    def set_sprite(self, index):
        self.index = index

    def end_sprite(self):
        if self.index == len(self._sprites) - 1:
            return True
        return False

    def set_size(
        self,
        scale_: float = 1,
        any_size_: Tuple[int, int] = None,
    ):
        for sprite in self._sprites:
            sprite.set_size(scale_=scale_, any_size_=any_size_)

    def set_angle(self, angle_: float = 0):
        for sprite in self._sprites:
            sprite.set_angle(angle_=angle_)

    def set_mirror(self, x_=False, y_=False):
        for sprite in self._sprites:
            sprite.set_mirror(x_=x_, y_=y_)

    def start(self):
        self._run = True

    def stop(self):
        self._run = False

    @property
    def center(self):
        return self.pos

    @center.setter
    def center(self, center_pos_: Tuple[int, int]):
        self.pos = center_pos_
        for sprite in self._sprites:
            sprite.center = center_pos_

    @property
    def center_x(self):
        return self._sprites[0].center_x

    @center_x.setter
    def center_x(self, x_: int):
        self.pos[0] = x_
        for sprite in self._sprites:
            sprite.center_x = x_

    @property
    def center_y(self):
        return self._sprites[0].center_y

    @center_y.setter
    def center_y(self, y_: int):
        self.pos[1] = y_
        for sprite in self._sprites:
            sprite.center_y = y_

    def update(self):
        if self._run:
            self._time += 1

            if self._time % self._speed == 0:
                self.index += 1

            if self.index == len(self._sprites):
                if self._stoped:
                    self._render = False
                else:
                    self.index = 0

    def render(self, win_: Window):
        if self._render:
            self._sprites[self.index].draw(win_)


# ! image methods -------------------------------


# base math class -------------------------------


def two_element_typing_xy(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return iterable_[0], iterable_[1]
    elif isinstance(iterable_, Vector2):
        return iterable_.x, iterable_.y


def two_element_typing_x_y(iterable_: list | tuple | Vector2):
    if isinstance(iterable_, (list, tuple)):
        return [iterable_[0], iterable_[1]]
    elif isinstance(iterable_, Vector2):
        return [iterable_.x, iterable_.y]


def distance(
    point_1: Any | typing.Tuple[int, int], point_2: Any | typing.Tuple[int, int]
):
    dx = point_1[0] - point_2[0]
    dy = point_1[1] - point_2[1]
    _distance = math.sqrt(dx**2 + dy**2)
    return _distance


# create method get center position with two point type list ot type vector2 ->


def center_pos(
    point_1: Vector2 | typing.Tuple[int, int], point_2: Vector2 | typing.Tuple[int, int]
):
    x1, y1 = two_element_typing_xy(point_1)
    x2, y2 = two_element_typing_xy(point_2)
    dx = (x1 - x2) / 2
    dy = (y1 - y2) / 2
    return [x2 + dx, y2 + dy]


def vector_lenght(lenght_x: int, lenght_y: int):
    _distance = math.sqrt(lenght_x**2 + lenght_y**2)
    return _distance


def rect_center(rect_pos: typing.Tuple[int, int], rect_size: typing.Tuple[int, int]):
    return [rect_pos[0] + rect_size[0] / 2, rect_pos[1] + rect_size[1] / 2]


def angle_to(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    pos1 = two_element_typing_x_y(point_1)
    pos2 = two_element_typing_x_y(point_2)

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return int(atan / math.pi * 180 + 180)


def center_rect(
    pos: typing.Tuple[int, int], size: typing.Tuple[int, int], _reverse: bool = False
) -> Tuple[int, int]:
    if not _reverse:
        return [pos[0] + size[0] / 2, pos[1] + size[1] / 2]
    else:
        return [pos[0] - size[0] / 2, pos[1] - size[1] / 2]


def angle_to_float(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    if isinstance(point_1, Vector2):
        pos1 = point_1.xy
    elif isinstance(point_1, (list, tuple)):
        pos1 = point_1

    if isinstance(point_2, Vector2):
        pos2 = point_2.xy
    elif isinstance(point_2, (list, tuple)):
        pos2 = point_2

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return (atan / math.pi * 180 + 180) % 360


def in_rect(
    rect_pos_: typing.Tuple[float, float] | Vector2,
    rect_size_: typing.Tuple[float, float] | Vector2,
    point_: typing.Tuple[float, float] | Vector2,
):
    if isinstance(rect_pos_, Vector2):
        rect_pos = rect_pos_.xy
    elif isinstance(rect_pos_, (list, tuple)):
        rect_pos = rect_pos_

    if isinstance(rect_size_, Vector2):
        rect_size = rect_size_.xy
    elif isinstance(rect_size_, (list, tuple)):
        rect_size = rect_size_

    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_

    if (
        point[0] > rect_pos[0]
        and point[0] < rect_pos[0] + rect_size[0]
        and point[1] > rect_pos[1]
        and point[1] < rect_pos[1] + rect_size[1]
    ):
        return True
    else:
        return False


def sin(value: float) -> float:
    return math.sin(value)


def cos(value: float) -> float:
    return math.cos(value)


# base math class -------------------------------

# base draw class -------------------------------


class Draw:
    @classmethod
    def __outline(self, _color, _width, _type, _surf, **kvargs):
        if _type == "rect":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            size = kvargs["size"]
            Draw.draw_rect(_surf, pos, size, _color, _width, radius=radius)
        elif _type == "circle":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            Draw.draw_circle(_surf, pos, radius, _color, _width)
        elif _type == "polygone":
            points = kvargs["points"]
            Draw.draw_polygone(_surf, points, _color, _width)

    @classmethod
    def draw_rect(
        self,
        surface: pygame.Surface,
        pos: list[int],
        size: list[int],
        color: list | str | Color = "gray",
        width: int = 0,
        radius: int = -1,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(radius, (list, tuple)):
            lt_rad = radius[0]
            rt_rad = radius[1]
            rb_rad = radius[2]
            lb_rad = radius[3]
            radius = -1
        else:
            lt_rad = radius
            rt_rad = radius
            rb_rad = radius
            lb_rad = radius
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.rect(
            surface, color, (pos, size), width, radius, lt_rad, rt_rad, lb_rad, rb_rad
        )

        if outline is not None:
            Draw.__outline(
                outline[0],
                outline[1],
                "rect",
                surface,
                radius=(lt_rad, rt_rad, rb_rad, lb_rad),
                pos=pos,
                size=size,
            )

    @classmethod
    def draw_circle(
        self,
        surface: pygame.Surface,
        pos: list[int],
        radius: int,
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
        centering: bool = False,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.circle(surface, color, pos, radius, width)
        if centering:
            pos = [pos[0] + radius, pos[1] + radius]

        if outline is not None:
            Draw.__outline(
                outline[0], outline[1], "circle", surface, pos=pos, radius=radius
            )

    @classmethod
    def draw_polygone(
        self,
        surface: pygame.Surface,
        points: list[list[int]],
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.polygon(surface, color, points, width)

        if outline is not None:
            Draw.__outline(outline[0], outline[1], "polygone", surface, points=points)

    @classmethod
    def draw_line(
        self,
        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        pygame.draw.line(surface, color, pos1, pos2, width)

    @classmethod
    def draw_dashed_line(
        self,
        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_line(surface, pos1, delta_pos, color, width)
            pos1 = delta_pos

    @classmethod
    def draw_dashed_hline(
        self,
        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_hline(surface, pos1[1], pos1[0], delta_pos[0], width, color)
            pos1 = delta_pos

    @classmethod
    def draw_dashed_vline(
        self,
        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        vector = Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1])
        lenght = vector.lenght
        vector.normalyze()
        vector *= dash_size
        delta_pos = pos1
        for i in range(int(lenght // dash_size)):
            delta_pos = [pos1[0] - vector.x, pos1[1] - vector.y]
            if i % 2 == 0:
                Draw.draw_vline(surface, pos1[0], pos1[1], delta_pos[1], width, color)
            pos1 = delta_pos

    @classmethod
    def draw_lines(
        self,
        surface: pygame.Surface,
        points: Tuple[Tuple[float, float], ...],
        color: Tuple[int, int, int] | str | Color,
        width: int,
        closed: bool = False,
        blend: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                pygame.draw.aalines(surface, color, closed, points_, blend)

    @classmethod
    def draw_vline(
        self,
        surface: pygame.Surface,
        x: int,
        y1: int,
        y2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.vline(surface, int(x - int(width / 2) + i), int(y1), int(y2), color)

    @classmethod
    def draw_hline(
        self,
        surface: pygame.Surface,
        y: int,
        x1: int,
        x2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            gfxdraw.hline(surface, int(x1), int(x2), int(y - int(width / 2) + i), color)

    @classmethod
    def draw_bezier(
        self,
        surface: pygame.Surface,
        points: Tuple[Tuple[float, float], ...],
        steps: int = 2,
        color: Tuple[int, int, int] | str | Color = (100, 100, 100),
        width: int = 1,
    ):
        if isinstance(color, Color):
            color = color.rgb
        for i in range(width):
            for j in range(width):
                points_ = list(
                    map(
                        lambda elem: [
                            elem[0] + i - width // 2,
                            elem[1] + j - width // 2,
                        ],
                        points,
                    )
                )
                gfxdraw.bezier(surface, points_, steps, color)

    @classmethod
    def draw_rect_fast(
        self,
        surface: pygame.Surface,
        pos: list[int],
        size: list[int],
        color: list | str | Color = "gray",
    ):
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(color, Color):
            color = color.rgb
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        gfxdraw.rectangle(surface, rect, color)

    @classmethod
    def draw_dashed_lines(
        self,
        surface: pygame.Surface,
        points: list,
        color: list | str | Color = "gray",
        width: int = 1,
        dash_size: int = 10,
    ):
        for i in range(len(points)):
            if i + 1 < len(points):
                Draw.draw_dashed_line(
                    surface, points[i], points[i + 1], color, width, dash_size
                )

    @classmethod
    def draw_arc(
        self,
        surface: pygame.Surface,
        center_pos: list,
        color: list | str | Color = "gray",
        start_angle: int = 0,
        stop_angle: int = 175,
        radius: int = 100,
        width: int = 50,
        step: int = 20,
    ):
        if isinstance(color, Color):
            color = color.rgb
        if width != 1:
            stop_angle = stop_angle % 361
            toch = step
            ang_step = (start_angle - stop_angle) / toch
            width = min(radius, width)

            start_pos = [
                center_pos[0] + sin(math.radians(start_angle)) * (radius - width),
                center_pos[1] + cos(math.radians(start_angle)) * (radius - width),
            ]
            poses = []
            poses.append(start_pos)

            for i in range(toch + 1):
                x = center_pos[0] + sin(math.radians(start_angle)) * radius
                y = center_pos[1] + cos(math.radians(start_angle)) * radius
                start_angle += ang_step

                poses.append([x, y])
            start_angle -= ang_step
            for i in range(toch):
                x = center_pos[0] + sin(math.radians(start_angle)) * (radius - width)
                y = center_pos[1] + cos(math.radians(start_angle)) * (radius - width)
                start_angle -= ang_step

                poses.append([x, y])

            Draw.draw_polygone(surface, poses, color)
        else:
            pygame.draw.arc(
                surface,
                color,
                [
                    center_pos[0] - radius,
                    center_pos[1] - radius,
                    radius * 2,
                    radius * 2,
                ],
                math.radians(start_angle + 90),
                math.radians(stop_angle + 90),
            )


# base draw class -------------------------------

# base input class ------------------------------

mouse__wheel = 0


class Mouse:
    left = "_left"
    right = "_right"
    middle = "_middle"

    end_pos = [0, 0]
    pressed = False

    @classmethod
    @property
    def whell(self):
        global mouse__wheel
        return mouse__wheel

    @classmethod
    def position(self, win_scale_: float = 1) -> list[int, int]:
        pos = [*pygame.mouse.get_pos()]
        if win_scale_ != 1:
            win_scale_ += 0.5
        pos[0] *= win_scale_
        pos[1] *= win_scale_
        return pos

    def set_position(self, pos: typing.Tuple[int, int]) -> None:
        pygame.mouse.set_pos(pos)

    @classmethod
    def set_hide(self):
        pygame.mouse.set_visible(False)

    @classmethod
    def set_show(self):
        pygame.mouse.set_visible(True)

    @classmethod
    def press(self, button: str = left):
        if button == Mouse.left:
            return pygame.mouse.get_pressed()[0]
        if button == Mouse.middle:
            return pygame.mouse.get_pressed()[1]
        if button == Mouse.right:
            return pygame.mouse.get_pressed()[2]

    @classmethod
    def click(self, button: str = left):
        p = self.press(button)
        if p:
            if not self.pressed:
                self.pressed = True
                return True
            else:
                return False
        else:
            self.pressed = False
            return False

    @classmethod
    @property
    def speed(self) -> typing.Tuple[int, int]:
        pos = self.position()
        dx = pos[0] - self.end_pos[0]
        dy = pos[1] - self.end_pos[1]

        self.end_pos = copy(pos)
        return [dx, dy]

    @classmethod
    def set_cursor(self, cursor: Any) -> None:
        pygame.mouse.set_cursor(cursor)


class Keyboard:
    def key_pressed(key):
        return keyboard.is_pressed(key)

    def key_pressed_win(key):
        akt = pygame.mouse.get_focused()
        if akt:
            return keyboard.is_pressed(key)
        else:
            return False


# base input class ------------------------------


# base socket manager ---------------------------


def string_to_list(string_: str) -> list:
    return literal_eval(string_)


def list_to_string(list_: list) -> str:
    return str(list_)


def packing(data_: Iterable, packet_name_: str) -> bytes:
    _inf = [packet_name_, data_]
    convert_data = list_to_string(_inf).encode()
    return convert_data


def unpacking(data_: bytes) -> list:
    convert_data = string_to_list(data_.decode())
    return convert_data


def socket_sleep(sec_: float):
    sleep(sec_)


def packet_with_name(data_: Any, name_: str):
    if data_[0] == name_:
        return data_[1]
    else:
        None


localhost = "localhost"


class Server:
    def __init__(
        self,
        port_: int = 4000,
        host_: str = localhost,
        name_: str = "my server",
        max_client_: int = 2,
    ) -> None:
        self._port = port_
        self._host = host_
        self._name = name_

        self._clients: typing.Tuple[socket.socket] = []

        self._client_connecting = False

        self._max_client = max_client_

        self._end_conn_client = None
        self._end_conn_addr = None

        self.__init()

    def __init(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._server.bind((self._host, self._port))
        self._server.setblocking(0)
        self._server.listen(5)

    @property
    def clientcon(self) -> bool:
        return self._client_connecting

    @property
    def max_connected(self) -> bool:
        if len(self._clients) == self._max_client:
            return False
        else:
            return True

    def waitcon(self, sec_: float):
        sleep(sec_)
        self._client_connecting = False
        if len(self._clients) < self._max_client:
            try:
                client, addr = self._server.accept()
                client.setblocking(0)
                self._client_connecting = True
                self._clients.append([client, addr])
                self._end_conn_client = client
                self._end_conn_addr = addr

                print(f"Client {addr} connected!")
            except:
                self._client_connecting = False

    def send_packet(self, packet_: bytes) -> None:
        for client in self._clients:
            try:
                client[0].send(packet_)
            except:
                ...

    def recv_packet(self, buf_size: int = 2048) -> str:
        packets = []
        for client in self._clients:
            packet = client[0].recv(buf_size)
            _inf = packet.decode()
            _list_inf = string_to_list(_inf)
            packets.append(_list_inf)
        return packets


class Client:
    def __init__(self, port_: int = 4000, host_: str = localhost) -> "Client":
        self._port = port_
        self._host = host_

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self._client.connect((self._host, self._port))
        print(f"Connected!")

    def recv_packet(self, buf_size: int = 2048) -> str:
        packet = self._client.recv(buf_size)
        _inf = packet.decode()
        return _inf

    def send_packet(self, packet_: bytes) -> None:
        try:
            self._client.send(packet_)
        except:
            ...


# base socket manager ---------------------------

# data bases ------------------------------------


class _DataBaseReader:
    @classmethod
    def read(self, DataBaseName_: str):
        _DataBaseFile = open(DataBaseName_, "r")
        _dummy = self.__reader__(_DataBaseFile)
        _dummy = self.__converter__(_dummy)
        return _dummy

    @classmethod
    def write(self, DataBase_: str, DataBaseName_: str):
        _DataBaseFile = open(DataBaseName_, "r")

    @classmethod
    def __reader__(self, DataBaseFile: TextIOWrapper):
        _dummy = []
        for _stroke in DataBaseFile.readlines():
            _dummy.append(_stroke.replace("\n", "").replace("   ", ""))

        return _dummy

    @classmethod
    def __write_pack_former__(self, DataBase: dict):
        pack = ""
        for elem in DataBase:
            name = elem
            for nick in DataBase[elem]:
                person = nick

    @classmethod
    def __writer__(self, DataBaseFile: TextIOWrapper, DataBase: dict):
        ...

    @classmethod
    def __type_converter__(self, typingString_: str):
        returnedType = None
        try:
            returnedType = float(typingString_)
        except:
            returnedType = typingString_

        return returnedType

    @classmethod
    def __converter__(self, dummy_: list[str]):
        base_conv_opened = False
        wrapped_base = []
        conv = []
        for index, stroke_ in enumerate(dummy_):
            if base_conv_opened and stroke_ != "};":
                dummy_conv = copy(stroke_)
                dummy_conv_list = dummy_conv.split(": ")
                dataName = dummy_conv_list[0][1:]
                data = self.__type_converter__(dummy_conv_list[1])
                conv.append([dataName, data])

            if stroke_ == "};":
                wrapped_base.append(conv)
                conv = []
                base_conv_opened = False

            if stroke_ != "" and stroke_[0] == "[":
                dummy_stroke = copy(stroke_)
                dummy_list = dummy_stroke.split(" ")
                personName = dummy_list[1]
                convName = dummy_list[3]
                base_conv_opened = True
                conv.append([personName, convName])

        return wrapped_base


class DataBase:
    def __init__(self, DataBase: str) -> None:
        self._dataBase = DataBase
        self._db_reader = _DataBaseReader.read(self._dataBase)
        self.__convert_data_base__(self._db_reader)

    def __convert_data_base__(self, data_base_dummy_: list):
        self._DATA_BASE = {}

        for base_object in data_base_dummy_:
            data_data = base_object[0]
            data_name = data_data[1]
            data_person = data_data[0]
            data = {}
            __not_wrapped_data = base_object[1:]
            for bs in __not_wrapped_data:
                data[bs[0]] = bs[1]

            my_data = {}
            my_data[data_person] = data
            self._DATA_BASE[data_name] = my_data

    def show(self):
        for bs in self._DATA_BASE:
            bg = self._DATA_BASE[bs]

            for kk in bg:
                nm = bg[kk]
                print(bs, f"[ {kk} ]")
                for ll in nm:
                    print("    ", ll, " ", nm[ll])

    def get(self, person_name: str, pack_name: str):
        ret_data = {}
        for elem in self._DATA_BASE:
            _inf = self._DATA_BASE[elem]
            for inf_name in _inf:
                if inf_name == person_name and elem == pack_name:
                    ret_data = _inf[inf_name]
                    return ret_data


# data bases ------------------------------------
