"""
metrics.py

Calculates performance metrics comparing
Classical TSP vs Quantum QAOA results.

Metrics:
    - Cost Difference
    - Cost Percentage Difference
    - Speed Ratio (Classical/Quantum)
    - Accuracy Score
    - Performance Summary

Author:
"""


# -------------------------------------------------------
# Cost Difference
# -------------------------------------------------------

def calculate_cost_diff(classical_cost: float, quantum_cost: float) -> dict:
    """
    Calculates the absolute and relative cost difference.

    Returns:
        dict with absolute_diff, percentage_diff, winner
    """
    absolute_diff = abs(classical_cost - quantum_cost)

    if classical_cost > 0:
        percentage_diff = ((quantum_cost - classical_cost) / classical_cost) * 100
    else:
        percentage_diff = 0.0

    if quantum_cost < classical_cost:
        winner = "Quantum"
    elif classical_cost < quantum_cost:
        winner = "Classical"
    else:
        winner = "Tie"

    return {
        "classical_cost": round(classical_cost, 4),
        "quantum_cost": round(quantum_cost, 4),
        "absolute_diff": round(absolute_diff, 4),
        "percentage_diff": round(percentage_diff, 4),
        "winner": winner
    }


# -------------------------------------------------------
# Speed Ratio
# -------------------------------------------------------

def calculate_speed_ratio(
    classical_time: float,
    quantum_time: float
) -> dict:
    """
    Calculates how much faster one approach is vs the other.

    Returns:
        dict with ratio, faster_method
    """
    if quantum_time > 0:
        ratio = classical_time / quantum_time
    else:
        ratio = float("inf")

    faster = "Classical" if classical_time < quantum_time else "Quantum"

    return {
        "classical_time_s": round(classical_time, 6),
        "quantum_time_s": round(quantum_time, 6),
        "speed_ratio": round(ratio, 4),
        "faster_method": faster,
        "description": (
            f"Classical is {ratio:.2f}x faster"
            if classical_time < quantum_time
            else f"Quantum is {1/ratio:.2f}x faster (simulation overhead)"
        )
    }


# -------------------------------------------------------
# Accuracy Score
# -------------------------------------------------------

def calculate_accuracy_score(
    classical_cost: float,
    quantum_cost: float
) -> dict:
    """
    Calculates the solution quality of the quantum result
    relative to the classical optimal solution.

    Score = 100% means perfect match.
    Score < 100% means quantum solution is worse by that %.
    """
    if classical_cost > 0:
        accuracy = (classical_cost / quantum_cost) * 100 if quantum_cost > 0 else 0
        accuracy = min(accuracy, 100.0)  # Cap at 100%
        gap = max(0, (quantum_cost - classical_cost) / classical_cost * 100)
    else:
        accuracy = 100.0
        gap = 0.0

    if accuracy >= 95:
        quality_label = "Excellent"
    elif accuracy >= 80:
        quality_label = "Good"
    elif accuracy >= 60:
        quality_label = "Moderate"
    else:
        quality_label = "Poor"

    return {
        "accuracy_pct": round(accuracy, 2),
        "optimality_gap_pct": round(gap, 2),
        "quality_label": quality_label
    }


# -------------------------------------------------------
# Number of Solutions Found
# -------------------------------------------------------

def calculate_solution_diversity(quantum_unique_solutions: int) -> dict:
    """
    Summarizes how many unique solutions the quantum approach found.
    """
    return {
        "quantum_unique_solutions": quantum_unique_solutions,
        "classical_unique_solutions": 1,
        "note": (
            "Quantum explores the full solution space probabilistically; "
            "classical returns a single deterministic optimal route."
        )
    }


# -------------------------------------------------------
# Overall Performance Report
# -------------------------------------------------------

def generate_performance_report(
    classical_cost: float,
    quantum_cost: float,
    classical_time: float,
    quantum_time: float,
    quantum_unique_solutions: int,
    best_probability: float
) -> dict:
    """
    Generates a comprehensive performance comparison report.
    """
    cost_metrics = calculate_cost_diff(classical_cost, quantum_cost)
    speed_metrics = calculate_speed_ratio(classical_time, quantum_time)
    accuracy_metrics = calculate_accuracy_score(classical_cost, quantum_cost)
    diversity_metrics = calculate_solution_diversity(quantum_unique_solutions)

    report = {
        "cost_comparison": cost_metrics,
        "speed_comparison": speed_metrics,
        "solution_quality": accuracy_metrics,
        "solution_diversity": diversity_metrics,
        "quantum_best_probability": round(best_probability, 6),
        "summary": {
            "cost_winner": cost_metrics["winner"],
            "speed_winner": speed_metrics["faster_method"],
            "quantum_accuracy": accuracy_metrics["accuracy_pct"],
            "quantum_quality": accuracy_metrics["quality_label"],
        }
    }

    return report
