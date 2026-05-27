"""Game environment for the six-trigger Pig dice game.

The environment contains only the game rules. It does not know anything about
Q-learning. Agents, dummy players and human players interact with it through
legal actions and the step() method.
"""

import random

from settings import STATE_BUCKET_SIZE

ROLL = "roll"
HOLD = "hold"

class PigGame:
    """Two-player six-trigger Pig environment.

        The six-trigger rule means that rolling a 6 forces the current player to
        roll again before holding. This makes the legal action set depend on the
        current state.
        """

    def __init__(self, target_score=100, seed=None):
        """Create a new game environment.

        Args:
            target_score: Score needed to win the game.
            seed: Optional random seed for reproducible dice rolls.
        """
        self.target_score = target_score
        self.random = random.Random(seed)
        self.reset()


    def reset(self, starting_player=None):
        """Reset the game state and return the initial state.

        Args:
            starting_player: Optional fixed starting player. If it is None,
                the starting player is chosen randomly.
        """
        self.scores = [0,0]

        if starting_player is None:
            self.current_player = self.random.randint(0,1)
        else:
            self.current_player = starting_player

        self.turn_total = 0
        self.forced_roll = False
        self.winner = None
        return self.get_state()

    def get_state(self):
        """Return the current state from the active player's perspective."""
        opponent = 1 - self.current_player

        return{
            "current_player": self.current_player,
            "own_score": self.scores[self.current_player],
            "opponent_score": self.scores[opponent],
            "turn_total": self.turn_total,
            "forced_roll": self.forced_roll
        }

    def get_state_key(self, bucket_size=STATE_BUCKET_SIZE):
        """Return a compact Q-table state representation.

        Design decision:
        Exact scores created a very large Q-table. Therefore, scores and turn
        totals are grouped into buckets. This gives the tabular agent some
        generalization between similar states.
        """
        opponent = 1 - self.current_player

        own_score = self.scores[self.current_player]
        opponent_score = self.scores[opponent]

        own_bucket = own_score // bucket_size
        opponent_bucket = opponent_score // bucket_size
        turn_bucket = self.turn_total // bucket_size

        return (
            own_bucket,
            opponent_bucket,
            turn_bucket,
            self.forced_roll
        )

    def get_legal_actions(self):
        """Return the actions allowed in the current state."""
        if self.forced_roll or self.turn_total == 0:
            return [ROLL]

        return [ROLL, HOLD]

    def step(self, action):
        """Apply one action and return the new state plus action information."""
        if self.winner is not None:
            raise ValueError("Game is already over.")

        if action not in self.get_legal_actions():
            raise ValueError(f"Invalid action. : {action}")

        if action == ROLL:
            return self._roll()

        if action == HOLD:
            return self._hold()


    def _roll(self):
        """Handle the game logic for rolling the dice."""
        dice = self.random.randint(1,6)

        info = {
            "action": ROLL,
            "dice": dice,
            "message": "",
            "winner": None
        }

        if dice == 1:
            self.turn_total = 0
            self.forced_roll = False
            info["message"] = "You rolled 1. Turntotal Lost!"
            self._switch_player()
            return self.get_state(), info

        self.turn_total += dice

        if dice == 6:
            self.forced_roll = True
            info["message"] = "You rolled 6. Forced to roll again!"
        else:
            self.forced_roll = False
            info["message"] = f"Rolled {dice}."

        return self.get_state(), info

    def _hold(self):
        """Add the turn score to the current player's total score."""
        self.scores[self.current_player] += self.turn_total

        info = {
            "action": HOLD,
            "dice": None,
            "message": f"Player {self.current_player} holds.",
            "winner": None
        }

        if self.scores[self.current_player] >= self.target_score:
            self.winner = self.current_player
            info["winner"] = self.winner
            info["message"] = f"Player {self.current_player} wins."
            return self.get_state(), info

        self.turn_total = 0
        self.forced_roll = False
        self._switch_player()

        return self.get_state(), info

    def _switch_player(self):
        """Switch the active player."""
        self.current_player = 1 - self.current_player

    def is_finished(self):
        """Return True if the game already has a winner."""
        return self.winner is not None

    def print_status(self):
        """Print the current game state for the command-line interface."""
        print("------------------------")
        print(f"Player 0 score: {self.scores[0]}")
        print(f"Player 1 score: {self.scores[1]}")
        print(f"Current player: {self.current_player}")
        print(f"Turn total: {self.turn_total}")
        print(f"Forced roll: {self.forced_roll}")
        print("------------------------")