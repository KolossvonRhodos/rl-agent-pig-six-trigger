# Q-Learning for Six-Trigger Pig Dice Game

This project implements a tabular Q-learning agent for the six-trigger variant of the Pig dice game.  
The agent learns from scratch by playing simulated games against dummy players. After training, it can be evaluated, used in experiments, or played against in the command-line interface.

No external reinforcement learning libraries are used.

## Requirements

- Python 3.x
- No additional packages required

Only Python standard library modules are used.

## Project Structure

```text
src/dice_game/
├── main.py             # CLI entry point
├── settings.py         # central parameters and experiment settings
├── pig_game.py         # six-trigger Pig game environment
├── q_agent.py          # tabular Q-learning agent
├── dummy_player.py     # dummy opponent strategies
├── reward.py           # reward functions
├── trainer.py          # training loop
├── evaluation.py       # evaluation logic
├── experiments.py      # experiment runners and CSV export
├── policy_stats.py     # policy inspection
└── __init__.py         # package marker
```

## How to Run

From the project root:

```bash
python src/dice_game/main.py
```

Or from inside the source folder:

```bash
cd src/dice_game
python main.py
```

## CLI Usage

After starting `main.py`, the menu offers:

```text
1. Train default agent
2. Evaluate current agent
3. Play against trained agent
4. Run experiments
5. Exit
```

Typical workflow:

1. Choose `1` to train the agent.
2. Choose `2` to evaluate the trained agent.
3. Choose `3` to play against the trained agent.
4. Choose `4` to run experiments.

For the human game mode, enter:

```text
roll
hold
```

The program only accepts legal actions. For example, after rolling a 6, the six-trigger rule forces another roll.

## Important Settings

Most important values are configured in `settings.py`.

```python
TARGET_SCORE = 100
SEED = 42
STATE_BUCKET_SIZE = 5

ALPHA = 0.1
GAMMA = 0.95
EPSILON = 0.1

EVALUATION_EPISODES = 1000
```

Dummy strategies:

```python
DUMMY_STRATEGIES = {
    "safe": 10,
    "balanced": 20,
    "risky": 30,
    "random": None,
}
```

Meaning:

- `safe`: holds when `turn_total >= 10`
- `balanced`: holds when `turn_total >= 20`
- `risky`: holds when `turn_total >= 30`
- `random`: chooses randomly between legal actions

## Experiments

Experiments can be run through the CLI:

```text
4. Run experiments
```

Experiment menu:

```text
1. Training iterations
2. Dummy strategies
3. Epsilon values
4. Reward functions
5. Target scores
6. Policy statistics
7. All experiments
```

Alternatively, all experiments can be run directly:

```bash
python src/dice_game/experiments.py
```

The results are saved as CSV files in the `results/` folder.

Generated files include:

```text
results/training_iterations_results.csv
results/dummy_strategy_results.csv
results/epsilon_results.csv
results/reward_function_results.csv
results/target_score_results.csv
results/policy_statistics.csv
results/all_experiment_results.csv
```

## Reproducibility

The project uses a fixed seed from `settings.py`:

```python
SEED = 42
```

To reproduce the results, keep the same settings and run the experiments again.  
Changing values in `settings.py` changes the experiment setup.
