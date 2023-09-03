from collections.abc import Iterator
from typing import Any, Iterable, Iterator, Self, Callable, Tuple, NewType
from ast import literal_eval
from random import randint, choice
import random

if __name__ == "__main__":
    from libdebug import Debug
else:
    from library.libdebug import Debug

DEB = Debug()


def id_generate(lenght_: int = 5):
    _syms = "abcdefghijklmnopqrstuvywz"
    _syms_id = "#"
    for i in range(lenght_):
        _syms_id += _syms[random.randint(0, len(_syms) - 1)]
    return _syms_id


def getargs(*args, index: str):
    try:
        return args[index]
    except:
        return None


def debug():
    DEB.DEBUGING = True


def getClass(object_: object) -> str:
    string_object = str(object_.__class__).split("'")[1]
    if "." in string_object:
        string_object = string_object.split(".")[-1]
    return string_object


class Null:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Null"

    def __eq__(self, __value: object) -> bool:
        return type(self) == type(__value)

    def __ne__(self, __value: object) -> bool:
        return type(self) != type(__value)


Index_ = NewType("Index", int)


all_lists = []


class List:
    @classmethod
    def binary_search(
        self, Soreted_List_object_: "List", search_number_: int
    ) -> Index_:
        if Soreted_List_object_.__to_sorted__():
            first_index = 0
            size = Soreted_List_object_.len()
            last_index = size - 1
            mid_index = Soreted_List_object_.__get_center__()

            mid_element = Soreted_List_object_[mid_index]

            is_found = True
            while is_found:
                if first_index == last_index:
                    if mid_element != search_number_:
                        is_found = False
                        return False
                elif mid_element == search_number_:
                    return mid_index
                elif mid_element > search_number_:
                    new_position = mid_index - 1
                    last_index = new_position
                    mid_index = (first_index + last_index) // 2
                    mid_element = Soreted_List_object_[mid_index]
                    if mid_element == search_number_:
                        return mid_index
                elif mid_element < search_number_:
                    new_position = mid_index + 1
                    first_index = new_position
                    last_index = size - 1
                    mid_index = (first_index + last_index) // 2
                    mid_element = Soreted_List_object_[mid_index]
                    if mid_element == search_number_:
                        return mid_index
        else:
            return False

    @classmethod
    def find_by_id(self, id_: str | int) -> "List":
        for list_object_ in all_lists:
            if list_object_[0] == id_:
                return list_object_[1]

    @classmethod
    def delete_with_id(self, id_: str | int) -> Null:
        for i, obj in enumerate(all_lists):
            if all_lists[i][0] == id_:
                del obj
                del all_lists[i][1]
                del all_lists[i]
                break

    @classmethod
    @property
    def all_list(self) -> Null:
        global all_lists
        __str = ""
        for list_obj_ in all_lists:
            __str += str(list_obj_[1]) + " "
        return __str

    @classmethod
    @property
    def lists_count(self) -> int:
        return len(all_lists)

    @classmethod
    @property
    def lists(self) -> Iterator["List"]:
        for list_obj_ in all_lists:
            yield list_obj_[1]

    @classmethod
    def convert(
        self,
        iterable_: list | str | int | tuple | dict | bytes,
        string_split_sym: str = None,
        use_ast_: bool = False,
    ) -> Self:
        DEB.create_log(
            DEB.DEBUG,
            DEB.SUCCSES_SCOBS,
            DEB.LIST,
            " --> ",
            f"Converting {iterable_} started!",
        )
        DEB.show()
        if isinstance(iterable_, (list, tuple)):
            _dummy = [elem_ for elem_ in iterable_]
            return List(_dummy)
        elif isinstance(iterable_, int):
            _dummy = [elem_ for elem_ in str(iterable_)]
            return List(_dummy)
        elif isinstance(iterable_, str):
            if use_ast_ is False:
                if string_split_sym is None:
                    _dummy = [elem_ for elem_ in str(iterable_)]
                else:
                    _dummy = iterable_.split(string_split_sym)
            else:
                _dummy = literal_eval(iterable_)
            return List(_dummy)
        elif isinstance(iterable_, dict):
            _dummy = [[name_, iterable_[name_]] for name_ in iterable_]
            return List(_dummy)
        elif isinstance(iterable_, bytes):
            _dummy = literal_eval(iterable_.decode())
            return List(_dummy)
        else:
            DEB.create_log(
                DEB.DEBUG,
                DEB.CRITICAL_ERROR_SCOBS,
                DEB.LIST,
                " --> ",
                f"Converting {iterable_} don't finished, because object type[{DEB.BLACK}{type(iterable_)}{DEB.RES}] not found!",
            )
            DEB.show()
            DEB.exit()

    @classmethod
    def generate(
        self,
        random_num_: Tuple[int, int, int] = None,
        choise_: Tuple[Tuple[Any] | str, int, bool] = None,
    ) -> Self:
        DEB.create_log(
            DEB.DEBUG,
            DEB.LIST,
            DEB.LIST_GENERATE,
            " --> ",
            f"Generate args[{DEB.BLACK}{random_num_=}, {choise_=}{DEB.RES}] start...",
        )
        DEB.show()
        if random_num_ is not None:
            _count = random_num_[2]
            _start = random_num_[0]
            _stop = random_num_[1]
            _dummy = [randint(_start, _stop) for _ in range(_count)]

            DEB.create_log(
                DEB.DEBUG,
                DEB.SUCCSES_SCOBS,
                DEB.LIST,
                DEB.LIST_GENERATE,
                " --> ",
                f"generating args[{DEB.BLACK}{random_num_=}{DEB.RES}] finish!",
            )

            return List(_dummy)
        if choise_ is not None:
            _count = choise_[1]
            _objs = choise_[0]
            _call = choise_[2]
            _dummy = []
            for _ in range(_count):
                if not _call:
                    _dummy.append(choice(_objs))
                else:
                    _dummy.append(choice(_objs)())

            DEB.create_log(
                DEB.DEBUG,
                DEB.SUCCSES_SCOBS,
                DEB.LIST,
                DEB.LIST_GENERATE,
                " --> ",
                f"generating args[{DEB.BLACK}{choise_=}{DEB.RES}] finish!",
            )

            return List(_dummy)

    def __init__(self, iterable_: Iterable | list, id_: str | int = None) -> "List":
        global all_lists
        self._list = iterable_

        self._id = id_generate(7)
        if id_ is not None:
            self._id = id_
        DEB.create_log(
            DEB.DEBUG,
            DEB.SUCCSES_SCOBS,
            DEB.LIST,
            " --> ",
            f"List [ id:{self._id} ] created!",
        )

        all_lists.append([self._id, self])
        DEB.show()

    def __eq__(self, __value: "List") -> bool:
        return self._list.__eq__(__value._list)

    def __ne__(self, __value: "List") -> bool:
        return self._list.__ne__(__value._list)

    def __add__(self, value__: "List") -> "List":
        return self.to_extend(value__)

    def __iadd__(self, value__: "List") -> Self:
        self.extend(value__)
        return self

    def __str__(self) -> str:
        return f"{self._list}"

    def __len__(self) -> int:
        return self._list.__len__()

    def __getitem__(self, index_or_srice_: slice | int) -> object:
        return self._list.__getitem__(index_or_srice_)

    def __setitem__(self, index_: int, object_: Any) -> Null:
        self._list.__setitem__(index_, object_)

    def __iter__(self) -> Iterator:
        return self._list.__iter__()

    def __contains__(self, object__: Any) -> bool:
        return self._list.__contains__(object__)

    def __bool_contains__(self, list: "List") -> "List":
        _new_list = List([])
        for elem in list:
            obj = elem
            if isinstance(elem, bool):
                if elem == True or elem == False:
                    obj = str(elem)

            _new_list.add(obj)
        return _new_list

    def __bool_convert__(self, obj: str) -> bool:
        if obj == "True":
            return True
        if obj == "False":
            return False
        return obj

    def __all_nums__(self) -> bool:
        _count: int = 0
        for elem in self._list:
            if isinstance(elem, (int, float)):
                _count += 1
        if self.len() == _count:
            return True
        return False

    def __get_center__(self) -> Index_:
        return int(self.len() // 2)

    def __to_sorted__(self) -> bool:
        trigg_ = 0
        for i in range(len(self._list)):
            if self._list[i] >= self._list[i - 1]:
                trigg_ += 1

        if trigg_ == self.len() - 1:
            return True

        trigg_ = 0
        for i in range(len(self._list)):
            n = max(i - 1, 0)

            if self._list[i] <= self._list[n]:
                trigg_ += 1

        if trigg_ == self.len() - 1:
            return True

        return False

    def len(self) -> int:
        return len(self._list)

    def copy(self) -> "List":
        _new_list = self._list.copy()
        _copy_list = List(_new_list)
        DEB.create_log(
            DEB.DEBUG,
            DEB.SUCCSES_SCOBS,
            DEB.LIST,
            DEB.LIST_COPY,
            " --> ",
            f"Copy List[{DEB.BLACK}{self.id=}{DEB.RES}] to List[{DEB.BLACK}{_copy_list.id=}{DEB.RES}]",
        )
        DEB.show()
        return _copy_list

    def clear(self) -> Null:
        DEB.create_log(
            DEB.DEBUG,
            DEB.LIST,
            DEB.LIST_TRANSFORM,
            " --> ",
            f"List[{DEB.BLACK}{self.id=}{DEB.RES}] clearing...",
        )
        DEB.show()

        self._list.clear()

        DEB.create_log(
            DEB.DEBUG,
            DEB.SUCCSES_SCOBS,
            DEB.LIST,
            DEB.LIST_TRANSFORM,
            " --> ",
            f"List[{DEB.BLACK}{self.id=}{DEB.RES}] clearing finish!",
        )
        DEB.show()

    def add(self, object_: Any):
        DEB.create_log(
            DEB.DEBUG,
            DEB.LIST,
            DEB.LIST_TRANSFORM,
            " --> ",
            f"List[{DEB.BLACK}{self.id=}{DEB.RES}] add new object[{DEB.BLACK}{object_=}, {type(object_)}{DEB.RES}]",
        )
        DEB.show()
        self._list.append(object_)

    def insert(self, object_: Any, index_: int):
        try:
            self._list.insert(index_, object_)
            DEB.create_log()
        except:
            ...

    def to_insert(self, object_: Any, index_: int):
        _new_list = self.copy()
        _new_list.insert(object_, index_)
        return _new_list

    def count(self, object_: Any) -> int:
        return self._list.count(object_)

    def reverse(self):
        self._list.reverse()

    def to_reverse(self):
        _new_list = self.copy()
        _new_list.reverse()
        return _new_list

    def pop(self, index_: int):
        self._list.pop(index_)

    def to_pop(self, index_: int):
        _new_list = self.copy()
        _new_list.pop(index_)
        return _new_list

    def sort(self, sort_method_: Callable, reverse_: bool = False):
        self._list = sorted(self._list, key=sort_method_, reverse=reverse_)

    def to_sort(self, sort_method_: Callable, reverse_: bool = False) -> "List":
        _new_list = self.copy()
        _new_list.sort(sort_method_, reverse_)
        return _new_list

    def sub_list(self, start_index_: Index_, stop_index_: Index_) -> "List":
        sub_list_ = self._list[start_index_:stop_index_]
        return List(sub_list_)

    def map(self, map_method_: Callable):
        self._list = list(map(map_method_, self._list))

    def to_map(self, map_method_: Callable) -> "List":
        _new_list = self.copy()
        _new_list.map(map_method_)
        return _new_list

    def bytes(self) -> bytes:
        return str(self._list).encode()

    def range(self) -> Iterator:
        return [[obj_, index_] for obj_, index_ in enumerate(self._list)]

    def extend(self, iterable_: list | Iterable):
        if isinstance(iterable_, list):
            self._list.extend(iterable_)
        if isinstance(iterable_, List):
            self._list.extend(iterable_._list)

    def to_extend(self, iterable_: list | Iterable) -> "List":
        _new_list = self.copy()
        _new_list.extend(iterable_)
        return _new_list

    def any(self, object_: Any) -> bool:
        for _dummy_object_ in self._list:
            if _dummy_object_ == object_:
                return True

        return False

    def more(self, object_: Any) -> bool:
        _dummy_counter_ = 0
        for _dummy_object_ in self._list:
            if _dummy_object_ == object_:
                _dummy_counter_ += 1
        if _dummy_counter_ == self.len():
            return True
        return False

    def find(self, find_method_: Callable, find_end_: bool = False) -> Any:
        for i in range(len(self._list)):
            if find_end_:
                i = self.len() - 1 - i
            _elem = self._list[i]
            if list(map(find_method_, [_elem]))[0]:
                return _elem
        return None
    
    def find_all(self, find_method_: Callable) -> Any:
        arr = List([])
        for i in range(len(self._list)):
            _elem = self._list[i]
            if list(map(find_method_, [_elem]))[0]:
                arr.add(_elem)
        return arr

    def find_index(self, find_method_: Callable, find_end_: bool = False) -> int:
        for i in range(len(self._list)):
            if find_end_:
                i = self.len() - 1 - i
            _elem = self._list[i]
            if list(map(find_method_, [_elem]))[0]:
                return i
        return None

    def call(self, method_name_: str | list = None, *args, **kvargs):
        [
            elem.__class__.__dict__[method_name_](elem, *args, **kvargs)
            for elem in self._list
        ]

    def call_less_dell(self, argument_: str, less_value_: float | int):
        for i in range(len(self._list)):
            if self._list[i].__dict__[argument_] < less_value_:
                del self._list[i]
                break

    def call_more_dell(self, argument_: str, less_value_: float | int):
        for i in range(len(self._list)):
            if self._list[i].__dict__[argument_] > less_value_:
                del self._list[i]
                break

    def filter(self, filter_method_: Callable):
        self._list = list(filter(filter_method_, self._list))
        return self

    def to_filter(self, filter_method_: Callable) -> "List":
        _new_list = self.copy()
        _new_list.filter(filter_method_)
        return _new_list

    def set(self):
        self._list = list(set(self._list))

    def to_set(self) -> "List":
        _new_list = self.copy()
        _new_list.set()
        return _new_list

    def elemets(self) -> "List":
        _new_list = self.__bool_contains__(self)
        _dummy = _new_list.to_set()
        _counts = List([])
        for elem in _dummy:
            _counts.add([self.__bool_convert__(elem), _new_list.count(elem)])
        return _counts

    @property
    def python_list(self) -> list:
        return self._list

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int | str = None):
        if id is not None:
            self._id = id


