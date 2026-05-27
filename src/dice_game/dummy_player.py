"""Dummy opponent strategies used for training and evaluation.

Dummy players do not learn. They provide fixed opponent behavior so that the
Q-agent can train through repeated simulated games.
"""

import random

from pig_game import ROLL, HOLD
import settings

class ThresholdDummyPlayer:
    """Dummy player that holds after reaching a fixed turn total."""

    def __init__(self, hold_threshold=20):
        """Create a threshold-based dummy player."""
        self.hold_threshold = hold_threshold

    def choose_action(self, state, legal_actions):
        """Choose HOLD if the threshold is reached, otherwise choose ROLL."""
        if HOLD in legal_actions and state["turn_total"] >= self.hold_threshold:
            return HOLD

        return ROLL


class RandomDummyPlayer:
    """Dummy player that selects randomly between legal actions."""
    def __init__(self, seed=None):
        """Create a random dummy player with an optional seed."""
        self.random = random.Random(seed)

    def choose_action(self, state, legal_actions):
        """Choose a random legal action.

        The state argument is accepted for the same interface as other players,
        but the random dummy does not use it.
        """
        return self.random.choice(legal_actions)

def create_dummy(name, seed=None):
    """Create a dummy player by strategy name.

    The thresholds are configured in settings.DUMMY_STRATEGIES. A value of None
    means that the random dummy strategy should be used.
    """
    if name not in settings.DUMMY_STRATEGIES:
        raise ValueError(f"Unknown dummy strategy: {name}")

    threshold = settings.DUMMY_STRATEGIES[name]

    if threshold is None:
        return RandomDummyPlayer(seed=seed)

    return ThresholdDummyPlayer(hold_threshold=threshold)

