# -*- coding: utf-8 -*-
"""
色々なネットワークを使って
学習した結果を比較してみる
基本的なI/Oに関して
入力層のニューロン数:取れる石の数
出力層のニューロン数:取れる石の数
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import InputLayer
from keras.layers import LSTM
import numpy as np
import pandas as pd
from module.player.strategylearner import data_molder as DM

def build_three_layerNNW(stone_max:int,
                         middle_layer_num:int,
                         hidden_activation:str = "relu",
                         output_activation:str = "softmax"
                       ):
    """
    3層ニューラルネットワークのモデルを作成する
    引数の説明
    stone_max:取れる石の最大値　入力層と出力層の値と対応
    middle_layer_num: 中間層の数
    hidden_activation: 中間層の活性化関数　デフォルトはReLU
    outpur_activation:出力層の活性化関数　デフォルトはソフトマックス関数
    """
    model = Sequential()
    model.add(
            Dense(middle_layer_num,
                  input_dim = stone_max,
                  activation = hidden_activation)
    )
    model.add(Dense(stone_max, activation = output_activation))
    return model
    

def buildLSTM(stone_max:int,
               time_length:int,
               hidden_num:int = 128,
               dropout_rate:float = 0.5,
               activation_lstm:str = "tanh",
               output_activation:str = "soft_max"):
    """
    石の数と石を取ることができる数の最大値を入力のベースにする
    出力は取る石の数のため、出力層の数はget_max個になる
    """
    model = Sequential()
    model.add(InputLayer(batch_input_shape=(None, time_length, stone_max))) 
    model.add(LSTM(hidden_num, 
                   activation = activation_lstm))
    model.add(Dense(stone_max, activation = output_activation))

    return model
    
def set_compile_conf(model, 
                     optimizer_func:str = "adam", 
                     loss_func:str = "hinge"):
    model.compile(optimizer = optimizer_func, loss = loss_func)
    return model

def learn(testdata:pd.DataFrame,
          model):
    model.fit(testdata.input, testdata.teacher)

def build_learn_strategy(model,
                         stone_max:int,
                         show_result:bool = False):
    """
    Playerに渡すことができるような形式にする
    学習済みのモデルと石をとることができる数の最大値を引数として渡す
    """
    record = []
    converter = DM.data_molder(stone_max)
    def strategy(pretook_stone:int)->int:
        record.append(pretook_stone)
        input_val = np.array([converter(pretook_stone)])
        raw_result = model.predict(input_val)
        result = 1
        biggest_value = raw_result[0][0]
        for index, value in enumerate(raw_result[0][1:]):
            if biggest_value < value:
                biggest_value = value
                result = index + 2
        if show_result:
            print(raw_result, result)           
        return result
    return strategy
        
