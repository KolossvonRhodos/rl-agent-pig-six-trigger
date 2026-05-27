# General settings #
TARGET_SCORE = 100
SEED = 42
STATE_BUCKET_SIZE = 5

RESULTS_FOLDER = "results"

AGENT_PLAYER = 0
DUMMY_PLAYER = 1

# Q-learning default params
ALPHA = 0.1
GAMMA = 0.95
EPSILON = 0.1

# Training / eval
EVALUATION_EPISODES = 1000

TRAINING_EPISODE_OPTIONS = [
    1000,
    5000,
    10000,
    50000
]

EPSILON_OPTIONS = [
    0.05,
    0.10,
    0.20
]

DUMMY_STRATEGIES = {
    "safe": 10,
    "balanced": 20,
    "risky": 30,
    "random": None
}

DUMMY_EXPERIMENT_TRAINING_EPISODES = 10000

# Additional experiment settings
PARAMETER_EXPERIMENT_TRAINING_EPISODES = 10000

TARGET_SCORE_OPTIONS = [
    50,
    100,
    150
]

REWARD_FUNCTION_OPTIONS = [
    "standard",
    "step_penalty"
]