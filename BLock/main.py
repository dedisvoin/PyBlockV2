from points import Point, PointType, SocketType, POINT_TYPE_COLORS
from widgets import TextBox, InputBox, DropDown, Slider
from interface import UpInterface, SaveWindow, OpenWindow
from library.liball import *
from saveload import save
import json


# start settings -----------------------------------------------------

win = Window(size=[1200, 750], flag=Flags.win_resize)
Mouse.set_hide()
Mouse_color = Color([0, 0, 0])

# start settings -----------------------------------------------------


# engine settings ----------------------------------------------------


class Engine:
    def __init__(self, win_: Window) -> None:
        self.mouse_celit_block = False
        self.mouse_pos = []
        self.__win = win_

        self.points = []

    def RenderMouse(self):
        self.mouse_pos = Mouse.position()
        Draw.draw_circle(self.__win(), self.mouse_pos, 3, Mouse_color)
        if self.mouse_celit_block:
            Draw.draw_circle(self.__win(), self.mouse_pos, 7, Mouse_color, 1)

    def update_points(self):
        [point.update() for point in self.points]

    def render_points_type(self):
        [point.render_data() for point in self.points]

    # def render_points(self):
    #    [point.render() for point in self.points]


class Space:
    def __init__(self, eng) -> None:
        self.blocks = []
        self.eng = eng
        self.vertical_lines = []
        self.horizontal_lines = []
        
        
    
            
        
            

    def Update(self):
        ENG.mouse_celit_block = False
        for bi, block in enumerate(self.blocks):
            block.update(speed)
            block.render()
            if in_rect(block.bone.pos, block.bone.size, Mouse.position()):
                ENG.mouse_celit_block = True

                if Keyboard.key_pressed("del"):
                    ids = list(map(lambda elem: elem.block_id, ENG.points))
                    while block.bone.id in ids:
                        ids = list(map(lambda elem: elem.block_id, ENG.points))
                        for i in range(len(ENG.points)):
                            p = ENG.points[i]
                            if p.block_id == block.bone.id:
                                if p.socket_type == SocketType.OUTPUT:
                                    for poi in ENG.points:
                                        if poi.id in p.my_con_points_ids:
                                            poi.point_type = poi.start_point_type
                                            poi.connectpoint_id = None

                                del ENG.points[i]
                                break
                    else:
                        del self.blocks[bi]
                        break
        for block in self.blocks:
            try:
                block.render_data() 
            except:...
        [block.render() for block in self.blocks]

    def recreating(self, data):
        for block_data in data:
            block_type = block_data["name"]
            block_id = block_data["id"]
            block_pos = block_data["pos"]
            block_points = block_data["points"]
            block = None
            if block_type in AllBlocks:
                block = AllBlocks[block_type](block_pos)

            block.id = block_id

            if block is not None:
                for point in block_points:
                    block.set_points(point[0], point[3], point[2], point[1], point[4])

    def load(self, file_name):
        self.blocks = []
        self.eng.points = []
        with open("saves\\" + file_name, "r") as f:
            data = json.load(f)
            self.recreating(data)


# engine settings ----------------------------------------------------


# blocks classes -----------------------------------------------------


class BlockType:
    NUMBER_TYPE: str = "NUMBER_TYPE"
    STRING_TYPE: str = "STRING_TYPE"
    FUNCTION_TYPE: str = "FUNCTION_TYPE"
    ERROR_TYPE: str = "ERROR_TYPE"
    BOOL_TYPE: str = "BOOL_TYPE"
    LIST_TYPE: str = "LIST_TYPE"
    RENDER_TYPE: str = "RENDER_TYPE"


BLOCK_TYPE_COLORS = {
    BlockType.NUMBER_TYPE: Color([100, 100, 250]),
    BlockType.STRING_TYPE: Color([250, 140, 100]),
    BlockType.FUNCTION_TYPE: Color([150, 100, 200]),
    BlockType.ERROR_TYPE: Color([200, 100, 100]),
    BlockType.BOOL_TYPE: Color((100, 160, 160)),
    BlockType.LIST_TYPE: Color((200, 100, 200)),
    BlockType.RENDER_TYPE: Color((150,150,250))
}

BlockType_ = NewType("BlockType", str)
BlockBaseColor = Color([200, 200, 200])


