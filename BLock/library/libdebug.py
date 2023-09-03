from copy import copy
from colorama import Fore, Style
import os
import time


class Debug:
    def __init__(self) -> None:
        self.__debug = ""
        self.DEBUGING = False

    def log(self):
        dummy = copy(self.__debug)

        with open("log.txt", "w") as log_file:
            log_file.write(dummy)

    def exit(self):
        os._exit(-1)

    @property
    def ERROR(self):
        return f"{Style.BRIGHT}{Fore.RED}ERROR{Fore.RESET}{Style.RESET_ALL}"

    @property
    def SUCCSES(self):
        return f"{Style.BRIGHT}{Fore.GREEN}SUCCSES{Fore.RESET}{Style.RESET_ALL}"

    @property
    def SUCCSES_SCOBS(self):
        return f"[ {self.SUCCSES} ]"

    @property
    def ERROR_SCOBS(self):
        return f"[ {self.ERROR} ]"

    @property
    def CRITICAL_ERROR(self):
        return f"{Style.BRIGHT}{Fore.RED}CRITICAL ERROR{Fore.RESET}{Style.RESET_ALL}"

    @property
    def CRITICAL_ERROR_SCOBS(self):
        return f"[ {self.CRITICAL_ERROR} ]"

    @property
    def BLACK(self):
        return f"{Fore.BLUE}"

    @property
    def RES(self):
        return f"{Fore.RESET}"

    @property
    def LIST(self):
        return f"[ {Fore.CYAN}LIST{Fore.RESET} ]"

    @property
    def LIST_TRANSFORM(self):
        return f"[ {Fore.LIGHTCYAN_EX}TRANSFORM{Fore.RESET} ]"

    @property
    def LIST_GENERATE(self):
        return f"[ {Fore.LIGHTBLUE_EX}GENERATE{Fore.RESET} ]"

    @property
    def LIST_COPY(self):
        return f"[ {Fore.LIGHTBLUE_EX}COPY{Fore.RESET} ]"

    @property
    def AT_TIME(self):
        t = time.ctime(time.time())
        return f"[ {Fore.LIGHTMAGENTA_EX}{t.split(' ')[3]}{Fore.RESET} ]"

    @property
    def LOG(self):
        return f"{Fore.YELLOW}log {Fore.RESET}"

    @property
    def DEBUG(self):
        return f"{self.AT_TIME} - {self.LOG}"

    def create_log(self, *args):
        dummy = ""
        for arg in args:
            dummy += arg
        self.__debug += dummy + "\n"

    def show(self):
        if self.DEBUGING:
            os.system("cls")
            print(self.__debug)
