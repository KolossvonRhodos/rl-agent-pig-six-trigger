import random

from pig_game import ROLL, HOLD
import settings


class QAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.1, seed=None):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.random = random.Random(seed)
        self.fallback_hold_threshold = 20

    def get_q_value(self, state, action, create=True):
        """
        Returns the Q value for the given state and action.
        If state is unknown, init with Q-values 0
        """

        if state not in self.q_table:
            if not create:
                return 0

            self.q_table[state] = {
                ROLL: 0.0,
                HOLD: 0.0,
            }

        return self.q_table[state][action]

    def choose_action(self, state, legal_actions, training=True):
        """
        Chooses an action.

        During Training:
        - sometimes chooses rand for exploration
        - otherwise chooses best known action

        During Eval:
        - always chooses best known action
        """

        if training and self.random.random() < self.epsilon:
            return self.random.choice(legal_actions)

        if not training and state not in self.q_table:
            return self.fallback_action(state, legal_actions)

        return self.best_action(state, legal_actions, create=training)

    def best_action(self, state, legal_actions, create=False):
        """
        Returns the action with highest Q-value.
        If multiple actions with same val, choose randomly.
        """

        best_value = max(
            self.get_q_value(state, action, create=create)
            for action in legal_actions
        )

        best_actions = [
            action for action in legal_actions
            if self.get_q_value(state, action, create=create) == best_value
        ]

        return self.random.choice(best_actions)

    def update(self, state, action, reward, next_state, next_legal_actions, done):
        """
        Applies Q-Learning update formular
        """

        old_q = self.get_q_value(state, action)

        if done:
            target = reward
        else:
            best_next_q = max(
                self.get_q_value(next_state, next_action)
                for next_action in next_legal_actions
            )
            target = reward + self.gamma * best_next_q

        new_q = old_q + self.alpha * (target - old_q)
        self.q_table[state][action] = new_q

    def get_policy_action(self, state, legal_actions):
        """
        Returns learned policy action.
        Used after Training
        """
        return self.choose_action(state, legal_actions, training=False)

    def get_q_table_size(self):
        return len(self.q_table)

    def fallback_action(self, state, legal_actions):
        turn_total_bucket = state[2]
        estimated_turn_total = turn_total_bucket * settings.STATE_BUCKET_SIZE

        if HOLD in legal_actions and estimated_turn_total >= self.fallback_hold_threshold:
            return HOLD

        return ROLL