class _BoneBlock:
    def __init__(
        self,
        pos_: list,
        size_: list,
        block_type_: BlockType_,
        win_: Window,
        block_name_: str,
        engine_: Engine,
        w_r: bool = False,
        h_r: bool = False,
    ) -> "_BoneBlock":
        self.pos = pos_
        self.__size = size_

        self.win = win_
        self.__engine = engine_

        self.__block_type = block_type_

        self.id = id_generate(8)

        self.__block_name = block_name_

        self.__HEADER_SIZE = 20
        self.__Generate_name()

        self.__opened = True
        self.__pressed = False
        self.__o_c_pressed = False

        self.width_resized = w_r
        self.height_resized = h_r

        self.start_size = copy(self.__size)

        self.end_pos = [0, 0]
        self.speed = [0, 0]

    @property
    def HEADER_SIZE(self):
        return self.__HEADER_SIZE

    @property
    def pressed(self):
        return self.__pressed

    @pressed.setter
    def pressed(self, val):
        self.__pressed = val

    @property
    def opened(self):
        return self.__opened

    @property
    def name(self):
        return self.__block_name

    @property
    def size(self):
        return self.__size

    def __Generate_name(self):
        self.__block_name_text = (
            Text("arial", self.__HEADER_SIZE - 3, self.__block_name, "grey", True)
            .render(self.__block_name, (255, 255, 255))
            ._surface
        )

    def render_error(self):
        size_1 = self.size[1]
        if not self.opened:
            size_1 = self.HEADER_SIZE
        Draw.draw_hline(
            self.win(),
            self.pos[1] + size_1,
            self.pos[0],
            self.pos[0] + self.size[0],
            4,
            (255, 100, 100),
        )

    def __render_header(self):
        Draw.draw_rect(
            self.win(),
            self.pos,
            [self.__size[0], self.__HEADER_SIZE],
            BLOCK_TYPE_COLORS[self.__block_type],
        )
        # self.__block_name_text.draw(
        #    self.win(), [self.pos[0] + 5, self.pos[1]], text=self.__block_name
        # )
        self.win().blit(self.__block_name_text, [self.pos[0] + 5, self.pos[1]])

        if not self.__opened:
            Draw.draw_lines(
                self.win(),
                [
                    [self.pos[0] + self.__size[0] - 20, self.pos[1] + 8],
                    [self.pos[0] + self.__size[0] - 20 + 5, self.pos[1] + 4 + 10],
                    [self.pos[0] + self.__size[0] - 20 + 10, self.pos[1] + 8],
                ],
                "white",
                2,
            )
        else:
            Draw.draw_lines(
                self.win(),
                [
                    [self.pos[0] + self.__size[0] - 20, self.pos[1] + 4 + 10],
                    [self.pos[0] + self.__size[0] - 20 + 5, self.pos[1] + 8],
                    [self.pos[0] + self.__size[0] - 20 + 10, self.pos[1] + 4 + 10],
                ],
                "white",
                2,
            )

    def __render_moved(self):
        if self.__pressed:
            if self.__opened:
                Draw.draw_rect_fast(
                    self.win(),
                    [self.pos[0] - 5, self.pos[1] - 5],
                    [self.__size[0] + 10, self.__size[1] + 10],
                    color=Color((100, 100, 100)),
                )
            else:
                Draw.draw_rect_fast(
                    self.win(),
                    [self.pos[0] - 5, self.pos[1] - 5],
                    [self.__size[0] + 10, self.__HEADER_SIZE + 10],
                    color=Color((100, 100, 100)),
                )

    def Render(self):
        if self.__opened:
            Draw.draw_rect(self.win(), self.pos, self.__size, BlockBaseColor)

        self.__render_header()
        self.__render_moved()

    def Open_and_close(self):
        if not self.__o_c_pressed:
            if Mouse.press() and in_rect(
                self.pos, [self.__size[0], self.__HEADER_SIZE], Mouse.position()
            ):
                self.__o_c_pressed = True
                self.__opened = not self.__opened

        if not Mouse.press():
            self.__o_c_pressed = False

        if Mouse.press():
            self.__o_c_pressed = True

    def Move(self, speed):
        if self.__opened:
            if in_rect(self.pos, self.__size, Mouse.position()) and Mouse.click(
                Mouse.right
            ):
                self.__pressed = True
        else:
            if in_rect(
                self.pos, [self.__size[0], self.__HEADER_SIZE], Mouse.position()
            ) and Mouse.click(Mouse.right):
                self.__pressed = True

        if not Mouse.press(Mouse.right):
            self.__pressed = False

        if self.__pressed:
            if Keyboard.key_pressed("s"):
                if self.width_resized:
                    self.__size[0] += speed[0]
                    self.__size[0] = max(self.__size[0], self.start_size[0])
                if self.height_resized:
                    self.__size[1] += speed[1]
                    self.__size[1] = max(self.__size[1], self.start_size[1])
            else:
                self.pos[0] += speed[0]
                self.pos[1] += speed[1]

        self.speed[0] = self.pos[0] - self.end_pos[0]
        self.speed[1] = self.pos[1] - self.end_pos[1]

        self.end_pos = copy(self.pos)

        if Mouse.press(Mouse.middle):
            self.pos[0] += speed[0]
            self.pos[1] += speed[1]


# blocks classes -----------------------------------------------------


ENG = Engine(win)
SPC = Space(ENG)
UIUP = UpInterface(win)
SAVEWIN = SaveWindow(win, [220, 60])
OPENWIN = OpenWindow(win, [400, 500])


