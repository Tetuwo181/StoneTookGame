# -*- coding: utf-8 -*-
import csv
import os
from typing import List
import pandas as pd
import numpy as np


def convert_to_int_in_list(dataset):
    return [int(data) for data in dataset]

def build_player_log(dataset:List[List[int]])->pd.core.frame.DataFrame:
    """
    先手が勝者か後手が勝者か判定する
    (勝者のログ，敗者のログ)のpandas形式のデータフレームを返す
    """
    win = "init"
    last_log = dataset[-1]
    if last_log[1] == -1:
        winner = [data[0] for data in dataset[:]]
        remain_winner = [data[2] for data in dataset[:]]
        loser = [data[1] for data in dataset[:]]
        remain_loser = [data[3] for data in dataset[:]]
        win = "pre"
    else:
        winner = [data[1] for data in dataset[:]]
        remain_winner =[data[3] for data in dataset[:]]        
        loser = [data[0] for data in dataset[:]]    
        remain_loser = [data[2] for data in dataset[:]]
        win = "after"
    return pd.DataFrame({"win":winner, "lose":loser, "winner_term":win, "remain_winner":remain_winner, "remain_loser":remain_loser})
    

def load_nim_log(log_path:str)->pd.core.frame.DataFrame:
    """
    指定したパスのログを読み込む
    返し値は(石をとった数,　勝者ログ, 敗者ログ)という属性の
    pandas形式のデータフレーム
    """
    with open(log_path, "r") as csv_data:
        raw_dataset = csv.reader(csv_data)
        converted = [convert_to_int_in_list(data) for data in raw_dataset]
        input_header = converted[0][1:]
        base_df = build_player_log(converted[1:])
        return pd.DataFrame({"get_max": input_header[1],
                             "stone_max": input_header[0],
                             "win": base_df.win,
                             "remain_winner":base_df.remain_winner,
                             "lose": base_df.lose,
                             "remain_loser":base_df.remain_loser,
                             "winner_term":base_df.winner_term})
        

def load_data_log_by_max_stone(log_dir_path:str, stone_max:int)->List[str]:
    """
    指定したフォルダのパスから石をとることができる数の上限を指定して、
    当該するログのパスを取得する
    """
    datalog_pathes =[path for path in os.chdir(log_dir_path)
                     if path[-3:] == "csv"]
    is_max_path = lambda path: path[:-4].split("_")[-1] == str(stone_max)
    return [path for path in datalog_pathes
            if is_max_path(path)]
    
