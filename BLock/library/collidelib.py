import math
import random
from .Lowlevelib import *

from typing import overload, Tuple, List



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
        self.id = random.randint(0,99999999999999)

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
    def wh(self, size_: Tuple[float,float]):
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
        return [self._x+self._w/2, self._y+self._h/2]
    
    @property
    def center_x(self):
        return self._x+self._w/2
    
    @property
    def center_y(self):
        return self._y+self._h/2
    
    @center_x.setter
    def center_x(self, _x:int):
        self._x = _x-self._w/2
    
    @center_y.setter
    def center_y(self, _y:int):
        self._y = _y-self._h/2
    
    @center.setter
    def center(self, pos):
        self._x = pos[0]-self._w/2
        self._y = pos[1]-self._h/2
        
        
class Collider:
    def __init__(self, x: float, y: float, w: float, h: float, 
                 simulating: bool = False, 
                 speed: Vector2 | None = None, id: None | Any = None,
                 resistance: Vector2 = Vector2(1,1),
                 elastic: Vector2 = Vector2(0,0),
                 
                 mass = 1000) -> None:
                
        self._rect = Rect(x,y,w,h)
        self._simulating = simulating
        self._speed = Vector2(0,0) if speed is None else speed
        self._id = random.randint(0,999999999) if id is None else id
        self._resistance = resistance
        self._elastic = elastic
        self._mass = mass
        
        self._collides = {
            'left':False, 'right':False,'up':False,'down':False
        }
        
    def collides_resset(self):
        self._collides = {
            'left':False, 'right':False,'up':False,'down':False
        }
        
    def draw(self, win):
        self._rect.draw(win)
        
    @property
    def sx(self) -> float:
        return self._speed.x
    
    @property
    def sy(self) -> float:
        return self._speed.y
    
    @sx.setter
    def sx(self, value):
        self._speed.x = value

    @sy.setter
    def sy(self, value):
        self._speed.y = value
        
    @property
    def center(self) -> Tuple[float, float]:
        return self._rect.center
    
    @center.setter
    def center(self, value) -> Tuple[float, float]:
        self._rect.center = value
        
class ColliderSpace:
    def __init__(self, gravity: Vector2, air_resistance: Vector2) -> None:
        self._gravity = gravity
        self._air_resistance = air_resistance
        self._colliders: Tuple[Collider, ...] = []
        
    def __collides_list_form__(self,collider_: Collider, colliders_: Tuple[Collider, ...]) -> Tuple[Collider, ...]:
        collide_list = []
        for collider in colliders_:
            if collider_._rect.collide_rect(collider._rect) and collider_._id != collider._id:
                collide_list.append(collider)
        return collide_list
    
    def __collide_from_rects__(self, collider: Collider, colliders: Tuple[Collider, ...]):
        collider.collides_resset()
        
        
        
        collider._rect.y+=collider._speed.y
        collide_list = self.__collides_list_form__(collider, colliders)
        
        for rect in collide_list:
            
            if collider._speed.y>0:
                collider._collides['down'] = True
                if collider._elastic.lenght!=0:
                    collider._speed.y *= -collider._elastic.y
                else:
                    collider._speed.y = 0
                collider._speed.x*=rect._resistance.x
                collider._rect.y_down = rect._rect.y_up

            elif collider._speed.y<0:
                collider._collides['up'] = True
                if collider._elastic.lenght!=0:
                    collider._speed.y *= -collider._elastic.y
                else:
                    collider._speed.y = 0
                collider._speed.x*=rect._resistance.x
                collider._rect.y_up = rect._rect.y_down
                
            

                
        collider._rect.x+=collider._speed.x   
        collide_list = self.__collides_list_form__(collider, colliders)
        
        for rect in collide_list:
            
            

            if collider._speed.x>0:
                rect.sx = collider.sx
                collider._collides['right'] = True
                collider._speed.x *= -collider._elastic.x
                collider._rect.x_right = rect._rect.x_left
                

            elif collider._speed.x<0:
                rect.sx = collider.sx
                collider._collides['left'] = True
                collider._speed.x *= -collider._elastic.x
                collider._rect.x_left = rect._rect.x_right
                
            
                

                
        
        
        
    def add(self, collider_: Collider | Tuple[Collider, ...]):
        if isinstance(collider_, Collider):
            self._colliders.append(collider_)
        elif isinstance(collider_, list):
            for collider in  collider_:
                self._colliders.append(collider)
        
    def speed_form(self,collider: Collider):
        collider._speed+=self._gravity
        collider._speed.x*=self._air_resistance.x
        collider._speed.y*=self._air_resistance.y
        
    def simulate(self):
        for collider in self._colliders:
            if collider._simulating:
                self.speed_form(collider)
                
                self.__collide_from_rects__(collider, self._colliders)
                  
    def render(self, win):
        [c.draw(win) for c in self._colliders]
        
    def collider(self, id) -> Collider:
        for collider in self._colliders:
            if collider._id == id:
                return collider
    
    
    
    

if __name__ == "__main__":
    win = Window(size=[1200,750])


    cs = ColliderSpace(Vector2(0,0.5))

    cs.add(
        Collider(50,100,50,50,True,id='ded')
    )

    cs.add(
        Collider(0,600,1200,50)
    )
    cs.add(
        Collider(0,0,50,1000)
    )
    cs.add(
        Collider(1200-50,0,50,1000)
    )





    while win.update(fps=60, fps_view=1, base_color='white'):
        cs.render(win())
        cs.simulate()
        
        if Keyboard.key_pressed('left'):
            cs.collider('ded').sx = -3
        if Keyboard.key_pressed('right'):
            cs.collider('ded').sx = 3
        if Keyboard.key_pressed('up'):
            cs.collider('ded').sy = -7
            
        if Mouse.click():
            cs.add(Collider(Mouse.position()[0],Mouse.position()[1],50,50,True,speed=Vector2(random.randint(-5,5),random.randint(-5,5)),mass=1))
        
        