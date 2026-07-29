# 🚀 Pipeline Execution Guide

The **Quantum Delivery Route Planner** follows an end-to-end execution pipeline that transforms delivery location data into optimized delivery routes using both **Quantum Approximate Optimization Algorithm (QAOA)** and **Classical Optimization** techniques.

The pipeline is orchestrated by **`main.py`**, where each stage is responsible for a specific transformation of the optimization problem.

---

# 🏗️ Pipeline Overview

```text
┌──────────────────────────────┐
│ Delivery Locations (CSV)     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Step 1 - Problem Encoder     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Distance Matrix & VRP JSON   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 2 - QUBO Builder        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 3 - Ising Converter     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 4 - QAOA Optimizer      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 5 - Aer Simulator       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 6 - Bitstring Decoder   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ Step 7 - Result Processor    │
└──────────────┬───────────────┘
               │
     ┌─────────┴─────────┐
     ▼                   ▼
┌──────────────┐   ┌────────────────────┐
│ Step 8       │   │ Classical Solver   │
│ OR-Tools     │   │ Held-Karp Fallback │
└──────┬───────┘   └─────────┬──────────┘
       └────────────┬────────┘
                    ▼
      ┌────────────────────────────┐
      │ Step 9 - Comparison Engine │
      └─────────────┬──────────────┘
                    ▼
      ┌────────────────────────────┐
      │ Step 10 - Visualization    │
      └─────────────┬──────────────┘
                    ▼
      ┌────────────────────────────┐
      │ Step 11 - Streamlit App    │
      └────────────────────────────┘
```

---

# 📋 Pipeline Summary

| Step | Module            | Purpose                                  | Output                  |
| ---- | ----------------- | ---------------------------------------- | ----------------------- |
| 1    | Problem Encoder   | Generate distance matrix and VRP dataset | CSV + JSON              |
| 2    | QUBO Builder      | Build quadratic optimization model       | QuadraticProgram        |
| 3    | Ising Converter   | Convert QUBO into Ising Hamiltonian      | SparsePauliOp           |
| 4    | QAOA Optimizer    | Optimize variational parameters          | Optimal γ & β           |
| 5    | Quantum Simulator | Execute QAOA circuit                     | Measurement counts      |
| 6    | Decoder           | Decode best bitstring                    | Delivery route          |
| 7    | Result Processor  | Compute statistics                       | Processed metrics       |
| 8    | Classical Solver  | Solve exact benchmark                    | Optimal classical route |
| 9    | Comparison Engine | Compare quantum vs classical             | Benchmark report        |
| 10   | Visualization     | Generate plots and charts                | Images & Plotly charts  |
| 11   | Dashboard         | Interactive analytics                    | Streamlit application   |

---

# 🔍 Detailed Execution Flow

## Step 1 — Problem Encoder

**Module:** `optimization/problem_encoder.py`

### Responsibilities

* Load delivery locations
* Validate dataset
* Compute Euclidean distance matrix
* Generate VRP metadata

### Input

```
data/raw/delivery_locations.csv
```

### Output

```
data/processed/distance_matrix.csv

data/processed/validated_vrp_dataset.json
```

---

## Step 2 — QUBO Builder

**Module:** `optimization/qubo_builder.py`

### Responsibilities

* Create binary decision variables

[
x_{i,t}\in{0,1}
]

* Build objective function
* Add TSP constraints
* Generate QuadraticProgram

### Output

```
QuadraticProgram
```

---

## Step 3 — Ising Converter

**Module:** `optimization/ising_converter.py`

### Responsibilities

* Convert QuadraticProgram into QUBO
* Transform QUBO into Ising Hamiltonian
* Generate SparsePauliOp

### Output

```
data/processed/ising_model.pkl
```

---

## Step 4 — QAOA Optimizer

**Module:** `quantum/qaoa.py`

### Responsibilities

* Load Ising Hamiltonian
* Construct QAOA ansatz
* Optimize γ and β
* Execute COBYLA optimisation

### Output

```
results/simulator/qaoa_result.pkl
```

---

## Step 5 — Quantum Simulation

**Module:** `quantum/simulator.py`

### Responsibilities

* Build measurement circuit
* Transpile for AerSimulator
* Execute SamplerV2
* Collect measurement counts

### Output

```
results/simulator/counts.json
```

---

## Step 6 — Quantum Decoder

**Module:** `quantum/decoder.py`

### Responsibilities

* Select highest-probability bitstring
* Decode binary solution
* Construct delivery route

### Output

```
results/simulator/decoded_solution.json
```

---

## Step 7 — Result Processor

**Module:** `quantum/result_processor.py`

### Responsibilities

* Compute route distance
* Calculate execution statistics
* Estimate sampling probability
* Generate quantum performance metrics

### Output

```
results/simulator/processed_results.json
```

---

## Step 8 — Classical Solver

**Module:** `classical/tsp_solver.py`

### Responsibilities

* Solve TSP using Google OR-Tools
* Fall back to Held-Karp DP when required
* Generate optimal benchmark route

### Output

```
results/classical/classical_result.json
```

---

## Step 9 — Comparison Engine

**Module:** `comparison/compare_results.py`

### Responsibilities

* Compare route costs
* Compare execution times
* Compute quantum accuracy
* Determine best-performing solver

### Output

```
results/comparison/comparison_result.json
```

---

## Step 10 — Visualization Engine

**Modules**

* `delivery_graph.py`
* `route_plot.py`
* `probability_distribution.py`
* `charts.py`

### Generated Visualizations

* Delivery network graph
* Route trajectory comparison
* Probability histogram
* Cost comparison
* Speed comparison
* Accuracy gauge

### Output Directory

```
visualization/outputs/
```

---

## Step 11 — Interactive Dashboard

**Module**

```
app/dashboard.py
```

Launch the dashboard:

```bash
streamlit run app/dashboard.py
```

### Dashboard Features

* 📍 Delivery route explorer
* ⚛️ Quantum circuit statistics
* 📊 Interactive Plotly analytics
* 📈 Benchmark comparison
* 📉 Probability distribution
* 🎯 Accuracy metrics
* 🚚 Classical vs Quantum route visualisation

---

# 📂 Generated Artifacts

```text
data/
├── raw/
│   └── delivery_locations.csv
│
└── processed/
    ├── distance_matrix.csv
    ├── validated_vrp_dataset.json
    └── ising_model.pkl

results/
├── simulator/
│   ├── qaoa_result.pkl
│   ├── counts.json
│   ├── decoded_solution.json
│   └── processed_results.json
│
├── classical/
│   └── classical_result.json
│
└── comparison/
    └── comparison_result.json

visualization/
└── outputs/
```

---

# ▶️ Running the Complete Pipeline

Execute every stage automatically:

```bash
python main.py
```

Launch the dashboard:

```bash
streamlit run app/dashboard.py
```

Run the unit tests:

```bash
python -m unittest discover tests
```

---

# ✅ Pipeline Outcome

After successful execution, the project produces:

* Optimized quantum delivery route
* Optimal classical benchmark route
* Quantum measurement statistics
* Performance comparison report
* Interactive dashboard
* Route visualisations
* Probability distributions
* Benchmark analytics
* Exportable result artefacts

The modular pipeline makes it easy to replace or extend individual components—for example, by integrating a different quantum optimizer, adding new classical solvers, supporting CVRP variants, or executing on real quantum hardware in future work.
