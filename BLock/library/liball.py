from library.Lowlevelib import *
from library.libtypes import *
from library.libgfx import *
from library.libui import *
from .collidelib import *


from typing import overload
from typing import Tuple




class SpriteStack:
    def __init__(
        self, sprite_slices_file_name_: str, size_: Tuple[int, int], scale_: int = 1
    ) -> None:
        self.load_slices = pygame.image.load(sprite_slices_file_name_)
        self._size = size_
        self.object_pos = []
        self._pos = []
        self._scale = scale_

    def convert(self, angles_count=180, zapl=False):
        height = self.load_slices.get_height()
        self.converted_sprites = []
        self.angle_dur = 360 / angles_count

        for angle in range(angles_count):
            pre_surfs: list[pygame.Surface] = []
            for i in range(height // self._size[1]):
                sp = self.load_slices.subsurface(
                    [0, 0 + i * self._size[1]], [self._size[0], self._size[1]]
                )
                sp = pygame.transform.scale(
                    sp, [sp.get_width() * self._scale, sp.get_height() * self._scale]
                )
                sub_surf = pygame.transform.rotate(
                    sp,
                    angle * self.angle_dur,
                )
                pre_surfs.append(sub_surf)
            pre_surfs.reverse()
            surf_size = [
                pre_surfs[0].get_width(),
                pre_surfs[0].get_height() + i * self._scale,
            ]
            dummy_surf = pygame.Surface(surf_size).convert_alpha()
            dummy_surf.set_colorkey((0, 0, 0))
            for i, image in enumerate(pre_surfs):
                for k in range(int(self._scale)):
                    dummy_surf.blit(
                        image,
                        [
                            0,
                            dummy_surf.get_height()
                            - image.get_height()
                            - i * self._scale
                            - k,
                        ],
                    )
            self.converted_sprites.append(dummy_surf)

    def set_pos(self, pos):
        self._pos = copy(pos)

        self._pos[1] -= self._size[2] * self._scale / 2

    def render(self, surf: pygame.Surface, angle):
        sprite = self.converted_sprites[int((angle % 360) // self.angle_dur)]

        surf.blit(
            sprite,
            [
                self._pos[0] - sprite.get_width() / 2,
                self._pos[1] - sprite.get_height() / 2,
            ],
        )

        Draw.draw_circle(surf, self._pos, 2, "blue")
