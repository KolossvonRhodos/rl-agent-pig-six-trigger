"""Training loop for the Q-learning Pig agent."""

from pig_game import PigGame
from dummy_player import ThresholdDummyPlayer
from settings import AGENT_PLAYER
from reward import standard_reward


def play_dummy_turns_until_agent_or_end(game, dummy_player):
    """
    Lets the dummy player act until:
    - the game is finished, or
    - it is the agent's turn again.
    """
    while not game.is_finished() and game.current_player != AGENT_PLAYER:
        state = game.get_state()
        legal_actions = game.get_legal_actions()

        action = dummy_player.choose_action(
            state=state,
            legal_actions=legal_actions
        )

        game.step(action)


def play_training_game(agent, dummy_player, reward_function, target_score=100, seed=None):
    """
    Plays one full training game:
    - Agent learns
    - Dummy does not learn
    """

    game = PigGame(target_score=target_score, seed=seed)

    while not game.is_finished():

        # If dummy starts, let dummy play until the agent is active
        if game.current_player != AGENT_PLAYER:
            play_dummy_turns_until_agent_or_end(game, dummy_player)
            continue

        # Agent turn
        state = game.get_state_key()
        legal_actions = game.get_legal_actions()

        action = agent.choose_action(
            state=state,
            legal_actions=legal_actions,
            training=True
        )

        game.step(action)

        # After the agent acts, the dummy may play.
        # We wait until the agent is active again or the game is finished.
        play_dummy_turns_until_agent_or_end(game, dummy_player)

        done = game.is_finished()
        reward = reward_function(game, AGENT_PLAYER)

        next_state = game.get_state_key()

        if done:
            next_legal_actions = []
        else:
            next_legal_actions = game.get_legal_actions()

        agent.update(
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            next_legal_actions=next_legal_actions,
            done=done
        )

    return game.winner


def train_agent(agent, episodes=10000, target_score=100, dummy_player=None, reward_function=None, seed=None):
    """
    Trains agent for a number of episodes.
    Returns basic training statistics.
    """

    if dummy_player is None:
        dummy_player = ThresholdDummyPlayer(hold_threshold=20)

    if reward_function is None:
        reward_function = standard_reward

    agent_wins = 0
    dummy_wins = 0

    for episode in range(episodes):
        episode_seed = None if seed is None else seed + episode

        winner = play_training_game(
            agent=agent,
            dummy_player=dummy_player,
            reward_function=reward_function,
            target_score=target_score,
            seed=episode_seed
        )

        if winner == AGENT_PLAYER:
            agent_wins += 1
        else:
            dummy_wins += 1

    return {
        "episodes": episodes,
        "agent_wins": agent_wins,
        "dummy_wins": dummy_wins,
        "agent_win_rate": agent_wins / episodes,
        "q_table_size": agent.get_q_table_size()
    }