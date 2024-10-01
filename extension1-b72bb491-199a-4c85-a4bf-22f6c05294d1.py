""" CS 5001 -Yijia Zhan - Project 10 extension1
This defines the WoodConfig class, which represents configuration
parameters for the woods simulation.

*Define enjoy_var
"""


class WoodConfig:
    """Represents configuration parameters for a woods simulation.
    """
    def __init__(self, move_interval, tree_min, tree_max, baby_min, baby_max,
                 bird_min, bird_max, enjoy_var=False):
        """Initializes a new instance of the ForestConfig class.

        Args:
            tree_min (int): The minimum number of trees in the forest.
            tree_max (int): The maximum number of trees in the forest.
            baby_min (int): The minimum number of baby animals in the forest.
            baby_max (int): The maximum number of baby animals in the forest.
            bird_min (int): The minimum number of bird in the forest.
            bird_max (int): The maximum number of bird in the forest.
        """
        self.move_interval = move_interval
        self.tree_min = tree_min
        self.tree_max = tree_max
        self.baby_min = baby_min
        self.baby_max = baby_max
        self.bird_min = bird_min
        self.bird_max = bird_max
        self.enjoy_var = enjoy_var
