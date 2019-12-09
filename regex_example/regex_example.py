"""
A file with various imports
"""

import enum
import enum, typing
import numbers as something_else
from math import (
    sqrt,
    pow,
    sin as useless,
    cos,
    tan,
    tanh,
    sinh as something_to_fill_up_this_line_to_make_it_120_characters,
)

from multiprocessing import Process as ProcessRandomName
from typing import List, Optional, Union
from typing import Set


class UpgradeId(enum.Enum):
    TERRANINFANTRYWEAPONSLEVEL1 = 7
    TERRANINFANTRYWEAPONSLEVEL2 = 8
    TERRANINFANTRYWEAPONSLEVEL3 = 9
    SS_INTERCEPTOR = 1035


class MyClass:
    def __init__(self):
        pass


class SomeClass(MyClass, enum.Enum):
    """ Some docstring that should be removed. """

    def __init__(self):
        """ Some init function docstring """
        MyClass.__init__(self)
        # A comment
        self.my_instance_var = 5
        self.my_instance_string = "6"
        if hasattr(self, "my_instance_var"):
            setattr(self, "my_instance_var", 3)

    # Multiline function
    def my_function(
        self,
        parameter_name1=7,
        parameter_name2: int = 8,
        parameter_name3: List[Union[Optional[int], Set[str]]] = 8,
        parameter_name4=None,
    ):
        pass

    # Single line function
    def my_function2(self, parameter_name5: str = "hello", parameter_name6="something"):
        pass


"""
Found names that should be ignored by opy are:
import, enum, Enum, from, math, sqrt, pow, sin, as, useless, cos, tan, tanh, sinh, something_to_fill_up_this_line_to_make_it_120_characters,
multiprocessing, Process, ProcessRandomName,
typing, List, Optional, Set, Union

TERRANINFANTRYWEAPONSLEVEL1
7
TERRANINFANTRYWEAPONSLEVEL2
8
TERRANINFANTRYWEAPONSLEVEL3
9
SS_INTERCEPTOR
1035

class
MyClass
__init__
self
pass

SomeClass
my_instance_var
my_instance_string
my_function
parameter_name1
parameter_name2
int
parameter_name3
str
parameter_name4
parameter_name5
parameter_name6
"""
