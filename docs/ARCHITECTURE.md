# 🏗️ System Architecture

The Quantum Delivery Route Planner follows a complete end-to-end optimization pipeline that transforms delivery location data into both **quantum** and **classical** route solutions before benchmarking their performance.

```text
                         Delivery Locations (CSV)
                                   │
                                   ▼
                    Problem Encoder & Distance Matrix
                                   │
                                   ▼
                     Validated VRP / TSP Dataset (JSON)
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
              ▼                                         ▼
       Classical Optimization                 Quantum Optimization
      (OR-Tools / Held-Karp)                 (QUBO Construction)
              │                                         │
              ▼                                         ▼
      Optimal Classical Route                  Ising Hamiltonian
              │                                         │
              │                                         ▼
              │                               QAOA Variational Circuit
              │                                         │
              │                                         ▼
              │                               Aer Quantum Simulation
              │                                         │
              │                                         ▼
              │                                 Bitstring Decoder
              │                                         │
              └────────────────────┬────────────────────┘
                                   ▼
                        Performance Comparison Engine
                                   │
                                   ▼
                    Visualizations & Streamlit Dashboard
```

---

## Mathematical Workflow

The project follows the standard quantum optimization pipeline:

```
Delivery Coordinates
        │
        ▼
Distance Matrix (Euclidean)
        │
        ▼
Traveling Salesperson Problem (TSP)
        │
        ▼
Quadratic Unconstrained Binary Optimization (QUBO)
        │
        ▼
Ising Hamiltonian

        HC = Σ hiZi + Σ JijZiZj + Offset

        │
        ▼
Quantum Approximate Optimization Algorithm (QAOA)

        |ψ(γ,β)⟩

        │
        ▼
COBYLA Parameter Optimization
        │
        ▼
Qiskit Aer Simulation
        │
        ▼
Measurement Counts
        │
        ▼
Bitstring Decoding
        │
        ▼
Optimized Delivery Route
```

---

## Core Components

### 📍 Problem Encoder

* Reads delivery locations
* Computes Euclidean distance matrix
* Generates validated VRP dataset

### 🧩 QUBO Builder

* Creates the binary optimization model
* Defines objective function
* Applies TSP constraints

### ⚛️ Ising Converter

* Converts QUBO to an Ising Hamiltonian
* Generates SparsePauliOp representation
* Stores Hamiltonian for QAOA

### 🚀 Quantum Solver

* Builds a parameterized QAOA circuit
* Optimizes γ and β using COBYLA
* Executes sampling on Qiskit Aer

### 🧠 Classical Solver

* Google OR-Tools Routing Solver
* Held-Karp Dynamic Programming fallback
* Generates optimal benchmark route

### 📊 Comparison Engine

* Route cost comparison
* Runtime benchmarking
* Quantum accuracy evaluation
* Performance reporting

### 📈 Visualization Engine

* Network topology graph
* Route trajectory plots
* Probability distribution histogram
* Interactive Plotly dashboards

### 🖥️ Streamlit Dashboard

* Delivery network explorer
* Quantum circuit statistics
* Route comparison
* Performance analytics
* Interactive benchmark visualizations
