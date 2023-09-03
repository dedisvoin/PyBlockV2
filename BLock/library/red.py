from copy import copy
from rich.console import Console
from rich.theme import Theme


import os


class Colors:
    color_red1 = "rgb(200,100,120)"
    color_blue1 = "rgb(20,10,220)"
    number_style = "rgb(150,170,50)"
    function_color = "rgb(0,125,155)"
    syms_color = "rgb(150,130,10)"
    grey = "rgb(120,100,100)"
    word_color = "rgb(200,30,160) bold"
    self_color = "rgb(200,190,30)"
    class_and_def_colors = "rgb(30,100,200) bold"
    classes_color = "rgb(20,100,150)"
    my_class_color = "rgb(240,190,140) bold"

    decor_color = "rgb(200,250,50)"


funcs = ["print", "range", "input", "exec", "evel", "len", "enumerate", "exit"]
funcs += str.__dict__
funcs += int.__dict__


syms = [
    "{",
    "}",
    "(",
    ")",
    "=",
    "д",
    "+",
    "-",
    "*",
    "/",
    "[",
    "]",
    ":",
    "п",
    "м",
    "р",
    "д",
    "у",
]
wordes = [
    "for",
    "in",
    "while",
    "class",
    "def",
    "import",
    "from",
    "as",
    "if",
    "else",
    "elif",
    "lambda",
    "return",
    "not",
    "@",
    "try",
    "except",
    "or",
    "and",
]
self_ = ["self"]
clases = ["int", "str", "list", "set"]

console = Console(theme=Theme({"repr.number": "rgb(230,180,100)"}))


class Engine:
    def __init__(self) -> None:
        self.otstup = 36

    def View_hello_message(self, files: dict):
        console.print("-" * self.otstup, style=Colors.color_red1, end="")
        console.print("[ PyCode ]", style=Colors.color_blue1, end="")
        console.print("-" * self.otstup, style=Colors.color_red1)

        console.print("|", style="rgb(100,0,100)", end=" ")
        console.print("line", style="rgb(100,200,100)", end=" ")
        console.print("|", style="rgb(100,0,100)", end=" ")

        console.print("open files -> [ ", style="rgb(200,50,170)", end="")
        keys = [i for i in files.keys()]
        console.print(*keys, style="rgb(10,150,230)", end="")
        console.print(" ]", style="rgb(200,50,170)", end="\n")

        console.print("-" * (self.otstup * 2 + 10), style=Colors.color_red1)


