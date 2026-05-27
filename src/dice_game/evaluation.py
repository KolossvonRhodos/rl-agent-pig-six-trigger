"""Evaluation utilities for trained Q-learning agents."""

from pig_game import PigGame
from settings import AGENT_PLAYER, DUMMY_PLAYER


def evaluate_agent(agent, dummy_player, games=1000, target_score=100, seed=None):
    """Evaluate a trained agent without exploration.

    The agent uses its learned policy, while the dummy player follows its fixed
    strategy. The returned metrics are used for experiment comparison.
    """
    agent_wins = 0
    total_turns = 0
    total_score_difference = 0

    for game_index in range(games):
        episode_seed = None if seed is None else seed+game_index
        game = PigGame(target_score=target_score, seed=episode_seed)

        turns = 0

        while not game.is_finished():
            state = game.get_state()
            legal_actions = game.get_legal_actions()

            if game.current_player == AGENT_PLAYER:
                state_key = game.get_state_key()
                action = agent.choose_action(
                    state=state_key,
                    legal_actions=legal_actions,
                    training=False
                )
            else:
                action = dummy_player.choose_action(state, legal_actions)

            game.step(action)
            turns += 1

        if game.winner == AGENT_PLAYER:
            agent_wins += 1

        score_difference = game.scores[AGENT_PLAYER] - game.scores[DUMMY_PLAYER]
        total_score_difference += score_difference
        total_turns += turns

    return {
        "evaluation_games": games,
        "agent_wins": agent_wins,
        "win_rate": agent_wins/games,
        "avg_turns": total_turns/games,
        "avg_score_difference": total_score_difference/games,
        "q_table_size": agent.get_q_table_size(),
    }