all_dicts = []


class Dict:
    @classmethod
    def find_by_id(self, id_: str | int) -> "List":
        for dict_object_ in all_dicts:
            if dict_object_[0] == id_:
                return dict_object_[1]

    @classmethod
    def convert(self, iterable_: list | tuple) -> "Dict":
        dummy_ = {}
        for obj in iterable_:
            dummy_[obj[0]] == dummy_[1]
        return Dict(dummy_)

    def __init__(self, dict_: dict = None, id_: str | int = None) -> None:
        global all_dicts
        self._dict = {} if dict_ is None else dict_
        self._id = id_ if id_ is not None else id_generate(7)
        all_dicts.append([self._id, self])

    def __str__(self) -> str:
        return f"{self._dict}"

    def __copy__(self) -> dict:
        return self._dict.copy()

    def __iter__(self) -> Iterator:
        for obj, key in zip(self.values().python_list, self.keys().python_list):
            yield [obj, key]

    def __set_dict__(self, dummy_: dict):
        self._dict = dummy_

    def __eq__(self, __other: object) -> bool:
        return self._dict.__eq__(__other)

    def __ne__(self, __value: object) -> bool:
        return self._dict.__ne__(__value)

    def add(self, key_: any, value_: object):
        if key_ not in self._dict:
            self._dict[key_] = value_

    def change(self, key_: any, value_: object):
        if key_ in self._dict:
            self._dict[key_] = value_

    def clear(self):
        self._dict.clear()

    def copy(self) -> "Dict":
        dummy_ = Dict()
        dummy_.__set_dict__(self.__copy__())
        return dummy_

    def get(self, __key: Any) -> Any:
        return self._dict.__getitem__(__key)

    def values(self) -> List:
        dummy_ = List(list(self._dict.items().mapping.values()))
        return dummy_

    def keys(self) -> List:
        dummy_ = List(list(self._dict.keys()))
        return dummy_

    def pop(self, key_: any) -> tuple:
        return self._dict.pop(key_)


class Color:
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    PURPLE = [120, 100, 180]
    DARK_PURPLE = [120 / 2, 100 / 2, 180 / 2]

    def __init__(self, color: list | tuple) -> "Color":
        self._r = color[0]
        self._g = color[1]
        self._b = color[2]

    @classmethod
    def random(self) -> "Color":
        _r = random.randint(0, 255)
        _g = random.randint(0, 255)
        _b = random.randint(0, 255)
        return Color([_r, _g, _b])

    @property
    def rgb(self):
        return [self._r, self._g, self._b]

    @property
    def chb(self):
        _chb_value = (self._r + self._g + self._b) / 3
        return [_chb_value, _chb_value, _chb_value]

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, _value: int):
        self._r = _value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, _value: int):
        self._g = _value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, _value: int):
        self._b = _value


class Percent:
    def __init__(self, value_: int, max_value_: int) -> "Percent":
        self.__value = value_
        self.__max_value = max_value_

        self._percent = self.__value / self.__max_value

    def __str__(self) -> str:
        return f"{int(self._percent*100)}%"

    @property
    def float_percent(self) -> float:
        return self._percent

    @property
    def int_percent(self) -> int:
        return int(self._percent * 100)
