"""
main.py

Quantum Delivery Route Planner - End-to-End Pipeline

Executes all 11 steps in order:

    Step 1.  problem_encoder.py       - Build distance matrix
    Step 2.  qubo_builder.py          - Build QUBO model
    Step 3.  ising_converter.py       - Convert to Ising Hamiltonian
    Step 4.  qaoa.py                  - Run QAOA optimization
    Step 5.  simulator.py             - Run QAOA circuit on Aer
    Step 6.  decoder.py               - Decode bitstring to route
    Step 7.  result_processor.py      - Process & compute statistics
    Step 8.  tsp_solver.py            - Solve classically (OR-Tools)
    Step 9.  compare_results.py       - Compare Classical vs Quantum
    Step 10. Visualization scripts    - Generate all charts & plots
    Step 11. streamlit run app/...    - Launch dashboard (optional)

Author:
"""

import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable


# -------------------------------------------------------
# Step Runner
# -------------------------------------------------------

def run_step(name: str, script: Path, cwd: Path = None) -> bool:
    """
    Runs a Python script as a subprocess.
    Returns True on success, False on failure.
    """
    print(f"\n{'=' * 65}")
    print(f"  {name}")
    print(f"{'=' * 65}")

    start = time.time()

    try:
        result = subprocess.run(
            [PYTHON, str(script)],
            cwd=str(cwd or BASE_DIR),
            capture_output=False,
            text=True,
            timeout=300
        )

        elapsed = time.time() - start

        if result.returncode == 0:
            print(f"\n  [OK] Completed in {elapsed:.2f}s")
            return True
        else:
            print(f"\n  [FAILED] (exit code {result.returncode}) in {elapsed:.2f}s")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n  [FAILED] Timed out after 300s")
        return False

    except Exception as e:
        print(f"\n  [FAILED] Error: {e}")
        return False


# -------------------------------------------------------
# Pipeline Steps
# -------------------------------------------------------

STEPS = [
    (
        "Step 1 | Problem Encoder -- Build Distance Matrix",
        BASE_DIR / "optimization" / "problem_encoder.py"
    ),
    (
        "Step 2 | QUBO Builder -- Build Quadratic Program",
        BASE_DIR / "optimization" / "qubo_builder.py"
    ),
    (
        "Step 3 | Ising Converter -- Build Ising Hamiltonian",
        BASE_DIR / "optimization" / "ising_converter.py"
    ),
    (
        "Step 4 | QAOA -- Run Quantum Optimization",
        BASE_DIR / "quantum" / "qaoa.py"
    ),
    (
        "Step 5 | Simulator -- Run QAOA Circuit on Aer",
        BASE_DIR / "quantum" / "simulator.py"
    ),
    (
        "Step 6 | Decoder -- Decode Bitstring to Route",
        BASE_DIR / "quantum" / "decoder.py"
    ),
    (
        "Step 7 | Result Processor -- Compute Quantum Statistics",
        BASE_DIR / "quantum" / "result_processor.py"
    ),
    (
        "Step 8 | Classical TSP Solver -- OR-Tools Benchmark",
        BASE_DIR / "classical" / "tsp_solver.py"
    ),
    (
        "Step 9 | Comparison -- Classical vs Quantum",
        BASE_DIR / "comparison" / "compare_results.py"
    ),
    (
        "Step 10a | Visualization -- Delivery Network Graph",
        BASE_DIR / "visualization" / "delivery_graph.py"
    ),
    (
        "Step 10b | Visualization -- QAOA Route Plot",
        BASE_DIR / "visualization" / "route_plot.py"
    ),
    (
        "Step 10c | Visualization -- Probability Distribution",
        BASE_DIR / "visualization" / "probability_distribution.py"
    ),
    (
        "Step 10d | Visualization -- Comparison Charts",
        BASE_DIR / "visualization" / "charts.py"
    ),
]


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    print()
    print("===============================================================")
    print("  QUANTUM DELIVERY ROUTE PLANNER -- End-to-End Pipeline  ")
    print("===============================================================")
    print()

    results = {}
    start_total = time.time()

    for step_name, script_path in STEPS:
        if not script_path.exists():
            print(f"\n  [SKIP] {step_name}")
            print(f"         File not found: {script_path}")
            results[step_name] = "SKIPPED"
            continue

        success = run_step(step_name, script_path)
        results[step_name] = "OK" if success else "FAILED"

    total_elapsed = time.time() - start_total

    # Summary
    print()
    print("===============================================================")
    print("                    PIPELINE SUMMARY                           ")
    print("===============================================================")
    print()

    passed = 0
    failed = 0

    for step_name, status in results.items():
        label = step_name.split(" | ")[-1] if " | " in step_name else step_name
        icon = f"[{status}]"
        print(f"  {icon:<10} {label[:50]}")

        if status == "OK":
            passed += 1
        elif status == "FAILED":
            failed += 1

    print()
    print(f"  Total time : {total_elapsed:.1f}s")
    print(f"  Passed     : {passed}")
    print(f"  Failed     : {failed}")
    print()

    if failed == 0:
        print("  Pipeline completed successfully!")
        print()
        print("  Launch the dashboard with:")
        print("  > streamlit run app/dashboard.py")
    else:
        print("  Some steps failed. Check output above.")
    print()


if __name__ == "__main__":
    main()
