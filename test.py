#!/usr/bin/env python
import enum
import random

# TODO
# problèmes suivants relevés:
#

class Color(enum.IntEnum):
    """Represent a team color
    """
    RED = 1
    BLUE = 2
    DARK = 3
    NEUTRAL = 4


class TurnType(enum.Enum):
    """Represent a type of turn, either 'guess' or 'play'"""
    GUESS = enum.auto()
    PROPOSAL = enum.auto()
    GAME_OVER = enum.auto()


class Card:

    def __init__(self, t, c):
        # sanity checks
        if not isinstance(c, Color):
            raise TypeError('Given color is not of type Color:', c)

        self.text = t
        self.color = c

    def __str__(self):
        """Return text"""
        return ";".join([str(self.text), str(self.color)])


class Player:
    """Represent a player"""

    def __init__(self, player_id, name, r, c):
        # attributes forever
        if not isinstance(c, Color):
            raise TypeError('Given color is not of type Color:', c)

        self.name = name
        self.color = c
        self.role = r
        self.player_id = player_id

    def __str__(self):
        """Return id, name"""
        return "; ".join([str(self.player_id), self.name])

if __name__=="__main__":
    Color.RED
    Color["RED"]
    Color(1)
