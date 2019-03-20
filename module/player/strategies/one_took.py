# -*- coding: utf-8 -*-
from typing import Optional

def strategy(stone_num:int,
             get_max:int,
             pretook_enemy:Optional[int] = None,
             pretook_self:Optional[int] = None)->int:
    """
    何が何でも1個しかとらない
    引数に何の意味もないけどインターフェース統一のために
    """
    if stone_num < 2:
        return -1    
    return 1