from library.Lowlevelib import AnimatedSprite
from library.Lowlevelib import Vector2
from library.Lowlevelib import Sprite
from library.Lowlevelib import Window
from library.Lowlevelib import Color
from library.Lowlevelib import Draw
from library.collidelib import *



from dataclasses import dataclass
from typing import Self, Tuple
from typing import NewType
from random import randint
from random import choice
from copy import copy
from math import sin

ParticleColor_ = NewType("ParticleColor", [str | Tuple[int, int, int] | Color])


@dataclass
class Shapes:
    RECT = "rect_shape"
    CIRCLE = "circle_shape"
    IMAGE = "image_shape"
    ANIMATE = "animate_shape"


@dataclass
class SpriteModes:
    VECTOR = "vector_mode"
    ROTATE = "rotate_mode"


@dataclass
class SpavnerTypes:
    RECT_SPAVNER = "rect_spavner"
    CIRCLE_SPAVNER = "circle_spavner"
    LINE_SPAVNER = "line_spavner"


class _particle:
    particle_shape: Shapes = Shapes.CIRCLE
    particle_color: str | Color | Tuple[int, int, int] = "black"
    particle_radius: float = 1
    particle_radius_randoming: float = 0
    particle_size: Tuple[float, float] = [1, 1]
    particle_pos: Tuple[float, float] = [0, 0]
    particle_speed: float = 1
    particle_move_angle: float = 0
    particle_move_duration: float = 0
    particle_speed_rotation: float = 0
    particle_move_adding: float = 1
    particle_sinusing: float = 0
    particle_sinusing_amplitude: float = 0
    particle_choise_color: bool = False
    particle_sprite: Sprite = None
    particle_sprite_mode: SpriteModes = SpriteModes.VECTOR
    particle_sprite_rotate_angle: float = 0
    particle_sprite_scale: float = 1
    particle_sprite_sum_angle: float = 0
    particle_speed_randoming: int = 0

    particle_size_deller: float = 0.1
    particle_animation: AnimatedSprite = None
    
    particle_phisics: bool = False
    particle_phisics_trenie: Vector2 = Vector2(0.5,0.5)
    particle_phisics_gravity: Vector2 = Vector2(0,0.2)


class Particle(_particle):
    def __init__(self) -> "Particle":
        super().__init__()

    def set_shape(cls, shape_: Shapes) -> "Particle":
        cls.particle_shape = shape_
        return cls

    def set_color(cls, color_value_: ParticleColor_) -> "Particle":
        cls.particle_color = color_value_
        return cls

    def set_speed(cls, speed_: float) -> "Particle":
        cls.particle_speed = speed_
        return cls

    def set_radius(cls, radius_: float) -> "Particle":
        cls.particle_radius = radius_
        return cls

    def set_size(cls, size_: Tuple[int, int] | Tuple[int]) -> "Particle":
        cls.particle_size = size_
        return cls

    def set_radius_randoming(cls, value_: float) -> "Particle":
        cls.particle_radius_randoming = value_
        return cls

    def set_move_angle(cls, angle_: float) -> "Particle":
        cls.particle_move_angle = angle_
        return cls

    def set_move_duration(cls, angle_: float) -> "Particle":
        cls.particle_move_duration = angle_
        return cls

    def set_size_deller(cls, value_: float) -> "Particle":
        cls.particle_size_deller = value_
        return cls

    def set_speed_rotation(cls, angle_: float) -> "Particle":
        cls.particle_speed_rotation = angle_
        return cls

    def set_move_adding(cls, value_: float) -> "Particle":
        cls.particle_move_adding = value_
        return cls

    def set_sinusing(cls, value_: float) -> "Particle":
        cls.particle_sinusing = value_
        return cls

    def set_sinusing_amplitude(cls, value_: float) -> "Particle":
        cls.particle_sinusing_amplitude = value_
        return cls

    def set_color_choise(cls, bool_: bool) -> "Particle":
        cls.particle_choise_color = bool_
        return cls

    def set_sprite(cls, sprite_: Sprite, scale_: float = 1) -> "Particle":
        cls.particle_sprite = sprite_
        cls.particle_sprite.set_size(scale_=scale_)
        cls.particle_sprite_scale = scale_
        return cls

    def set_sprite_mode(cls, mode_: SpriteModes) -> "Particle":
        cls.particle_sprite_mode = mode_
        return cls

    def set_sprite_rotate_angle(cls, angle_: float) -> "Particle":
        cls.particle_sprite_rotate_angle = angle_
        return cls

    def set_sprite_sum_angle(cls, angle_: float) -> "Particle":
        cls.particle_sprite_sum_angle = angle_
        return cls
    
    def set_phisics_simulate(cls, flag_: bool) -> "Particle":
        cls.particle_phisics = flag_
        return cls
    
    def set_phisics_gravity(cls, gravity_: Vector2) -> "Particle":
        cls.particle_phisics_gravity = gravity_
        return cls
    
    def set_phisics_trenie(cls, trenie_: Vector2) -> "Particle":
        cls.particle_phisics_trenie = trenie_
        return cls
    
    def set_particle_speed_randoming(cls, value_: int) -> "Particle":
        cls.particle_speed_randoming = value_
        return cls


