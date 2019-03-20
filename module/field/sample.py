# -*- coding: utf-8 -*-

from . import game
from ..player import sample as PS



def sample_battle():
    """
    最強戦略どうし、
    石の最大値30、取れる数4で戦う
    """
    player1 = PS.player2
    player2 = PS.player2
    duel_base = game.Nim(30, 4)
    return game.battle(duel_base, player1, player2)

def sample_battle2():
    """
    最強戦略vsランダム
    石の最大値30、取れる数4で戦う
    """
    player1 = PS.player1
    player2 = PS.player2
    duel_base = game.Nim(30, 4)
    return game.battle(duel_base, player1, player2)