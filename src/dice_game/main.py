"""Command-line interface for the Pig Q-learning project."""

import q_agent
from pig_game import PigGame
from dummy_player import create_dummy
from trainer import train_agent
from evaluation import evaluate_agent
from reward import standard_reward
from experiments import (
    experiment_training_iterations,
    experiment_dummy_strategies,
    experiment_epsilon_values,
    experiment_reward_functions,
    experiment_target_scores,
    run_all_experiments,
    save_results_to_csv,
)
import settings
from policy_stats import experiment_policy_statistics


def create_agent():
    """Create a Q-learning agent with the default settings."""
    return q_agent.QAgent(
        alpha=settings.ALPHA,
        gamma=settings.GAMMA,
        epsilon=settings.EPSILON,
        seed=settings.SEED
    )


def train_default_agent(agent=None):
    """Train a default agent or continue training an existing one."""
    if agent is None:
        agent = create_agent()

    dummy = create_dummy("balanced", seed=settings.SEED)

    print("Training agent...")

    stats = train_agent(
        agent=agent,
        episodes=settings.PARAMETER_EXPERIMENT_TRAINING_EPISODES,
        target_score=settings.TARGET_SCORE,
        dummy_player=dummy,
        reward_function=standard_reward,
        seed=settings.SEED
    )

    print("Training finished.")
    print(stats)

    return agent

def evaluate_current_agent(agent):
    """Evaluate the currently trained agent against the balanced dummy."""
    if agent is None:
        print("No trained agent available. Train an agent first.")
        return

    dummy = create_dummy("balanced", seed=settings.SEED)

    stats = evaluate_agent(
        agent=agent,
        dummy_player=dummy,
        games=settings.EVALUATION_EPISODES,
        target_score=settings.TARGET_SCORE,
        seed=settings.SEED
    )

    print("Evaluation result:")
    print(stats)


def play_against_agent(agent):
    """Start an interactive CLI game against the trained agent."""
    if agent is None:
        print("No trained agent available. Train an agent first.")
        return

    game = PigGame(
        target_score=settings.TARGET_SCORE,
        seed=settings.SEED
    )

    human_player = 0
    computer_player = 1

    print("Game started.")
    print("You are Player 0. The computer is Player 1.")

    while not game.is_finished():
        game.print_status()
        legal_actions = game.get_legal_actions()

        if game.current_player == human_player:
            print(f"Legal actions: {legal_actions}")

            while True:
                action = input("Choose action (roll/hold): ").strip().lower()

                if action in legal_actions:
                    break

                print("Invalid action. Try again.")

            _, info = game.step(action)
            print(info["message"])

        elif game.current_player == computer_player:
            state_key = game.get_state_key()

            action = agent.choose_action(
                state=state_key,
                legal_actions=legal_actions,
                training=False
            )

            print(f"Computer chooses: {action}")

            _, info = game.step(action)
            print(info["message"])

    print("------------------------")
    print(f"Final score Player 0: {game.scores[0]}")
    print(f"Final score Player 1: {game.scores[1]}")

    if game.winner == human_player:
        print("You won.")
    else:
        print("Computer won.")


def run_single_experiment_menu():
    """Open the experiment submenu and save the selected result CSV."""
    print("------------------------")
    print("Choose experiment:")
    print("1. Training iterations")
    print("2. Dummy strategies")
    print("3. Epsilon values")
    print("4. Reward functions")
    print("5. Target scores")
    print("6. Policy statistics")
    print("7. All experiments")
    print("------------------------")

    choice = input("Choice: ").strip()

    if choice == "1":
        results = experiment_training_iterations()
        save_results_to_csv(results, "training_iterations_results.csv")

    elif choice == "2":
        results = experiment_dummy_strategies()
        save_results_to_csv(results, "dummy_strategy_results.csv")

    elif choice == "3":
        results = experiment_epsilon_values()
        save_results_to_csv(results, "epsilon_results.csv")

    elif choice == "4":
        results = experiment_reward_functions()
        save_results_to_csv(results, "reward_function_results.csv")

    elif choice == "5":
        results = experiment_target_scores()
        save_results_to_csv(results, "target_score_results.csv")

    elif choice == "6":
        results = experiment_policy_statistics()
        save_results_to_csv(results, "policy_statistics.csv")

    elif choice == "7":
        run_all_experiments()

    else:
        print("Invalid choice.")


def main():
    """Run the main command-line menu."""
    agent = None

    while True:
        print("------------------------")
        print("Pig Dice Game - Q-Learning")
        print("1. Train default agent")
        print("2. Evaluate current agent")
        print("3. Play against trained agent")
        print("4. Run experiments")
        print("5. Exit")
        print("------------------------")

        choice = input("Choice: ").strip()

        if choice == "1":
            agent = train_default_agent(agent)

        elif choice == "2":
            evaluate_current_agent(agent)

        elif choice == "3":
            play_against_agent(agent)

        elif choice == "4":
            run_single_experiment_menu()

        elif choice == "5":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()