# -*- coding: utf-8 -*-
from . import game
from ..player import sample as PS
from typing import Tuple
from typing import List

BATTLE_SETTING_SET = [(30, 4), (45, 4), (60, 4), (75, 4), (90, 4), (150, 4),
                      (30, 5), (45, 5), (60, 5), (75, 5), (90, 5), (150, 5),
                      (30, 6), (45, 6), (60, 6), (75, 6), (90, 6), (150, 6),
                      (30, 7), (45, 7), (60, 7), (75, 7), (90, 7), (150, 7)                      
                      ]

PLAYER_SETTING_SET = [(PS.player1, PS.player1), (PS.player1, PS.player2), (PS.player1, PS.player3),
                      (PS.player2, PS.player1), (PS.player2, PS.player2), (PS.player2, PS.player3),
                      (PS.player3, PS.player1), (PS.player3, PS.player2), (PS.player3, PS.player3)]

def battle(battle_setting:Tuple[int, int],
           player_setting:Tuple[PS.PL.Player, PS.PL.Player]):
    """
    それぞれのセッティングから対戦を行う
    プレイヤー1と2両方先制後攻を行う
    """
    battle_field = game.battle_field_builder(battle_setting[0], battle_setting[1])
    battle_field(player_setting[0], player_setting[1])
    battle_field = game.battle_field_builder(battle_setting[0], battle_setting[1])
    battle_field(player_setting[1], player_setting[0])
    
def battle_all_setting(battle_setting_set:List[Tuple[int, int]],
                       player_setting_set:List[Tuple[PS.PL.Player, PS.PL.Player]]):
    for battle_setting in battle_setting_set:
        for player_setting in player_setting_set:
            battle(battle_setting, player_setting)

def run():
    battle_all_setting(BATTLE_SETTING_SET, PLAYER_SETTING_SET)