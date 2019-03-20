# -*- coding: utf-8 -*-
from typing import Optional

def strategy(stone_num:int,
             get_max:int,
             pretook_enemy:Optional[int] = None,
             pretook_self:Optional[int] = None)->int:
    """
    石取りゲーム必勝法の戦略
    """
    mod = stone_num % get_max
    if mod == 0:
        return get_max - 1
    if mod == 1:
        return get_max
    return mod - 1