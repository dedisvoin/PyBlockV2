from library.liball import *
from settings import DX_VAL


class PointType:
    NUMBER_TYPE: str = "NUMBER_TYPE"
    STRING_TYPE: str = "STRING_TYPE"
    ANY_TYPE: str = "ANY_TYPE"
    STRING_NUMBER_TYPE: str = "STRING_NUMBER_TYPE"
    STRING_LIST_TYPE: str = "STRING_LIST_TYPE"
    ERROR_TYPE: str = "ERROR_TYPE"
    BOOL_TYPE: str = "BOOL_TYPE"
    LIST_TYPE: str = "LIST_TYPE"


class SocketType:
    INPUT: str = "INPUT"
    OUTPUT: str = "OUTPUT"


POINT_TYPE_COLORS = {
    PointType.NUMBER_TYPE: Color([100, 100, 250]),
    PointType.STRING_TYPE: Color([250, 140, 100]),
    PointType.ANY_TYPE: Color([150, 150, 150]),
    PointType.STRING_NUMBER_TYPE: [Color([250, 140, 100]), Color([100, 100, 250])],
    PointType.STRING_LIST_TYPE: [Color([250, 140, 100]), Color((200, 100, 200))],
    PointType.ERROR_TYPE: Color((255, 100, 100)),
    PointType.BOOL_TYPE: Color((100, 160, 160)),
    PointType.LIST_TYPE: Color((200, 100, 200)),
}

PointType_ = NewType("BlockType", str)