class Block_int:
    size = [60, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [60, 72], BlockType.NUMBER_TYPE, win, "int", ENG)
        self.socket_input = Point(
            self.bone, PointType.STRING_NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.buff_value = 0
        self.socket_output.value = self.buff_value
        self.socket_input.value = 0

        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input.pos,
                    [self.socket_input.pos[0] + 10, self.socket_input.pos[1] - 10],
                    [self.socket_input.pos[0] + 20, self.socket_input.pos[1]],
                    [self.socket_input.pos[0] + 60, self.socket_input.pos[1]],
                ],
                BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input.pos,
                    [self.socket_input.pos[0] + 10, self.socket_input.pos[1] + 10],
                    [self.socket_input.pos[0] + 20, self.socket_input.pos[1]],
                ],
                BLOCK_TYPE_COLORS[BlockType.STRING_TYPE],
                1,
            )
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value = int(self.socket_input.value)
        except:
            try:
                self.socket_output.value = int(float(self.socket_input.value))
            except:
                self.socket_output.value = None
                self.socket_error_output.value = {
                    "type": "Not mutable type!",
                    "error": True,
                }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_print:
    size = [80, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(
            pos, [80, 52], BlockType.FUNCTION_TYPE, win, "print", ENG, True
        )
        self.text_box = TextBox(self.bone, 1, 3)
        self.socket_input = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 1, ENG.points
        )

        ENG.points.append(self.socket_input)
        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.bone.opened:
            self.text_box.render()

        self.socket_input.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_input.update_pos()
        self.text_box.update_pos_and_size()

        self.text_box.text_value = self.socket_input.value

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_type:
    size = [70, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [70, 52], BlockType.FUNCTION_TYPE, win, "type", ENG)

        self.socket_input = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        self.socket_input.render()
        self.socket_output.render()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input.pos,
                    [self.socket_input.pos[0] + 30, self.socket_input.pos[1]],
                    [self.socket_input.pos[0] + 30, self.socket_input.pos[1] - 5],
                    [self.socket_input.pos[0] + 30, self.socket_input.pos[1] + 5],
                ],
                POINT_TYPE_COLORS[self.socket_input.point_type],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 35, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 35, self.socket_output.pos[1] - 5],
                    [self.socket_output.pos[0] - 35, self.socket_output.pos[1] + 5],
                ],
                BLOCK_TYPE_COLORS[BlockType.STRING_TYPE],
                1,
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_input.update_pos()
        self.socket_output.update_pos()

        self.socket_output.value = getClass(self.socket_input.value)

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_input:
    size = [80, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(
            pos, [80, 52], BlockType.FUNCTION_TYPE, win, "input", ENG, True
        )
        self.input_box = InputBox(self.bone, 1, 3)
        self.socket_output = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        ENG.points.append(self.socket_output)
        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.bone.opened:
            self.input_box.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_output.update_pos()
        self.input_box.update_pos_and_size()

        self.socket_output.value = self.input_box.input_text

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_number:
    size = [95, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(
            pos, [95, 72], BlockType.NUMBER_TYPE, win, "number", ENG, True
        )
        self.input_box = InputBox(self.bone, 1, 3)
        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )
        self.input_box.input_text = "0"

        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)
        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            self.input_box.render()
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )
        self.socket_error_output.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.input_box.update_pos_and_size()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value = int(self.input_box.input_text)
        except:
            try:
                self.socket_output.value = float(self.input_box.input_text)
            except:
                self.socket_output.value = 0
                self.socket_error_output.value = {
                    "type": "Don't converted type!",
                    "error": True,
                }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_math:
    size = [80, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [80, 72], BlockType.NUMBER_TYPE, win, "math", ENG)
        self.math_operations = DropDown(
            self.bone, 1, 3, ["+", "-", "*", "/", "**", "//"], 0
        )

        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_input_1 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )
        self.socket_input_1.value = 0
        self.socket_input_2.value = 0

        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_2.pos,
                    [self.socket_input_2.pos[0] + 20, self.socket_input_2.pos[1]],
                    [self.socket_input_2.pos[0] + 20, self.socket_input_2.pos[1] - 15],
                ],
                BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE].rgb,
                1,
            )

            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )
            self.math_operations.render()

        self.socket_error_output.render()
        self.socket_output.render()
        self.socket_input_2.render()
        self.socket_input_1.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.math_operations.update_pos_and_size()
        self.socket_output.update_pos()
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            if self.math_operations.values[self.math_operations.vabor_value] == "+":
                self.socket_output.value = (
                    self.socket_input_1.value + self.socket_input_2.value
                )
            if self.math_operations.values[self.math_operations.vabor_value] == "-":
                self.socket_output.value = (
                    self.socket_input_1.value - self.socket_input_2.value
                )
            if self.math_operations.values[self.math_operations.vabor_value] == "/":
                self.socket_output.value = (
                    self.socket_input_1.value / self.socket_input_2.value
                )
            if self.math_operations.values[self.math_operations.vabor_value] == "*":
                self.socket_output.value = (
                    self.socket_input_1.value * self.socket_input_2.value
                )
            if self.math_operations.values[self.math_operations.vabor_value] == "**":
                self.socket_output.value = (
                    self.socket_input_1.value**self.socket_input_2.value
                )
            if self.math_operations.values[self.math_operations.vabor_value] == "//":
                self.socket_output.value = (
                    self.socket_input_1.value // self.socket_input_2.value
                )
        except:
            self.socket_output.value = 0
            self.socket_error_output.value = {
                "type": "Not supported type!",
                "error": True,
            }
        if isinstance(self.socket_input_1.value, (int, float)) and isinstance(
            self.socket_input_1.value, (int, float)
        ):
            ...
        else:
            self.socket_error_output.value = {
                "type": "Not supported type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_abs:
    size = [60, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [60, 72], BlockType.NUMBER_TYPE, win, "abs", ENG)

        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_input = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )
        self.socket_input.value = 0

        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.bone.opened:
            Draw.draw_line(
                self.bone.win(),
                self.socket_input.pos,
                [self.socket_input.pos[0] + 25, self.socket_input.pos[1]],
                POINT_TYPE_COLORS[PointType.NUMBER_TYPE],
            )
            Draw.draw_circle(
                self.bone.win(),
                [self.socket_input.pos[0] + 30, self.socket_input.pos[1]],
                5,
                POINT_TYPE_COLORS[PointType.NUMBER_TYPE],
                1,
            )

            Draw.draw_line(
                self.bone.win(),
                self.socket_output.pos,
                [self.socket_output.pos[0] - 20, self.socket_output.pos[1]],
                POINT_TYPE_COLORS[PointType.NUMBER_TYPE],
            )

            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        if self.socket_error_output.value:
            self.bone.render_error()
        self.socket_error_output.render()
        self.socket_output.render()
        self.socket_input.render()

    def update(self, speed):
        self.socket_error_output.value = False
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_output.update_pos()
        self.socket_input.update_pos()
        self.socket_error_output.update_pos()

        try:
            self.socket_output.value = abs(self.socket_input.value)
        except:
            self.socket_output.value = 0
            self.socket_error_output.value = True

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_string:
    size = [80, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [80, 52], BlockType.STRING_TYPE, win, "string", ENG)
        self.socket_input = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        self.socket_input.render()
        self.socket_output.render()
        if self.bone.opened:
            Draw.draw_line(
                self.bone.win(),
                self.socket_input.pos,
                [self.socket_input.pos[0] + 45, self.socket_input.pos[1]],
                POINT_TYPE_COLORS[self.socket_input.point_type],
                1,
            )

            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] + 5],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] - 5],
                ],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )

            Draw.draw_line(
                self.bone.win(),
                [self.socket_output.pos[0] - 30, self.socket_output.pos[1] + 5],
                [self.socket_output.pos[0] - 50, self.socket_output.pos[1] + 5],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )

            Draw.draw_line(
                self.bone.win(),
                [self.socket_output.pos[0] - 30, self.socket_output.pos[1] - 5],
                [self.socket_output.pos[0] - 50, self.socket_output.pos[1] - 5],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_output.value = str(self.socket_input.value)

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_eval:
    size = [65, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [65, 72], BlockType.FUNCTION_TYPE, win, "eval", ENG)

        self.socket_input = Point(
            self.bone, PointType.STRING_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )
        self.socket_input.value = "0"

        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()
        if self.bone.opened:
            Draw.draw_line(
                self.bone.win(),
                self.socket_input.pos,
                [self.socket_input.pos[0] + 45, self.socket_input.pos[1]],
                POINT_TYPE_COLORS[self.socket_input.point_type],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] + 5],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] - 5],
                ],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )
            Draw.draw_line(
                self.bone.win(),
                [self.socket_output.pos[0] - 30, self.socket_output.pos[1] + 5],
                [self.socket_output.pos[0] - 50, self.socket_output.pos[1] + 5],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )
            Draw.draw_line(
                self.bone.win(),
                [self.socket_output.pos[0] - 30, self.socket_output.pos[1] - 5],
                [self.socket_output.pos[0] - 50, self.socket_output.pos[1] - 5],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )

            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        if self.socket_error_output.value:
            self.bone.render_error()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()

        self.socket_error_output.value = False
        try:
            self.socket_output.value = eval(self.socket_input.value)
        except:
            self.socket_output.value = None
            self.socket_error_output.value = True

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_error:
    size = [75, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [75, 72], BlockType.ERROR_TYPE, win, "error", ENG)
        self.socket_input = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.INPUT, 0.99, ENG.points
        )
        self.socket_output_1 = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_output_2 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = Text("arial", 15, "Error", (100, 100, 100), True)

        self.socket_input.value = {}

        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output_1)
        ENG.points.append(self.socket_output_2)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_input.render()
        self.socket_output_1.render()
        self.socket_output_2.render()
        if self.bone.opened:
            self.error_text.draw(
                self.bone.win(),
                [self.socket_output_2.pos[0] - 45, self.socket_output_2.pos[1] - 9],
                text="error",
                color=(150, 150, 150),
            )
            self.error_text.draw(
                self.bone.win(),
                [self.socket_output_1.pos[0] - 40, self.socket_output_1.pos[1] - 9],
                text="type",
                color=(150, 150, 150),
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output_1.update_pos()
        self.socket_output_2.update_pos()

        try:
            self.socket_output_1.value = self.socket_input.value["type"]
            self.socket_output_2.value = self.socket_input.value["error"]
        except:
            ...

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_equal:
    size = [80, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [80, 72], BlockType.BOOL_TYPE, win, "equal", ENG)

        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_input_1 = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 1, ENG.points
        )

        self.socket_input_2 = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 2.5, ENG.points
        )

        self.socket_input_1.value = 0
        self.socket_input_2.value = 0

        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.bone.opened:
            Draw.draw_hline(
                self.bone.win(),
                self.socket_input_1.pos[1],
                self.socket_input_1.pos[0],
                self.socket_output.pos[0],
                1,
                POINT_TYPE_COLORS[self.socket_input_1.point_type],
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_2.pos,
                    [self.socket_input_2.pos[0] + 40, self.socket_input_2.pos[1]],
                    [self.socket_input_2.pos[0] + 40, self.socket_input_2.pos[1] - 17],
                    [
                        self.socket_input_2.pos[0] + 40 - 10,
                        self.socket_input_2.pos[1] - 17,
                    ],
                    [
                        self.socket_input_2.pos[0] + 40 + 10,
                        self.socket_input_2.pos[1] - 17,
                    ],
                ],
                POINT_TYPE_COLORS[self.socket_input_2.point_type],
                1,
            )

        self.socket_output.render()
        self.socket_input_2.render()
        self.socket_input_1.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_output.update_pos()
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()

        try:
            self.socket_output.value = (
                self.socket_input_1.value == self.socket_input_2.value
            )
        except:
            self.socket_output.value = False

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_not:
    size = [60, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [60, 72], BlockType.BOOL_TYPE, win, "not", ENG)
        self.socket_input = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = False
        self.socket_input.value = True

        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input.pos,
                    [self.socket_input.pos[0] + 10, self.socket_input.pos[1]],
                    [self.socket_input.pos[0] + 10, self.socket_input.pos[1] + 5],
                    [self.socket_input.pos[0] + 40, self.socket_input.pos[1] + 5],
                ],
                POINT_TYPE_COLORS[self.socket_input.point_type],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 10, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 10, self.socket_output.pos[1] - 5],
                    [self.socket_output.pos[0] - 40, self.socket_output.pos[1] - 5],
                ],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if type(self.socket_input.value) == bool:
            self.socket_output.value = not self.socket_input.value
        else:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Bool type not detect!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_or:
    size = [55, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [55, 72], BlockType.BOOL_TYPE, win, "or", ENG)
        self.socket_input_1 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = False
        self.socket_input_1.value = False
        self.socket_input_2.value = False

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_1.pos,
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] + 10],
                    self.socket_input_2.pos,
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] + 10],
                    [self.socket_input_1.pos[0] + 35, self.socket_input_1.pos[1] + 10],
                    [self.socket_input_1.pos[0] + 35, self.socket_input_1.pos[1]],
                    self.socket_output.pos,
                ],
                POINT_TYPE_COLORS[PointType.BOOL_TYPE],
                1,
            )

            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if (
            type(self.socket_input_1.value) == bool
            and type(self.socket_input_2.value) == bool
        ):
            self.socket_output.value = (
                self.socket_input_1.value or self.socket_input_2.value
            )
        else:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Bool type not detect!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_and:
    size = [65, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [65, 72], BlockType.BOOL_TYPE, win, "and", ENG)
        self.socket_input_1 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = False
        self.socket_input_1.value = False
        self.socket_input_2.value = False

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_1.pos,
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] + 10],
                    self.socket_input_2.pos,
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] + 10],
                    [self.socket_input_1.pos[0] + 35, self.socket_input_1.pos[1] + 10],
                    [self.socket_input_1.pos[0] + 35, self.socket_input_1.pos[1]],
                    self.socket_output.pos,
                ],
                POINT_TYPE_COLORS[PointType.BOOL_TYPE],
                1,
            )
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if (
            type(self.socket_input_1.value) == bool
            and type(self.socket_input_2.value) == bool
        ):
            self.socket_output.value = (
                self.socket_input_1.value and self.socket_input_2.value
            )
        else:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Bool type not detect!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_slider_number:
    size = [145, 52]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(
            pos, [145, 72], BlockType.NUMBER_TYPE, win, "slider number", ENG, True
        )

        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_input_1 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )

        self.socket_input_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_input_1.value = 0
        self.socket_input_2.value = 10

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.value_slider = Slider(self.bone, 1, 5, -100, -50, 20)

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)
        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_1.pos,
                    [self.socket_input_1.pos[0] + 50, self.socket_input_1.pos[1]],
                ],
                POINT_TYPE_COLORS[PointType.NUMBER_TYPE],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_2.pos,
                    [self.socket_input_2.pos[0] + 80, self.socket_input_2.pos[1]],
                    [self.socket_input_2.pos[0] + 80, self.socket_input_2.pos[1] - 20],
                ],
                POINT_TYPE_COLORS[PointType.NUMBER_TYPE],
                1,
            )
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_output.render()
        self.value_slider.render()
        self.socket_input_2.render()
        self.socket_input_1.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()

        if isinstance(self.socket_input_1.value, (int, float)):
            self.value_slider.min = self.socket_input_1.value
        else:
            self.value_slider.min = 0
        if isinstance(self.socket_input_2.value, (int, float)):
            self.value_slider.max = self.socket_input_2.value
        else:
            self.value_slider.max = 0

        self.value_slider.update_pos_and_size(20)
        self.socket_error_output.value = {"type": None, "error": False}

        self.socket_output.value = self.value_slider.value

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_upper:
    size = [80, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [80, 72], BlockType.STRING_TYPE, win, "upper", ENG)
        self.socket_input = Point(
            self.bone, PointType.STRING_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = ""
        self.socket_input.value = ""
        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value: str = self.socket_input.value.upper()
        except:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Not string type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_lower:
    size = [75, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [75, 72], BlockType.STRING_TYPE, win, "lower", ENG)
        self.socket_input = Point(
            self.bone, PointType.STRING_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.STRING_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = ""
        self.socket_input.value = ""
        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value: str = self.socket_input.value.lower()
        except:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Not string type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_split:
    size = [65, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [65, 72], BlockType.STRING_TYPE, win, "split", ENG)
        self.socket_input_1 = Point(
            self.bone, PointType.STRING_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.STRING_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.LIST_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = []
        self.socket_input_1.value = " "
        self.socket_input_2.value = " "
        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_1.pos,
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1]],
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] + 6],
                    [self.socket_input_1.pos[0] + 20, self.socket_input_1.pos[1] - 6],
                ],
                POINT_TYPE_COLORS[self.socket_input_1.point_type],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_input_2.pos,
                    [self.socket_input_2.pos[0] + 28, self.socket_input_2.pos[1]],
                    [self.socket_input_2.pos[0] + 28, self.socket_input_2.pos[1] - 30],
                ],
                POINT_TYPE_COLORS[self.socket_input_2.point_type],
                1,
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] + 6],
                    [self.socket_output.pos[0] - 30, self.socket_output.pos[1] - 6],
                ],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value: str = self.socket_input_1.value.split(
                self.socket_input_2.value
            )
        except:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Not string type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_get:
    size = [60, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [60, 72], BlockType.LIST_TYPE, win, "get", ENG)
        self.socket_input_1 = Point(
            self.bone, PointType.STRING_LIST_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.ANY_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = False
        self.socket_input_1.value = False
        self.socket_input_2.value = False

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if (
            type(self.socket_input_1.value) == list
            or type(self.socket_input_1.value) == str
        ) and type(self.socket_input_2.value) == int:
            try:
                self.socket_output.value = self.socket_input_1.value[
                    self.socket_input_2.value
                ]
            except:
                self.socket_output.value = False
                self.socket_error_output.value = {
                    "type": "Index not define!",
                    "error": True,
                }

        else:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Non iterable type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_len:
    size = [60, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [60, 72], BlockType.FUNCTION_TYPE, win, "len", ENG)
        self.socket_input = Point(
            self.bone, PointType.STRING_LIST_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = ""
        self.socket_input.value = []
        ENG.points.append(self.socket_input)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_input.render()
        self.socket_output.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            self.socket_output.value: str = len(self.socket_input.value)
        except:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Non itarable type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_index:
    size = [75, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [75, 72], BlockType.LIST_TYPE, win, "index", ENG)

        self.socket_input_1 = Point(
            self.bone, PointType.STRING_LIST_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = False
        self.socket_input_1.value = False
        self.socket_input_2.value = False

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if (
            type(self.socket_input_1.value) == list
            or type(self.socket_input_1.value) == str
        ):
            try:
                self.socket_output.value = self.socket_input_1.value.index(
                    self.socket_input_2.value
                )
            except:
                self.socket_output.value = None
                self.socket_error_output.value = {
                    "type": "Element not define!",
                    "error": True,
                }

        else:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Non iterable type!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_color:
    size = [105, 122]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(
            pos, [105, 122], BlockType.FUNCTION_TYPE, win, "color", ENG
        )

        self.socket_input_1 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_input_3 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 4, ENG.points
        )
        self.value_slider_1 = Slider(self.bone, 1, 5, 255, 0, 20)
        self.value_slider_2 = Slider(self.bone, 2.5, 5, 255, 0, 20)
        self.value_slider_3 = Slider(self.bone, 4, 5, 255, 0, 20)

        self.socket_output = Point(
            self.bone, PointType.LIST_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 5.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = [0, 0, 0]
        self.socket_input_1.value = 0
        self.socket_input_2.value = 0
        self.socket_input_3.value = 0

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_input_3)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_input_3.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            Draw.draw_rect(self.bone.win(), [self.bone.pos[0]+5,self.bone.pos[1]+97],[self.bone.size[0]-35,20],(self.value_slider_1.value,self.value_slider_2.value,self.value_slider_3.value))
            Draw.draw_hline(
                self.bone.win(),
                self.socket_input_1.pos[1],
                self.socket_input_1.pos[0] + 70,
                self.socket_input_1.pos[0] + 90,
                1,
                POINT_TYPE_COLORS[self.socket_input_1.point_type],
            )
            Draw.draw_hline(
                self.bone.win(),
                self.socket_input_2.pos[1],
                self.socket_input_2.pos[0] + 70,
                self.socket_input_2.pos[0] + 90,
                1,
                POINT_TYPE_COLORS[self.socket_input_1.point_type],
            )
            Draw.draw_hline(
                self.bone.win(),
                self.socket_input_3.pos[1],
                self.socket_input_3.pos[0] + 70,
                self.socket_input_3.pos[0] + 90,
                1,
                POINT_TYPE_COLORS[self.socket_input_1.point_type],
            )
            Draw.draw_lines(
                self.bone.win(),
                [
                    self.socket_output.pos,
                    [self.socket_output.pos[0] - 15, self.socket_output.pos[1]],
                    [self.socket_output.pos[0] - 15, self.socket_output.pos[1] + 48],
                ],
                POINT_TYPE_COLORS[self.socket_output.point_type],
                1,
            )
            self.value_slider_3.render()
            self.value_slider_2.render()
            self.value_slider_1.render()
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_input_3.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.value_slider_1.update_pos_and_size(0, 20)
        self.value_slider_2.update_pos_and_size(0, 20)
        self.value_slider_3.update_pos_and_size(0, 20)
        self.socket_error_output.value = {"type": None, "error": False}

        try:
            self.socket_output.value = [
                self.value_slider_1.value,
                self.value_slider_2.value,
                self.value_slider_3.value,
            ]
        except:
            self.socket_output.value = None
            self.socket_error_output.value = {
                "type": "Element not define!",
                "error": True,
            }

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_circle:
    size = [85, 122]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(
            pos, [85, 122], BlockType.RENDER_TYPE, win, "circle", ENG
        )

        self.socket_input_1 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_input_3 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.INPUT, 4, ENG.points
        )
        self.socket_input_4 = Point(
            self.bone, PointType.LIST_TYPE, SocketType.INPUT, 5.5, ENG.points
        )



        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 5.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.text = Text("arial", 15, "Error", (100, 100, 100), True)

        self.socket_input_1.value = 0
        self.socket_input_2.value = 0
        self.socket_input_3.value = 0
        self.socket_input_4.value = 0

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_input_3)
        ENG.points.append(self.socket_input_4)

        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_input_3.render()
        self.socket_input_4.render()


        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            
            self.text.draw(
                self.bone.win(),
                [self.socket_input_1.pos[0]+10, self.socket_input_1.pos[1] - 9],
                text="x",
                color=(150, 150, 150),
            )
            self.text.draw(
                self.bone.win(),
                [self.socket_input_2.pos[0] +10, self.socket_input_2.pos[1] - 9],
                text="y",
                color=(150, 150, 150),
            )
            self.text.draw(
                self.bone.win(),
                [self.socket_input_3.pos[0] +10, self.socket_input_3.pos[1] - 9],
                text="rad",
                color=(150, 150, 150),
            )
            self.text.draw(
                self.bone.win(),
                [self.socket_input_4.pos[0] +10, self.socket_input_4.pos[1] - 9],
                text="color",
                color=(150, 150, 150),
            )
            
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_input_3.update_pos()
        self.socket_input_4.update_pos()

        self.socket_error_output.update_pos()

        self.socket_error_output.value = {"type": None, "error": False}

    def render_data(self):
        try:
            Draw.draw_circle(self.bone.win(),[self.socket_input_1.value,self.socket_input_2.value], self.socket_input_3.value, self.socket_input_4.value)
        except:...

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt


