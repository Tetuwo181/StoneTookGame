# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime
from typing import List

class Recorder(object):
    def __init__(self, stone_max:int, get_max:int):
        self.__tern = 0
        self.__stone_max = stone_max
        self.__get_max = get_max
        self.__first = []
        self.__second = []
    
    @property
    def tern(self)->int:
        return self.__tern
    
    @property
    def battel_num(self)->int:
        """
        先手後手1セットを行った回数
        """
        if self.tern % 2 == 0:
            return int(self.tern/2)
        else:
            return int(self.tern/2) + 1
    
    @property
    def first(self)->List[int]:
        return self.__first
    
    @property
    def second(self)->List[int]:
        return self.__second
    
    def record(self, point:int):
        try:
            if self.tern % 2 == 0:            
                self.__first.append(point)
            else:            
                self.__second.append(point)
        finally:
            self.__tern = self.__tern + 1
    
    def write_csv(self
                  ,dir_path:str = os.path.join(os.getcwd(), "record")
                  ,file_name:str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
                  ):
        """
        結果を書き出す
        header行に石を取りあう回数を書く
        """
        if os.path.exists(dir_path) is False:
            os.mkdir(dir_path)
        file_path = os.path.join(dir_path, file_name)
        if self.tern%2 == 0:
            write_dataset = zip(self.first, self.second)
        else:
            second_base = self.second+[-1]
            write_dataset = zip(self.first, second_base)
        with open(file_path, "w", encoding="utf-8") as result_file:
            result_writer = csv.writer(result_file, lineterminator='\n')
            result_writer.writerow([self.battel_num, self.__stone_max, self.__get_max])
            converted = []
            for data in write_dataset:
                converted.append(list(data))   
            result_writer.writerows(converted)
        

            