# Quantum vs Classical Benchmarking ⚔️

This document outlines the comparative evaluation framework used to evaluate **QAOA (Quantum Approximate Optimization Algorithm)** against classical state-of-the-art combinatorial solvers (**Google OR-Tools** and **Held-Karp Dynamic Programming**).

---

## ⚖️ Benchmarking Methodology

The system evaluates route optimization performance across four primary dimensions:

1. **Solution Quality (Route Cost)**: Total Euclidean travel distance required to visit all delivery nodes and return to the depot.
2. **Computational Speed (Execution Time)**: Runtime (in seconds) required to compute or sample the optimal tour.
3. **Quantum Accuracy (%)**: The relative ratio of optimal classical distance to QAOA-decoded route distance.
4. **Sampling Efficiency**: The proportion of measurement shots yielding the global optimum bitstring versus sub-optimal/invalid tours.

---

## 📊 Performance Metrics & Formulas

### 1. Quantum Accuracy Percentage
$$\text{Quantum Accuracy (\%)} = \min\left(100.0, \, \frac{\text{Cost}_{\text{Classical}}}{\text{Cost}_{\text{Quantum}}} \times 100\right)$$

- **100% Accuracy**: QAOA identified the exact optimal tour equal to the classical ground-truth solver.
- **< 100% Accuracy**: QAOA converged to a sub-optimal tour or a valid route with slightly higher mileage.

### 2. Percentage Cost Difference
$$\Delta \text{Cost (\%)} = \frac{|\text{Cost}_{\text{Quantum}} - \text{Cost}_{\text{Classical}}|}{\text{Cost}_{\text{Classical}}} \times 100$$

### 3. Execution Speedup / Slowdown Ratio
$$\text{Speed Ratio} = \frac{\text{Time}_{\text{Quantum}}}{\text{Time}_{\text{Classical}}}$$

---

## 🏆 Performance Evaluation Matrix

The output produced by `comparison/compare_results.py` generates structured JSON reports matching the following format:

```json
{
    "classical": {
        "solver": "OR-Tools (Guided Local Search)",
        "route_cost": 284.15,
        "execution_time": 0.0125,
        "route_names": ["Depot", "Customer_A", "Customer_B", "Customer_C", "Depot"]
    },
    "quantum": {
        "route_cost": 284.15,
        "execution_time": 2.1450,
        "unique_solutions": 16,
        "best_probability": 0.3842,
        "best_bitstring": "1000010000100001"
    },
    "performance": {
        "summary": {
            "cost_winner": "Tie (Optimal Solution Found)",
            "speed_winner": "Classical",
            "quantum_accuracy": 100.0,
            "solution_quality": "Optimal"
        },
        "cost_comparison": {
            "absolute_diff": 0.0,
            "percentage_diff": 0.0
        },
        "speed_comparison": {
            "ratio": 171.6,
            "description": "Classical solver was 171.60x faster than QAOA simulator"
        }
    }
}
```

---

## 📈 Scalability & Hardware Analysis

| Dimension | Classical Solvers (OR-Tools / Held-Karp) | QAOA Variational Quantum Solver |
| :--- | :--- | :--- |
| **Problem Formulation** | Graph adjacency matrix / integer programming constraints | $N^2$ binary variables mapped to Ising $Z$-spin operators |
| **Qubit / Variable Requirement** | $N$ node indices | $N^2$ physical qubits for full TSP position matrix encoding |
| **Computational Complexity** | DP: $O(N^2 2^N)$ exact; Heuristics: $O(N \log N)$ approximate | Quantum state preparation: $O(p \cdot N^2)$ gate depth; Classical optimization: $O(\text{iterations})$ |
| **Noise & Hardware Limitations** | Deterministic CPU execution, no noise | NISQ hardware decoherence, gate errors, and measurement readout noise |
| **Scaling Horizon** | Solves up to 100,000+ nodes classically using heuristics | NISQ state simulator practical limit: $N \le 5$ locations ($25$ qubits) |