class Block_mouse_pos:
    size = [120, 100]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [120, 100], BlockType.FUNCTION_TYPE, win, "mouse pos", ENG)
        self.socket_output_1 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 1, ENG.points
        )
        self.socket_output_2 = Point(
            self.bone, PointType.NUMBER_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 4, ENG.points
        )
        
        self.text = Text("arial", 15, "Error", (100, 100, 100), True)
        
        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )


        self.socket_output_1.value = 0
        self.socket_output_2.value = 0

        ENG.points.append(self.socket_output_1)
        ENG.points.append(self.socket_output_2)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            
            self.text.draw(
                self.bone.win(),
                [self.socket_output_1.pos[0] - 20, self.socket_output_1.pos[1] - 9],
                text="x",
                color=(150, 150, 150),
            )
            self.text.draw(
                self.bone.win(),
                [self.socket_output_2.pos[0] - 20, self.socket_output_2.pos[1] - 9],
                text="y",
                color=(150, 150, 150),
            )
            
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

        self.socket_error_output.render()
        self.socket_output_2.render()
        self.socket_output_1.render()

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_output_1.update_pos()
        self.socket_output_2.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        self.socket_output_1.value = Mouse.position()[0]
        self.socket_output_2.value = Mouse.position()[1]

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt
    

class Block_buffer:
    size = [80, 72]

    def __init__(self, pos: list) -> None:
        self.bone = _BoneBlock(pos, [80, 72], BlockType.FUNCTION_TYPE, win, "buffer", ENG)

        self.socket_input_1 = Point(
            self.bone, PointType.ANY_TYPE, SocketType.INPUT, 1, ENG.points
        )
        self.socket_input_2 = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.INPUT, 2.5, ENG.points
        )
        self.socket_output = Point(
            self.bone, PointType.ANY_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )

        self.socket_output.value = None
        self.socket_input_1.value = None
        self.socket_input_2.value = False

        ENG.points.append(self.socket_input_1)
        ENG.points.append(self.socket_input_2)
        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)
        
        self.buffer = None

    def render(self):
        self.bone.Render()

        self.socket_error_output.render()
        self.socket_input_1.render()
        self.socket_input_2.render()
        self.socket_output.render()

        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:
            ...
            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )

    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)
        self.socket_input_1.update_pos()
        self.socket_input_2.update_pos()
        self.socket_output.update_pos()
        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        if self.socket_input_2.value:
            self.buffer = self.socket_input_1.value
            
        self.socket_output.value = self.buffer

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt
    

