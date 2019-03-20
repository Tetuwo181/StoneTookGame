# -*- coding: utf-8 -*-
from . import player as PL
from . import strategies as ST

player1 = PL.Player(ST.random.strategy, "random")
player2 = PL.Player(ST.strongest.strategy, "strongest")
player3 = PL.Player(ST.one_took.strategy, "one_took")