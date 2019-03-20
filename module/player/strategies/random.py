# -*- coding: utf-8 -*-
import random as RD
from typing import Optional

def strategy(stone_num:int,
             get_max:int,
             pretook_enemy:Optional[int] = None,
             pretook_self:Optional[int] = None)->int:
    """
    取る数をランダムで決定
    """
    if stone_num < 2:
        return -1
    if stone_num > get_max:
        get_num = RD.randint(1, get_max)
    else:
        get_num = RD.randint(1, stone_num)
    return get_num