class Block_bool:
    size = [70, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [70, 72], BlockType.BOOL_TYPE, win, "bool", ENG)
        self.math_operations = DropDown(
            self.bone, 1, 3, ["True", "False"], 0
        )

        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )


        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:


            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )
            self.math_operations.render()

        self.socket_error_output.render()
        self.socket_output.render()


    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.math_operations.update_pos_and_size()
        self.socket_output.update_pos()

        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            if self.math_operations.values[self.math_operations.vabor_value] == "True":
                self.socket_output.value = True
            if self.math_operations.values[self.math_operations.vabor_value] == "False":
                self.socket_output.value = False
                
            
        except:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Not supported type!",
                "error": True,
            }
        

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt
    
    
class Block_press:
    size = [75, 72]

    def __init__(self, pos) -> None:
        self.bone = _BoneBlock(pos, [75, 72], BlockType.FUNCTION_TYPE, win, "press", ENG)
        self.math_operations = DropDown(
            self.bone, 1, 3, ["left", "right",'middle'], 0
        )

        self.socket_output = Point(
            self.bone, PointType.BOOL_TYPE, SocketType.OUTPUT, 1, ENG.points
        )

        self.socket_error_output = Point(
            self.bone, PointType.ERROR_TYPE, SocketType.OUTPUT, 2.5, ENG.points
        )

        self.error_text = (
            Text("arial", 15, "Error", (255, 100, 100), True)
            .render("err", (250, 100, 100))
            ._surface
        )


        ENG.points.append(self.socket_output)
        ENG.points.append(self.socket_error_output)

        SPC.blocks.append(self)

    def render(self):
        self.bone.Render()
        if self.socket_error_output.value["error"]:
            self.bone.render_error()
        if self.bone.opened:


            self.bone.win().blit(
                self.error_text,
                [
                    self.socket_error_output.pos[0] - 27,
                    self.socket_error_output.pos[1] - 9,
                ],
            )
            self.math_operations.render()

        self.socket_error_output.render()
        self.socket_output.render()


    def update(self, speed):
        self.bone.Open_and_close()
        self.bone.Move(speed)

        self.math_operations.update_pos_and_size()
        self.socket_output.update_pos()

        self.socket_error_output.update_pos()
        self.socket_error_output.value = {"type": None, "error": False}
        try:
            if self.math_operations.values[self.math_operations.vabor_value] == "left":
                self.socket_output.value = Mouse.press(Mouse.left)
            if self.math_operations.values[self.math_operations.vabor_value] == "right":
                self.socket_output.value = Mouse.press(Mouse.right)
            if self.math_operations.values[self.math_operations.vabor_value] == "middle":
                self.socket_output.value = Mouse.press(Mouse.middle)
                
            
        except:
            self.socket_output.value = False
            self.socket_error_output.value = {
                "type": "Not supported type!",
                "error": True,
            }
        

    def set_points(self, point_name, id, conects=[], connect=None, pt=None):
        point: Point = self.__getattribute__(point_name)
        point.id = id
        point.my_con_points_ids = conects
        point.connectpoint_id = connect
        point.point_type = pt
        
        
