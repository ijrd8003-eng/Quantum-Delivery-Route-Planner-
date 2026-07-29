"""
backend.py

IBM Quantum Backend Configuration.
(Future implementation stub)

This module handles the IBM Quantum service connection
and backend selection for running QAOA on real hardware.

Usage (when IBM credentials are configured):
    service, backend = get_ibm_backend()

Author:
"""

from pathlib import Path

# -------------------------------------------------------
# Future IBM Quantum Connection
# -------------------------------------------------------

IBM_CHANNEL = "ibm_quantum"
IBM_INSTANCE = "ibm-q/open/main"

BASE_DIR = Path(__file__).resolve().parent.parent


def get_ibm_backend(
    min_qubits: int = 16,
    simulator: bool = False,
    verbose: bool = True
):
    """
    Connect to IBM Quantum and return the least busy backend.

    Parameters
    ----------
    min_qubits : int
        Minimum number of qubits required.
    simulator : bool
        If True, select a simulator backend.
    verbose : bool
        Print selected backend info.

    Returns
    -------
    service, backend
    """
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService

        service = QiskitRuntimeService(channel=IBM_CHANNEL)

        backend = service.least_busy(
            min_num_qubits=min_qubits,
            simulator=simulator,
            operational=True
        )

        if verbose:
            print(f"Connected to IBM Quantum.")
            print(f"Backend   : {backend.name}")
            print(f"Qubits    : {backend.num_qubits}")
            print(f"Simulator : {simulator}")

        return service, backend

    except ImportError:
        print("[backend.py] qiskit_ibm_runtime not installed.")
        return None, None

    except Exception as e:
        print(f"[backend.py] IBM Quantum connection failed: {e}")
        return None, None


def is_ibm_configured() -> bool:
    """
    Check whether IBM Quantum credentials are saved.
    """
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        accounts = QiskitRuntimeService.saved_accounts()
        return len(accounts) > 0
    except Exception:
        return False


# -------------------------------------------------------
# Status Check
# -------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("IBM Quantum Backend Status")
    print("=" * 60)

    configured = is_ibm_configured()
    print(f"IBM Credentials Configured : {configured}")

    if not configured:
        print(
            "\nTo configure IBM Quantum:\n"
            "  from qiskit_ibm_runtime import QiskitRuntimeService\n"
            "  QiskitRuntimeService.save_account(\n"
            "      channel='ibm_quantum',\n"
            "      token='YOUR_IBM_QUANTUM_TOKEN'\n"
            "  )"
        )
    else:
        print("\nAttempting backend connection...")
        get_ibm_backend()
