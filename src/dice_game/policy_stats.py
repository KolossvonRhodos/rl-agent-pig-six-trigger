"""Policy inspection utilities for the trained Q-learning agent."""

from pig_game import ROLL, HOLD
from dummy_player import create_dummy
from reward import standard_reward
from trainer import train_agent
import settings, q_agent


def analyze_policy(agent):
    """Inspect the agent's preferred action for selected example states.

    The score values are converted to the same bucketed state representation
    used during training. This keeps policy analysis consistent with the
    learned Q-table.
    """
    own_scores = [20, 50, 80]
    opponent_scores = [20, 50, 80]
    turn_totals = [0, 5, 10, 15, 20, 25, 30]

    rows = []

    for own_score in own_scores:
        for opponent_score in opponent_scores:
            for turn_total in turn_totals:
                state = (
                    own_score // settings.STATE_BUCKET_SIZE,
                    opponent_score // settings.STATE_BUCKET_SIZE,
                    turn_total // settings.STATE_BUCKET_SIZE,
                    False
                )

                # Holding is not legal before the player has gained turn points.
                if turn_total == 0:
                    legal_actions = [ROLL]
                else:
                    legal_actions = [ROLL, HOLD]

                action = agent.get_policy_action(state, legal_actions)

                rows.append({
                    "own_score": own_score,
                    "opponent_score": opponent_score,
                    "turn_total": turn_total,
                    "preferred_action": action,
                })

    return rows

def experiment_policy_statistics():
    """Train a default agent and return policy-statistic rows for CSV export."""
    agent = q_agent.QAgent(
        alpha=settings.ALPHA,
        gamma=settings.GAMMA,
        epsilon=settings.EPSILON,
        seed=settings.SEED
    )

    train_dummy = create_dummy("balanced", seed=settings.SEED)

    train_agent(
        agent=agent,
        episodes=settings.PARAMETER_EXPERIMENT_TRAINING_EPISODES,
        target_score=settings.TARGET_SCORE,
        dummy_player=train_dummy,
        reward_function=standard_reward,
        seed=settings.SEED
    )

    rows = analyze_policy(agent)

    for row in rows:
        print(row)

    return rows