class Spavner:
    def __init__(
        self,
        type_: SpavnerTypes = SpavnerTypes.RECT_SPAVNER,
        pos_: Tuple[int, int] = [0, 0],
        spavner_size_: Tuple[int, int] = [0, 0],
        spavner_radius_: int = 0,
        pos_2_: Tuple[int, int] = [0,0]
    ) -> None:
        self.type = type_
        self.pos = pos_
        self.pos_2 = pos_2_
        self.spavner_size = spavner_size_
        self.spavner_radius = spavner_radius_


class ParticleSpace:
    def __init__(self, Pos_: None, Size_: None, Win_: Window) -> "ParticleSpace":
        self.particles_ = []
        

        self._pos = Pos_
        self._size = Size_
        self._win = Win_
        self._time = 0

    def __construct_color__(self, particle_: Particle) -> Color:
        _color = particle_.particle_color
        _color_choise = particle_.particle_choise_color

        if _color_choise:
            _color = choice(_color)
        if isinstance(_color, Color):
            _color = _color.rgb
        return _color

    def __construct_speed__(self, particle_: Particle) -> Vector2:
        _speed = Vector2(0, 1)
        _speed *= (particle_.particle_speed+randint(0,particle_.particle_speed_randoming*10000)/10000)
        _speed.set_angle(
            particle_.particle_move_angle
            + randint(
                -particle_.particle_move_duration, particle_.particle_move_duration
            )
        )
        return _speed
    
    def __construct_collider__(self,
                               particle_: Particle, 
                               particle_pos_: Tuple[int,int], 
                               particle_radius_: int , 
                               particle_size_: Tuple[int,int],
                               particle_speed_: Vector2,
                               image_size_: Tuple[int,int]) -> Collider:
        if particle_.particle_shape == Shapes.CIRCLE:
            _collider = Collider(particle_pos_[0],particle_pos_[1], particle_radius_*2, particle_radius_*2, particle_speed_, gravity=particle_.particle_phisics_gravity,trenie=particle_.particle_phisics_trenie)
        if particle_.particle_shape == Shapes.RECT:
            _collider = Collider(particle_pos_[0],particle_pos_[1], particle_size_[0], particle_size_[1], particle_speed_, gravity=particle_.particle_phisics_gravity,trenie=particle_.particle_phisics_trenie)
        if particle_.particle_shape == Shapes.IMAGE:
            _collider = Collider(particle_pos_[0],particle_pos_[1], image_size_[0], image_size_[1], particle_speed_, gravity=particle_.particle_phisics_gravity,trenie=particle_.particle_phisics_trenie)
        return _collider

    def __construct_particle__(self, particle_: Particle, spavner_: Spavner) -> dict:
        if spavner_.type == SpavnerTypes.RECT_SPAVNER:
            particle_pos = [
                spavner_.pos[0] + randint(0, spavner_.spavner_size[0]),
                spavner_.pos[1] + randint(0, spavner_.spavner_size[1]),
            ]
        if spavner_.type == SpavnerTypes.LINE_SPAVNER:
            pos1 = spavner_.pos
            pos2 = spavner_.pos_2
            vector = Vector2(pos1[0]-pos2[0],pos1[1]-pos2[1])
            lenght = vector.lenght
            vector.normalyze()
            vector*=randint(0,int(lenght)*1000)/1000
            particle_pos = [
                spavner_.pos_2[0]+vector.x,
                spavner_.pos_2[1]+vector.y,
            ]
        particle_radius = particle_.particle_radius + randint(
                0, particle_.particle_radius_randoming
        )
        particle_shape = particle_.particle_shape
        particle_color = self.__construct_color__(particle_)
        particle_speed = self.__construct_speed__(particle_)
        particle_size_deller = particle_.particle_size_deller
        particle_speed_rotation = particle_.particle_speed_rotation
        particle_move_angle = particle_.particle_move_angle
        particle_move_adding = particle_.particle_move_adding
        particle_sinusing = particle_.particle_sinusing
        particle_sinusing_amplitude = particle_.particle_sinusing_amplitude
        particle_size = copy(particle_.particle_size)
        particle_sprite = copy(particle_.particle_sprite)
        particle_sprite_mode = particle_.particle_sprite_mode
        particle_sprite_angle = 0
        particle_sprite_rotate_angle = particle_.particle_sprite_rotate_angle
        particle_sprite_scale = particle_.particle_sprite_scale
        particle_sprite_sum_angle = particle_.particle_sprite_sum_angle
            
        if particle_.particle_phisics:
            particle_collider = self.__construct_collider__(particle_, particle_pos, particle_radius, particle_size, particle_speed, particle_sprite.render_image.get_size())
        else:
            particle_collider = None
        

        particle = {
                "pos": particle_pos,
                "size": particle_size,
                "timer": 0,
                "shape": particle_shape,
                "color": particle_color,
                "speed": particle_speed,
                "radius": particle_radius,
                "sprite": particle_sprite,
                "move_angle": particle_move_angle,
                "size_sinus": particle_sinusing,
                "size_deller": particle_size_deller,
                "move_adding": particle_move_adding,
                "sprite_mode": particle_sprite_mode,
                "speed_rotation": particle_speed_rotation,
                "sprite_angle": particle_sprite_angle,
                "size_sinus_amplitude": particle_sinusing_amplitude,
                "sprite_rotate_angle": particle_sprite_rotate_angle,
                "sprite_scale": particle_sprite_scale,
                "sprite_sum_angle": particle_sprite_sum_angle,
                "collider": particle_collider
        }
        return particle

    def add(
        self,
        particle_: Particle,
        spavner_: Spavner,
        count_: int = 1,
        spawn_time_: int = 5,
    ):
        if int(self._time) % spawn_time_ == 0:
            for _ in range(count_):
                __constructed_particle = self.__construct_particle__(
                    particle_, spavner_
                )
                self.particles_.append(__constructed_particle)

    def draw(self):
        for particle_ in self.particles_:
            if particle_["shape"] == Shapes.CIRCLE:
                Draw.draw_circle(
                    self._win(),
                    particle_["pos"],
                    particle_["radius"],
                    particle_["color"],
                )
            if particle_["shape"] == Shapes.RECT:
                Draw.draw_rect(
                    self._win(),
                    [
                        particle_["pos"][0] - particle_["size"][0] / 2,
                        particle_["pos"][1] - particle_["size"][1] / 2,
                    ],
                    particle_["size"],
                    particle_["color"],
                )
            if particle_["shape"] == Shapes.IMAGE:
                particle_["sprite"].center = particle_["pos"]
                particle_["sprite"].draw(self._win)

    def update(self, RectSpace_: None | Tuple[Collider, ...] = None):
        self._time += 1
        for particle_ in self.particles_:
            
            particle_["timer"] += 1
            if particle_['collider'] is None:
                particle_["pos"][0] += particle_["speed"].x * self._win.delta
                particle_["pos"][1] += particle_["speed"].y * self._win.delta
            else:
                
                
                particle_['pos'][0] = particle_['collider'].center[0]
                particle_['pos'][1] = particle_['collider'].center[1]
                if particle_['shape'] == Shapes.RECT:
                    particle_['collider'].wh = particle_['size']
                if particle_['shape'] == Shapes.CIRCLE:
                    particle_['collider'].wh = [particle_['radius']*2,particle_['radius']*2]
                if particle_['shape'] == Shapes.IMAGE:
                    particle_['collider'].wh = [int(particle_['sprite'].valid_image.get_width()),int(particle_['sprite'].valid_image.get_height())]
                particle_['collider'].collide_rect_list(RectSpace_,jumping=1)

            if particle_["shape"] == Shapes.CIRCLE:
                particle_["radius"] -= particle_["size_deller"] * self._win.delta
                particle_["radius"] -= (
                    sin(particle_["timer"] * particle_["size_sinus_amplitude"])
                    * particle_["size_sinus"]
                )

            if particle_["shape"] == Shapes.RECT:
                particle_["size"][0] -= particle_["size_deller"] * self._win.delta
                particle_["size"][1] -= particle_["size_deller"] * self._win.delta
                particle_["size"][0] -= (
                    sin(particle_["timer"] * particle_["size_sinus_amplitude"])
                    * particle_["size_sinus"]
                )
                particle_["size"][1] -= (
                    sin(particle_["timer"] * particle_["size_sinus_amplitude"])
                    * particle_["size_sinus"]
                )

            if particle_["shape"] == Shapes.IMAGE:
                particle_["sprite_scale"] -= (
                    particle_["size_deller"] / 10 * self._win.delta
                )
                try:
                    particle_["sprite"].set_size(scale_=particle_["sprite_scale"])
                except:
                    ...

                if particle_["sprite_mode"] == SpriteModes.VECTOR:
                    particle_["sprite"].set_angle(
                        angle_=particle_["speed"].get_angle()
                        + particle_["sprite_sum_angle"]
                    )
                if particle_["sprite_mode"] == SpriteModes.ROTATE:
                    particle_["sprite_angle"] += (
                        particle_["sprite_rotate_angle"] * self._win.delta
                    )
                    particle_["sprite"].set_angle(angle_=particle_["sprite_angle"])

            particle_["speed"].rotate(particle_["speed_rotation"] * self._win.delta)
            particle_["speed"] *= particle_["move_adding"]

    def deller(self):
        self.particles_ = list(
            filter(
                lambda elem: elem["sprite_scale"] > 0,
                self.particles_,
            )
        )
        

        self.particles_ = list(
            filter(
                lambda elem: elem["radius"] >= 0,
                self.particles_,
            )
        )

        self.particles_ = list(
            filter(
                lambda elem: elem["size"][0] > 0 and elem["size"][1] > 0,
                self.particles_,
            )
        )

        self.particles_ = list(
            filter(
                lambda elem: elem["pos"][0] > self._pos[0]
                and elem["pos"][0] < self._pos[0] + self._size[0],
                self.particles_,
            )
        )
        self.particles_ = list(
            filter(
                lambda elem: elem["pos"][1] > self._pos[1]
                and elem["pos"][1] < self._pos[1] + self._size[1],
                self.particles_,
            )
        )