class Point:
    def __init__(
        self,
        Block_,
        Point_Type_: PointType_,
        Socket_type_: str,
        dx_=1,
        any_points: list = [],
    ) -> "Point":
        self.__block = Block_
        self.__point_type = Point_Type_
        self.__start_type = copy(Point_Type_)
        self.__id = id_generate(8)
        self.__block_id = Block_.id

        self.__socket_type = Socket_type_
        self.pos = [0, 0]
        self.__dx = dx_
        self.any_points = any_points

        self.win = self.__block.win

        self.mouse_celing = False
        self.mouse_pressed = False

        self.connected = False
        self.connectpoint_id = None
        self.my_con_points_ids = []

        self.value = None
        self.error = False
        self.points_data_text = Text("arial", 15, color="black", bold=True)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def block_id(self):
        return self.__block_id

    @property
    def point_type(self):
        return self.__point_type

    @property
    def socket_type(self):
        return self.__socket_type

    @property
    def start_point_type(self):
        return self.__start_type

    @point_type.setter
    def point_type(self, type):
        self.__point_type = type

    def bezier_points_form(self, pos1: list, pos2: list):
        center_point = center_pos(pos1, pos2)
        left_point = [center_point[0], pos1[1]]
        left_point[0] = max(pos1[0] + 50, left_point[0])
        left_p = [left_point[0], center_point[1]]
        right_point = [center_point[0], pos2[1]]
        right_point[0] = min(pos2[0] - 50, right_point[0])
        right_p = [right_point[0], center_point[1]]
        return [pos1, left_point, left_p, center_point, right_p, right_point, pos2]

    def update_pos(self):
        if self.__socket_type == SocketType.INPUT:
            self.pos[0] = self.__block.pos[0]
        if self.__socket_type == SocketType.OUTPUT:
            self.pos[0] = self.__block.pos[0] + self.__block.size[0]

        self.pos[1] = (
            self.__block.pos[1] + self.__block.HEADER_SIZE + self.__dx * DX_VAL
        )
        if not self.__block.opened:
            self.pos[1] = self.__block.pos[1] + self.__block.HEADER_SIZE / 2

    def render_data(self):
        if self.mouse_celing:
            if not isinstance(POINT_TYPE_COLORS[self.__point_type], list):
                text_surf = self.points_data_text.render(
                    f"{self.__point_type}", POINT_TYPE_COLORS[self.__point_type].rgb
                )

                pos = copy(self.pos)
                pos[1] -= 50

                if self.socket_type == SocketType.INPUT:
                    pos[0] -= text_surf._surface.get_width() + 30
                    Draw.draw_lines(
                        self.win(),
                        [
                            self.pos,
                            [
                                pos[0] + text_surf._surface.get_width(),
                                pos[1] + text_surf._surface.get_height() + 2,
                            ],
                            [
                                pos[0],
                                pos[1] + text_surf._surface.get_height() + 2,
                            ],
                        ],
                        POINT_TYPE_COLORS[self.__point_type],
                        1,
                    )
                elif self.socket_type == SocketType.OUTPUT:
                    pos[0] += 30
                    Draw.draw_lines(
                        self.win(),
                        [
                            self.pos,
                            [pos[0], pos[1] + text_surf._surface.get_height() + 2],
                            [
                                pos[0] + text_surf._surface.get_width(),
                                pos[1] + text_surf._surface.get_height() + 2,
                            ],
                        ],
                        POINT_TYPE_COLORS[self.__point_type],
                        1,
                    )
                # self.win().blit(text_surf_white._surface, [pos[0] + 1, pos[1] + 1])
                self.win().blit(text_surf._surface, pos)

    def render(self):
        if self.mouse_pressed:
            Draw.draw_bezier(
                self.win(),
                self.bezier_points_form(self.pos, Mouse.position()),
                2,
                POINT_TYPE_COLORS[self.__point_type],
            )
            # Draw.draw_lines(
            #    self.win(),
            #    self.bezier_points_form(self.__pos, Mouse.position),
            #    "black",
            #    1,
            # )
        if len(self.my_con_points_ids) != 0:
            for id in self.my_con_points_ids:
                for point in self.any_points:
                    if point.id == id:
                        Draw.draw_bezier(
                            self.win(),
                            self.bezier_points_form(self.pos, point.pos),
                            2,
                            POINT_TYPE_COLORS[self.__point_type],
                            2,
                        )

                        point.value = self.value

        if isinstance(POINT_TYPE_COLORS[self.__point_type], list):
            Draw.draw_arc(
                self.win(),
                self.pos,
                POINT_TYPE_COLORS[self.__point_type][0],
                90,
                270,
                5,
                5,
                7,
            )
            Draw.draw_arc(
                self.win(),
                self.pos,
                POINT_TYPE_COLORS[self.__point_type][1],
                -90,
                -270,
                5,
                5,
                7,
            )
            if self.mouse_celing:
                Draw.draw_arc(
                    self.win(),
                    self.pos,
                    POINT_TYPE_COLORS[self.__point_type][0],
                    90,
                    270,
                    10,
                    1,
                    7,
                )
                Draw.draw_arc(
                    self.win(),
                    self.pos,
                    POINT_TYPE_COLORS[self.__point_type][1],
                    -90,
                    -270,
                    10,
                    1,
                    7,
                )
        else:
            if self.__point_type == PointType.ERROR_TYPE:
                Draw.draw_polygone(
                    self.win(),
                    [
                        [self.pos[0] + 4, self.pos[1]],
                        [self.pos[0] - 4, self.pos[1] - 4],
                        [self.pos[0] - 4, self.pos[1] + 4],
                    ],
                    POINT_TYPE_COLORS[self.__point_type],
                )
                if self.mouse_celing:
                    Draw.draw_polygone(
                        self.win(),
                        [
                            [self.pos[0] + 13, self.pos[1]],
                            [self.pos[0] - 8, self.pos[1] - 10],
                            [self.pos[0] - 8, self.pos[1] + 10],
                        ],
                        POINT_TYPE_COLORS[self.__point_type],
                        1,
                    )
            else:
                Draw.draw_circle(
                    self.win(), self.pos, 5, POINT_TYPE_COLORS[self.__point_type]
                )
                if self.mouse_celing:
                    Draw.draw_circle(
                        self.win(),
                        self.pos,
                        10,
                        POINT_TYPE_COLORS[self.__point_type],
                        1,
                    )

        if self.error:
            Draw.draw_circle(self.win(), self.pos, 10, "red", 2)

    def update(self):
        self.error = False
        # errors ----------------------------------------------------
        if self.value != None:
            if self.__start_type == PointType.ANY_TYPE:
                self.error = False

            if self.__start_type == PointType.NUMBER_TYPE:
                if isinstance(self.value, (int, float)) == True:
                    self.error = False
                else:
                    self.error = True

            if self.__start_type == PointType.STRING_TYPE:
                if isinstance(self.value, (str)) == True:
                    self.error = False
                else:
                    self.error = True

        # errors ----------------------------------------------------

        if distance(self.pos, Mouse.position()) < 6:
            self.mouse_celing = True
        else:
            self.mouse_celing = False
        # if self.connectpoint_id == None and self.__point_type != self.__start_type:
        #    self.__point_type = self.__start_type
        # all_ids = list(map(lambda elem: elem.__id, self.any_points))

        if self.mouse_celing:
            if self.__socket_type == SocketType.OUTPUT:
                if Mouse.press():
                    self.mouse_pressed = True

        if not Mouse.press():
            self.mouse_pressed = False

        if self.mouse_pressed:
            if self.__socket_type == SocketType.OUTPUT:
                for point in self.any_points:
                    if distance(Mouse.position(), point.pos) < 6:
                        if (
                            self.__id != point.id
                            and self.__block_id != point.block_id
                            and point.socket_type == SocketType.INPUT
                            and point.connectpoint_id == None
                        ):
                            self.my_con_points_ids.append(point.id)
                            point.connectpoint_id = self.id
                            point.__point_type = self.__point_type

                            self.mouse_pressed = False
                            break

        if (
            self.__socket_type == SocketType.INPUT
            and distance(self.pos, Mouse.position()) < 6
        ):
            if Mouse.click(Mouse.right):
                for point in self.any_points:
                    if (
                        self.__id != point.id
                        and self.__block_id != point.block_id
                        and point.socket_type == SocketType.OUTPUT
                    ):
                        if self.__id in point.my_con_points_ids:
                            point.my_con_points_ids.remove(self.__id)

                            self.connectpoint_id = None
                            self.__point_type = self.__start_type
                            self.value = None