class App:
    def __init__(self) -> None:
        self._codes = {}
        self._code = ""
        self._file_name = None
        self._run = True

        self._eng = Engine()
        self._end_stroke_bumber = 0
        self._code_runing = False
        self._classes = []

        self._defes = []
        self._perems = []

    def code_create(self, stroke: str):
        stroke = stroke.replace("{", " { ")
        stroke = stroke.replace("}", " } ")
        stroke = stroke.replace("(", " ( ")
        stroke = stroke.replace(")", " ) ")
        stroke = stroke.replace("[", " [ ")
        stroke = stroke.replace("]", " ] ")
        stroke = stroke.replace(".", " . ")
        stroke = stroke.replace(",", " , ")
        stroke = stroke.replace("==", " р ")
        stroke = stroke.replace("+=", " п ")
        stroke = stroke.replace("-=", " м ")
        stroke = stroke.replace("*=", " у ")
        stroke = stroke.replace("/=", " д ")

        stroke = stroke.replace("=", " = ")
        stroke = stroke.replace("-", " - ")
        stroke = stroke.replace("/", " / ")
        stroke = stroke.replace("*", " * ")
        stroke = stroke.replace("+", " + ")
        stroke = stroke.replace("%", " % ")
        stroke = stroke.replace(":", " : ")
        stroke = stroke.replace("@", " @ ")
        stroke = stroke.replace('"', ' " ')

        stroke = stroke.replace("\t", "\t ")

        words = stroke.split(" ")
        # print(words)
        while "" in words:
            words.remove("")
        cav_open = False
        for i, word in enumerate(words):
            color = Colors.grey

            in_words = False
            m = copy(funcs) + copy(syms) + copy(wordes) + copy(self_) + copy(clases)
            for w in m:
                if word in w:
                    in_words = True
                    break
            if not in_words:
                word = word.replace(" ", "")
            try:
                if words[i - 2] == "self":
                    color = Colors.color_red1
            except:
                ...
            if word == '"' and cav_open:
                cav_open = False
            elif word == '"' and not cav_open:
                cav_open = True
            if word in funcs:
                color = Colors.function_color
            if word in syms:
                color = Colors.syms_color
            if word in wordes:
                color = Colors.word_color
            if word in self_:
                color = Colors.self_color
            if words[i - 1] in ["def"]:
                color = Colors.class_and_def_colors
            if words[i - 1] in ["class"]:
                color = Colors.my_class_color
            if word in clases:
                color = Colors.classes_color

            try:
                if word == "=":
                    if words[i - 1] not in syms and words[i - 1] != '"':
                        self._perems.append(words[i - 1])
                if word == "for":
                    if words[i + 1] not in syms and words[i + 1] != '"':
                        self._perems.append(words[i + 1])
            except:
                ...

            if word == " ( ":
                word = "("
            if word == ",":
                word = ", "
            if word == " ) ":
                word = ")"
            if word == "in":
                word = " in "
            if word == "if":
                word = "if "
            if word == "or":
                word = " or "
            if word == "and":
                word = " and "
            if word == "else":
                word = "else "
            if word == "elif":
                word = "elif "
            if word == "lambda":
                word = "lambda "
            if words[i - 1] and words[i - 1] != "\t" and i - 1 != -1:
                if word == "for":
                    word = " for "
            else:
                if word == "for":
                    word = "for "

            if word == "class":
                word = "class "
                if words[i + 1] not in syms and words[i + 1] != '"':
                    self._classes.append(words[i + 1])

            if word == "def":
                word = "def "
                if words[i + 1] not in syms and words[i + 1] != '"':
                    self._defes.append(words[i + 1])
            if word == "return":
                word = "return "
            if word == "while":
                word = "while "
            try:
                if words[i - 2] == "from":
                    if word == "import":
                        word = " import "
                else:
                    if word == "import":
                        word = "import "
            except:
                if word == "import":
                    word = "import "

            if word == "from":
                word = "from "
            if word == "as":
                word = " as "
            if word == "not":
                word = " not "
            if word == "\t":
                word = " |  "
            if word == "=":
                word = " = "
            if word == "%":
                word = " % "
            if word == "р":
                word = " == "
            if word == "п":
                word = " += "
            if word == "м":
                word = " -= "
            if word == "д":
                word = " /= "
            if word == "у":
                word = " *= "
            if words[i - 1] == "@":
                color = Colors.decor_color
            if cav_open or word == '"':
                color = "rgb(10,230,100)"
            if word in self._classes:
                color = Colors.my_class_color
            if word in self._defes:
                color = Colors.class_and_def_colors
            if word in self._perems:
                color = Colors.color_red1
            if word in syms:
                color = Colors.syms_color

            console.print(word, style=color, end="")

        print()

    def viev_code(self):
        if self._file_name in self._codes:
            stroks = self._codes[self._file_name].split("\n")
            stroks = filter(lambda elem: elem != "", stroks)

            for i, stroke in enumerate(stroks):
                console.print("[", style=Colors.number_style, end="")
                print(f" {i:>4} ", end="")
                console.print("]", style=Colors.number_style, end=" ")
                self.code_create(stroke)
            try:
                self._end_stroke_bumber = i + 1
            except:
                self._end_stroke_bumber = 0

    def commands(self, inp):
        if inp[:4] == "open":
            text = inp.split(" ")
            s = open(text[1], "r")

            _code = ""
            for stroke in s.readlines():
                stroke = stroke.replace("    ", "\t")
                if stroke == "\n":
                    stroke = " \n"
                _code += stroke + "\n"
            self._codes[text[1]] = _code

        elif inp == "exit":
            os.system("cls")
            exit(-1)
        elif inp == "clear" or inp == "cls":
            self._codes[self._file_name] = ""
            self._code_runing = False
        elif inp == "run":
            os.system("cls")
            exec(self._codes[self._file_name])
            self._code_runing = True
        elif inp[:4] == "jump":
            text = inp.split(" ")
            try:
                if text[1] in self._codes.keys():
                    self._file_name = text[1]
                else:
                    self._file_name = [i for i in self._codes.keys()][int(text[1])]
            except:
                print("Jump Error!")

        elif inp == "view vars":
            os.system("cls")
            print(self._perems)
            self._code_runing = True
        elif inp == "":
            self._codes[self._file_name] = self._codes[self._file_name][:-1]
        else:
            self._code_runing = False
            return True

    def run(self):
        while self._run:
            if not self._code_runing:
                os.system("cls")
            self._code_runing = False
            self._eng.View_hello_message(self._codes)
            self.viev_code()
            inp = input(f"[ {self._end_stroke_bumber:>4} ] ")
            com = self.commands(inp)
            if com != None:
                self._codes[self._file_name] += inp + "\n"


app = App()

app.run()
