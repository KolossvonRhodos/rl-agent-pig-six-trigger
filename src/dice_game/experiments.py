import csv
from pathlib import Path

from q_agent import QAgent
from dummy_player import create_dummy
from trainer import train_agent
from evaluation import evaluate_agent
from reward import standard_reward, get_reward_function
from policy_stats import experiment_policy_statistics
import settings

def experiment_training_iterations():
    results = []

    for episodes in settings.TRAINING_EPISODE_OPTIONS:
        result = run_training_and_evaluation(
            experiment_name="training_iterations",
            training_episodes=episodes,
            epsilon=settings.EPSILON,
            target_score=settings.TARGET_SCORE,
            train_dummy_name="balanced",
            eval_dummy_name="balanced",
            reward_name="standard",
            seed=settings.SEED
        )

        results.append(result)
        print(result)

    return results

def experiment_dummy_strategies():
    results = []

    for train_dummy_name in settings.DUMMY_STRATEGIES.keys():
        for eval_dummy_name in settings.DUMMY_STRATEGIES.keys():
            result = run_training_and_evaluation(
                experiment_name="dummy_strategies",
                training_episodes=settings.DUMMY_EXPERIMENT_TRAINING_EPISODES,
                epsilon=settings.EPSILON,
                target_score=settings.TARGET_SCORE,
                train_dummy_name=train_dummy_name,
                eval_dummy_name=eval_dummy_name,
                reward_name="standard",
                seed=settings.SEED
            )

            results.append(result)
            print(result)

    return results

def run_training_and_evaluation(
        experiment_name,
        training_episodes,
        alpha=None,
        gamma=None,
        epsilon=None,
        target_score=None,
        train_dummy_name="balanced",
        eval_dummy_name="balanced",
        reward_name="standard",
        seed=None
):

    if alpha is None:
        alpha = settings.ALPHA

    if gamma is None:
        gamma = settings.GAMMA

    if epsilon is None:
        epsilon = settings.EPSILON

    if target_score is None:
        target_score = settings.TARGET_SCORE

    if seed is None:
        seed = settings.SEED

    agent = QAgent(
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        seed=seed
    )

    train_dummy = create_dummy(train_dummy_name, seed=seed)
    eval_dummy = create_dummy(eval_dummy_name, seed=seed)
    reward_function = get_reward_function(reward_name)

    train_stats = train_agent(
        agent=agent,
        episodes=training_episodes,
        target_score=target_score,
        dummy_player=train_dummy,
        reward_function=reward_function,
        seed=seed
    )

    eval_stats = evaluate_agent(
        agent=agent,
        dummy_player=eval_dummy,
        games=settings.EVALUATION_EPISODES,
        target_score=target_score,
        seed=seed
    )

    return {
        "experiment": experiment_name,
        "training_episodes": training_episodes,
        "target_score": target_score,
        "alpha": alpha,
        "gamma": gamma,
        "epsilon": epsilon,
        "train_dummy": train_dummy_name,
        "eval_dummy": eval_dummy_name,
        "reward_function": reward_name,
        "training_win_rate": train_stats["agent_win_rate"],
        "evaluation_win_rate": eval_stats["win_rate"],
        "avg_turns": eval_stats["avg_turns"],
        "avg_score_difference": eval_stats["avg_score_difference"],
        "q_table_size": eval_stats["q_table_size"],
    }

def experiment_epsilon_values():
    results = []

    for epsilon in settings.EPSILON_OPTIONS:
        result = run_training_and_evaluation(
            experiment_name="epsilon_values",
            training_episodes=settings.PARAMETER_EXPERIMENT_TRAINING_EPISODES,
            epsilon=epsilon,
            target_score=settings.TARGET_SCORE,
            train_dummy_name="balanced",
            eval_dummy_name="balanced",
            reward_name="standard",
            seed=settings.SEED
        )

        results.append(result)
        print(result)

    return results

def experiment_reward_functions():
    results = []

    for reward_name in settings.REWARD_FUNCTION_OPTIONS:
        result = run_training_and_evaluation(
            experiment_name="reward_functions",
            training_episodes=settings.PARAMETER_EXPERIMENT_TRAINING_EPISODES,
            epsilon=settings.EPSILON,
            target_score=settings.TARGET_SCORE,
            train_dummy_name="balanced",
            eval_dummy_name="balanced",
            reward_name=reward_name,
            seed=settings.SEED
        )

        results.append(result)
        print(result)

    return results

def experiment_target_scores():
    results = []

    for target_score in settings.TARGET_SCORE_OPTIONS:
        result = run_training_and_evaluation(
            experiment_name="target_scores",
            training_episodes=settings.PARAMETER_EXPERIMENT_TRAINING_EPISODES,
            epsilon=settings.EPSILON,
            target_score=target_score,
            train_dummy_name="balanced",
            eval_dummy_name="balanced",
            reward_name="standard",
            seed=settings.SEED
        )

        results.append(result)
        print(result)

    return results

def run_all_experiments():
    all_results = []

    training_results = experiment_training_iterations()
    save_results_to_csv(training_results, "training_iterations_results.csv")
    all_results.extend(training_results)

    dummy_results = experiment_dummy_strategies()
    save_results_to_csv(dummy_results, "dummy_strategy_results.csv")
    all_results.extend(dummy_results)

    epsilon_results = experiment_epsilon_values()
    save_results_to_csv(epsilon_results, "epsilon_results.csv")
    all_results.extend(epsilon_results)

    reward_results = experiment_reward_functions()
    save_results_to_csv(reward_results, "reward_function_results.csv")
    all_results.extend(reward_results)

    target_results = experiment_target_scores()
    save_results_to_csv(target_results, "target_score_results.csv")
    all_results.extend(target_results)

    policy_rows = experiment_policy_statistics()
    save_results_to_csv(policy_rows, "policy_statistics.csv")

    save_results_to_csv(all_results, "all_experiment_results.csv")

    return all_results

def save_results_to_csv(results, filename):
    if not results:
        print("No results to save.")
        return

    results_dir = Path(settings.RESULTS_FOLDER)
    results_dir.mkdir(parents=True, exist_ok=True)

    output_path = results_dir / filename

    fieldnames = []

    for result in results:
        for key in result.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved results to {output_path}")
if __name__ == "__main__":
    run_all_experiments()