AllBlocks = {
    "int": Block_int,
    "string": Block_string,
    "type": Block_type,
    "eval": Block_eval,
    "error": Block_error,
    "math": Block_math,
    "print": Block_print,
    "input": Block_input,
    "abs": Block_abs,
    "equal": Block_equal,
    "not": Block_not,
    "or": Block_or,
    "and": Block_and,
    "number": Block_number,
    "slider number": Block_slider_number,
    "upper": Block_upper,
    "lower": Block_lower,
    "get": Block_get,
    "len": Block_len,
    "split": Block_split,
    "index": Block_index,
    "color": Block_color,
    'circle':Block_circle,
    'mouse pos':Block_mouse_pos,
    'buffer':Block_buffer,
    'bool':Block_bool,
    'press':Block_press
}

AllSpawnBlocks = {
    "int": [Block_int, BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
    "string": [Block_string, BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]],
    "type": [Block_type, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    "eval": [Block_eval, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    "error": [Block_error, BLOCK_TYPE_COLORS[BlockType.ERROR_TYPE]],
    "math": [Block_math, BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
    "print": [Block_print, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    "input": [Block_input, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    "abs": [Block_abs, BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
    "equal": [Block_equal, BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
    "not": [Block_not, BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
    "or": [Block_or, BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
    "and": [Block_and, BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
    "number": [Block_number, BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
    "slider number": [Block_slider_number, BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
    "upper": [Block_upper, BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]],
    "lower": [Block_lower, BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]],
    "get": [Block_get, BLOCK_TYPE_COLORS[BlockType.LIST_TYPE]],
    "len": [Block_len, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    "split": [Block_split, BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]],
    "index": [Block_index, BLOCK_TYPE_COLORS[BlockType.LIST_TYPE]],
    "color": [Block_color, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    'circle':[Block_circle, BLOCK_TYPE_COLORS[BlockType.RENDER_TYPE]],
    'mouse pos':[Block_mouse_pos, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    'buffer':[Block_buffer, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
    'bool':[Block_bool,BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
    'press':[Block_press, BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]]
}


class LeftInterface:
    def __init__(self, win, blocks) -> None:
        self.win = win
        self.blocks = blocks
        self.w = 300

        self.NUMBERS = []
        self.STRINGS = []
        self.FUNCTIONS = []
        self.ERRORS = []
        self.BOOLS = []
        self.LISTS = []
        self.RENDERS = []

        self.types_buttons = [
            ["NUMBERS", BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]],
            ["STRINGS", BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]],
            ["FUNCTIONS", BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]],
            ["ERRORS", BLOCK_TYPE_COLORS[BlockType.ERROR_TYPE]],
            ["BOOLS", BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]],
            ["LISTS", BLOCK_TYPE_COLORS[BlockType.LIST_TYPE]],
            ["RENDERS", BLOCK_TYPE_COLORS[BlockType.RENDER_TYPE]]
        ]
        self.vabor = "NUMBERS"
        self.construct()

    def construct(self):
        for name in self.blocks:
            name_texts = Text("arial", 17, name, (200, 200, 200), bold=True)
            s = name_texts.render(name, (200, 200, 200))._surface
            s
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.NUMBER_TYPE]:
                self.NUMBERS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.FUNCTION_TYPE]:
                self.FUNCTIONS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.STRING_TYPE]:
                self.STRINGS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.ERROR_TYPE]:
                self.ERRORS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.BOOL_TYPE]:
                self.BOOLS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.LIST_TYPE]:
                self.LISTS.append([s, self.blocks[name]])
            if self.blocks[name][1] == BLOCK_TYPE_COLORS[BlockType.RENDER_TYPE]:
                self.RENDERS.append([s, self.blocks[name]])

    def render(self):
        Draw.draw_rect(
            self.win(), [0, 20], [self.w, self.win.get_size[0]], (100, 100, 100)
        )
        Draw.draw_rect(self.win(), [0, 20], [50, self.win.get_size[0]], (80, 80, 80))
        for i, tpb in enumerate(self.types_buttons):
            Draw.draw_rect(self.win(), [0, 20 + 50 * i], [50], (80, 80, 80))
            if in_rect([0, 20 + 50 * i], [50, 50], Mouse.position()):
                Draw.draw_rect(self.win(), [0, 20 + 50 * i], [50], (100, 100, 100))
            if Mouse.press():
                if in_rect([0, 20 + 50 * i], [50, 50], Mouse.position()):
                    self.vabor = tpb[0]
            if tpb[0] == self.vabor:
                Draw.draw_rect(self.win(), [0, 20 + 50 * i], [50], (100, 100, 100))

            Draw.draw_circle(self.win(), [0 + 25, 20 + 50 * i + 25], 10, tpb[1])

        if self.vabor == "NUMBERS":
            BLOCKS = self.NUMBERS
        elif self.vabor == "STRINGS":
            BLOCKS = self.STRINGS
        elif self.vabor == "FUNCTIONS":
            BLOCKS = self.FUNCTIONS
        elif self.vabor == "ERRORS":
            BLOCKS = self.ERRORS
        elif self.vabor == "BOOLS":
            BLOCKS = self.BOOLS
        elif self.vabor == "LISTS":
            BLOCKS = self.LISTS
        elif self.vabor == "RENDERS":
            BLOCKS = self.RENDERS

        for i, block in enumerate(BLOCKS):
            # print(block[1])
            if in_rect([60, 30 + i * 30], [240, 30], Mouse.position()):
                Draw.draw_rect(
                    self.win(),
                    [60 - 5, 30 + i * 30 - 5],
                    [230 + 10, 20 + 10],
                    block[1][1],
                )
                if Mouse.click(Mouse.right):
                    b: Block_not = block[1][0](
                        [Mouse.position()[0] - 30, Mouse.position()[1] - 30]
                    )
                    b.bone.pressed = True

            Draw.draw_rect(
                self.win(),
                [60, 30 + i * 30],
                [block[1][0].size[0], 20],
                block[1][1],
            )

            self.win().blit(block[0], [65, 30 + i * 30])


UILEFT = LeftInterface(win, AllSpawnBlocks)

# for i in range(10):
#    for j in range(10):
#        Block_color([i * 50, j * 50])


while win.update(fps="max", base_color=(70,70,70), fps_view=0):
    speed = Mouse.speed
    SPC.Update()

    # jENG.render_points()
    ENG.update_points()
    ENG.render_points_type()
    UIUP.render()
    UILEFT.render()
    SAVEWIN.render()
    OPENWIN.render(SPC)

    ENG.RenderMouse()

    if UIUP.bt_SAVEFILE.press and not OPENWIN.view:
        SAVEWIN.pos = center_rect(win.center, SAVEWIN.size, 1)
        SAVEWIN.view = True
    if UIUP.bt_OPENFILE.press and not SAVEWIN.view:
        OPENWIN.pos = center_rect(win.center, OPENWIN.size, 1)
        OPENWIN.get_files()
        OPENWIN.view = True

    if SAVEWIN.save_bt.press:
        if ".json" in SAVEWIN.input_box.input_text:
            save(SAVEWIN.input_box.input_text, SPC.blocks)
            SAVEWIN.error = False

        else:
            SAVEWIN.error = True
    # if Keyboard.key_pressed("l"):
    #    SPC.load("save.json")
