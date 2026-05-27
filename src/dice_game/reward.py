def standard_reward(game, agent_player):
    if not game.is_finished():
        return 0

    if game.winner == agent_player:
        return 1

    return -1

def step_penalty_reward(game, agent_player):
    if not game.is_finished():
        return -0.01

    if game.winner == agent_player:
        return 1

    return -1

def get_reward_function(name):
    if name == "standard":
        return standard_reward

    if name == "step_penalty":
        return step_penalty_reward

    raise ValueError(f"Unknown reward function: {name}")