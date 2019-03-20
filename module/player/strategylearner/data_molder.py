# -*- coding: utf-8 -*-

from ...recorder import data_loader as DL 
import pandas as pd
import numpy as np
from typing import Callable
from typing import List


"""
学習させるデータを成形する
例えば、石をとることができる数が4だとすると
数字の1がオリジナルのデータなら
[1.0, 0.0, 0.0, 0.0]という
numpy.ndarrayが返ってくる
"""

def data_molder(stone_max:int, noize_coefficient:float = 0)->Callable[[int], np.ndarray]:
    """
    データを成形する関数を返す
    stone_max:石をとることのできる最大値
    　　　　　　　　出力するデータの次元数を決定することになる
    """
    def molding(value:int)->np.ndarray:
        converter = lambda x: 1 if x == value else 0
        converted = np.array([converter(index+1) for index in range(int(stone_max))], dtype=float)
        return converted + noize_coefficient*(np.random.rand(stone_max)-0.5)
    return molding


def dataset_molder(stone_max:int, noize_coefficient:float = 0)->Callable[[List[int]], List[np.ndarray]]:
    """
    データのリストを成形する関数を返す
    stone_max:石をとることのできる最大値
    　　　　　　　　出力するデータの次元数を決定することになる
    """
    molder = data_molder(stone_max, noize_coefficient)
    def molding(dataset:List[int])->List[np.ndarray]:
        return [molder(data) for data in dataset]
    return molding


def timeseries_molder(time_num:int = 3)->Callable[[List[np.ndarray]], List[List[np.ndarray]]]:
    def converter(base:[List[np.ndarray]])->List[List[np.ndarray]]:
        result = []
        for index in range(len(base)-time_num):
            result.append(base[index:index+time_num])
        return result
    return converter


def convert_for_three_nnw(base_data:pd.core.frame.DataFrame, noize_coefficient:float = 0)->pd.core.frame.DataFrame:
    """
    オリジナルのデータを読み込んでそれを
    シンプルな入力のニューラルネットワークへ代入できるように変換
    入力データフレームのカラム
    stone_max: 石をとることができる最大値
    win: 勝者　これを教師データに
    lose: 敗者　これを入力データに
    """
    input_converter = dataset_molder(base_data.get_max[0], noize_coefficient)
    teacher_converter = dataset_molder(base_data.get_max[0])
    if base_data.winner_term[0] == "pre":
        teacher_base = base_data.win.values[1:]
        input_base = base_data.lose.values[:-1]
    else:
        teacher_base = base_data.win.values[:]
        input_base = base_data.lose.values[:]        
    return pd.DataFrame({"stone_max":base_data.stone_max[0],
                         "get_max":base_data.get_max[0],
                         "teacher":teacher_converter(base_data.win.values),
                         "input":input_converter(base_data.lose.values)})

    
def convert_for_timeseries_nnw(base_data:pd.core.frame.DataFrame,
                               time_num:int = 3)->pd.core.frame.DataFrame:
    simple_df = convert_for_three_nnw(base_data)
    converter = timeseries_molder(time_num)
    return pd.DataFrame({"stone_max":simple_df.stone_max[0],
                         "teacher":converter(simple_df.teacher.values),
                         "input":converter(simple_df.input[time_num:])})
    