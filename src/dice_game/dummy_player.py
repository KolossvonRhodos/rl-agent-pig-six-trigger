import random

from pig_game import ROLL, HOLD
import settings

class ThresholdDummyPlayer:

    def __init__(self, hold_threshold=20):
        self.hold_threshold = hold_threshold

    def choose_action(self, state, legal_actions):
        if HOLD in legal_actions and state["turn_total"] >= self.hold_threshold:
            return HOLD

        return ROLL

class RandomDummyPlayer:
    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def choose_action(self, state, legal_actions):
        return self.random.choice(legal_actions)

def create_dummy(name, seed=None):
    if name not in settings.DUMMY_STRATEGIES:
        raise ValueError(f"Unknown dummy strategy: {name}")

    threshold = settings.DUMMY_STRATEGIES[name]

    if threshold is None:
        return RandomDummyPlayer(seed=seed)

    return ThresholdDummyPlayer(hold_threshold=threshold)

