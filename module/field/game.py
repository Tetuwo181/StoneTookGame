# -*- coding: utf-8 -*-

from ..player import player as PL
from ..recorder import recorder as REC
from datetime import datetime
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Optional
import os


class StoneTookGame(object):
    """
    石取りゲームを行うクラス
    石の数を管理する
    メンバ変数の値
    __stone_num:int 石の最大値
    __get_max:int 石を取る数の最大値
    __now_num:int 現在の石の数
    """
    def __init__(self, stone_num:int, get_max:int):
        """
        stone_num:int 石の最大値
        get_max:取れる数の最大値
        """
        self.__stone_num = stone_num
        self.__stone_max = stone_num
        self.__get_max = get_max
        self.__now_num = self.stone_num
        self.__recorder = REC.Recorder(self.stone_max, self.get_max)
        
    @property
    def stone_num(self):
        return self.__stone_num
    
    @property
    def stone_max(self):
        return self.__stone_max
    
    @property
    def get_max(self):
        return self.__get_max
    
    @property
    def now_num(self):
        return self.__now_num
    
    @property
    def recorder(self):
        return self.__recorder
    
    def is_faul(self, took_stone:int)->bool:
        """
        とった石の数が0以下であったり所定の数以上であったかどうかを判定する
        反則はいけませんw
        反則があった場合True、そうでなければFalseを返す
        引数の説明
        took_stone:int 石をとった数
        """
        if took_stone < 1:
            return True
        if took_stone > self.get_max:
            return True
        return False
    
    def gotten_stone(self,
                     player:PL.Player,
                     pre_took:Optional[int] = None)->int:
        """
        プレイヤーに石を取られる操作
        取られた石の数を返す
        石の残りが1個以下のときは-1を返す
        """
        try:
            if self.now_num < 2:
                get_num = -1
                return -1
            get_num = player.get_stone(self.now_num,
                                       self.get_max,
                                       pre_took)
            if self.now_num < get_num - 1:
                get_num = self.now_num -1
            self.__now_num = self.now_num - get_num
            return get_num
        finally:
            self.__recorder.record(get_num)
            
            
    def record(self, csv_title:str = None ):
        if csv_title is None:
            return self.recorder.write_csv()
        return self.recorder.write_csv(file_name = csv_title)

    
def battle_one_term(nim:Nim,
                    player1:PL.Player,
                    player2:PL.Player)->Union[Tuple[str, int], str]:
    """
    Nimクラスのインスタンスを用いて対戦を行う
    返し値は(対戦相手の番号取った石の数のタプル)
    1対戦ごとに呼び出すジェネレータ形式
    nim:Nim 設定済みのNimのインスタンス
    player1:PL.Player 先手
    player2:PL.player 後手
    wait_time:int 石を撮った後待つ時間　視覚的に見せるときすぐに動かすと何が起こったかわからないため
    """    
    got_stone = None
    while nim.now_num > 1:
        got_stone = nim.gotten_stone(player1, got_stone)
        if (got_stone < 1) or (nim.now_num < 1):
            break            
        else:
            if nim.is_faul(got_stone):
                winner = player2.name
                break            
            yield ("player1 " + player1.name, got_stone)
        winner = player1.name
        got_stone = nim.gotten_stone(player2, got_stone)
        if (got_stone < 1) or (nim.now_num < 1):
            break
        else:
            if nim.is_faul(got_stone):
                winner = player1.name
                break                        
            yield ("player2 " + player2.name, got_stone)
        winner = player2.name                     
    yield winner

def battle(nim:Nim,
           player1:PL.Player,
           player2:PL.Player,
           write_path = os.path.join(os.getcwd(), "record")
           )->int:
    """
    GUIなしで戦う時のフィールド
    返し値は買ったプレイヤーの値
    """
    try:
        duel = battle_one_term(nim, player1, player2)
        print(player1.name, " vs ", player2.name)
        print("decide the destiny")        
        for result in duel:
            if type(result) == tuple:
                print(result[0], " took ", result[1])
            if type(result) is str:
                print(result, "win!")
                return result
    finally:
        title_base = player1.name+"_"+player2.name+str(nim.stone_max)+"_"+str(nim.get_max)+".csv"
        now_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")
        title = now_time+title_base
        nim.record(title)
        
        
def battle_field_builder(stone_num:int, get_max:int)->Callable[[PL.Player, PL.Player], int]:
    """
    設定された条件を元にしたNimのフィールドを生成する関数を返す
    そのままの設定だと一度しかそのフィールドは使えないため
    引数の説明
    stone_num:int 石の最大値
    get_max:取れる数の最大値
    """
    nim_field = Nim(stone_num, get_max)
    return lambda player1, player2: battle(nim_field, player1, player2)

