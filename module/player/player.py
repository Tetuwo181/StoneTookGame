# -*- coding: utf-8 -*-
from importlib import machinery 
from typing import Callable
from typing import Optional


class Player(object):
    """
    石取りゲームをするプレイヤー
    戦略を引数として初期化
    """
    def __init__(self,
                 strategy:Callable[[int, int, Optional[int], Optional[int]], int],
                 name:str = "anonimous"):
        self.__strategy = strategy
        self.__name = name
        self.__pre_took = None
        
    @property
    def strategy(self)->Callable[[int, int, Optional[int], Optional[int]], int]:
        return self.__strategy
    
    @property
    def name(self)->str:
        return self.__name
    
    def get_stone(self,
                  stone_num:int,
                  get_max:int,
                  pretook_enemy:Optional[int] = None
                  )->int:
        """
        戦略に応じて石を取る数を決める
        石が1個以下しかなければ-1を返す
        stone_num:int 山に残っている石の数
        get_max:int 石を取れる最大数
        pretook_enemy:Optional[int]: 直前に相手がとった石の数
        """
        try:
            if stone_num < 2:
                return -1
            took_stone = self.strategy(stone_num,
                                       get_max,
                                       pretook_enemy,
                                       self.__pre_took)
            return took_stone
        finally:
            self.__pre_took = took_stone

def build_player_from_strategy_module(module_name:str):
    """
    strategyフォルダ内にあるpythonファイルから戦略を読み込み
    プレイヤーを生成する。
    戦略を記述したファイルの構成は、utf-8で記述されたファイルで
    中にstrategy関数のみを実装したフォルダを使う。
    stone_num:int 山に残っている石の数
    get_max:int 石を取れる最大数
    pretook_enemy:Optional[int]: 直前に相手がとった石の数
    pretook_self:Optional[int]: 直前に自分がとった石の数
    """
    module = machinery.SourceFileLoader("strategies.", module_name).load_module()
    return Player(module.strategy)