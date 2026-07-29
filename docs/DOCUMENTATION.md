# Master Documentation Hub 📖

Welcome to the central documentation index for the **Quantum Delivery Route Planner**. This repository provides an end-to-end framework for solving combinatorial logistics optimization problems—specifically the **Traveling Salesperson Problem (TSP)** and **Vehicle Routing Problem (VRP)**—using quantum variational algorithms alongside classical benchmark solvers.

---

## 🗺️ Documentation Map

| Module | Link | Description |
| :--- | :--- | :--- |
| **System Architecture** | [ARCHITECTURE.md](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/ARCHITECTURE.md) | Mathematical formulation of VRP/TSP, QUBO matrix construction, Ising spin conversion ($H_C$), and QAOA circuit ansatz parameters. |
| **Pipeline Execution Guide** | [PIPELINE_GUIDE.md](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/PIPELINE_GUIDE.md) | Comprehensive breakdown of the 11 sequential steps in `main.py`, execution flow, inputs, outputs, and intermediate data models. |
| **Quantum vs Classical Benchmarks** | [QUANTUM_VS_CLASSICAL.md](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/QUANTUM_VS_CLASSICAL.md) | Comparison framework between QAOA (Qiskit Aer) and Classical solvers (Google OR-Tools, Held-Karp DP), efficiency, accuracy, and scaling analysis. |
| **Dashboard & Visualizations** | [DASHBOARD_AND_VISUALIZATION.md](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/DASHBOARD_AND_VISUALIZATION.md) | Overview of the Streamlit web dashboard (`app/dashboard.py`), route plots, probability distributions, and NetworkX graph generation. |

---

## ⚙️ System Overview & Workflow

The system takes physical delivery location coordinates, generates a distance matrix, formulates a binary decision model, solves it using quantum and classical algorithms, and computes performance comparisons.

```
[delivery_locations.csv] ➡️ (Problem Encoder) ➡️ [distance_matrix.csv & VRP JSON]
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
(QUBO & Ising Builder)                                (Classical Solver)
         │                                                     │
         ▼                                                     ▼
(QAOA Optimization & Simulator)                      [OR-Tools / Held-Karp]
         │                                                     │
         ▼                                                     ▼
(Decoder & Result Processor)                         [classical_result.json]
         │                                                     │
         └──────────────────────────┬──────────────────────────┘
                                    ▼
                         (Comparison & Metrics)
                                    │
                                    ▼
                      (Streamlit Dashboard & Plots)
```

---

## 🧰 Technology Stack

- **Quantum Computing Framework**: `Qiskit 1.x`, `qiskit-aer`, `qiskit-algorithms`, `qiskit-optimization`
- **Classical Optimization Engine**: `Google OR-Tools`, `SciPy`, `NumPy`
- **Network Graphing**: `NetworkX`
- **Web Application & UI**: `Streamlit`
- **Plotting & Analytics**: `Matplotlib`, `Plotly`, `Seaborn`

---

## 📂 Key Data Interfaces & Artifacts

### Input Data
- `data/raw/delivery_locations.csv`: Contains location IDs, names, X/Y spatial coordinates, and customer demands.

### Processed Artifacts (`data/processed/`)
- `distance_matrix.csv`: Pairwise Euclidean distance matrix across all locations.
- `validated_vrp_dataset.json`: Validated metadata containing depot index, vehicle capacities, demands, and distance matrix.
- `ising_model.pkl`: Serialized Ising Hamiltonian operator ($H_C$) and constant offset.

### Result Artifacts (`results/`)
- `results/simulator/qaoa_result.pkl`: QAOA optimal parameters $\gamma, \beta$, real eigenvalue, and solver iteration count.
- `results/simulator/counts.json`: Bitstring measurement frequency histogram from Qiskit Aer SamplerV2.
- `results/simulator/decoded_solution.json`: Best measured bitstring, decoded city ordering sequence, and reconstructed physical route.
- `results/simulator/processed_results.json`: Summary statistics including route cost, execution time, probability, and total shots.
- `results/classical/classical_result.json`: Exact route sequence, total distance, and computation time from OR-Tools / Held-Karp.
- `results/comparison/comparison_result.json`: Relative percentage cost error, speedup ratio, accuracy percentage, and winner determination.

---

## 🧪 Quick Test Run

To verify system dependencies and execute the entire pipeline:
```bash
python main.py
```

To run individual module tests:
```bash
python -m unittest discover tests
```
