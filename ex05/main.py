# Deutsch-Jozsa

from typing import Dict
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.result import Result
from qiskit_aer import AerSimulator, AerJob
from matplotlib import pyplot as plt


SHOTS = 500


def deutsch_jozsa_algorithm(oracle: QuantumCircuit) -> QuantumCircuit:

    # Create a quantum circuit with 4 qubits and 3 classical bits
    qc = QuantumCircuit(4, 3)

    qc.x(3)

    for qbit in range (0, 4):
        qc.h(qbit)

    qc.barrier(range(4))
    qc.compose(oracle, inplace=True)

    qc.barrier(range(4))
    for qbit in range (0, 3):
        qc.h(qbit)

    # We are only interested in the first 3 qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def balanced_oracle_definition() -> QuantumCircuit:
    qc = QuantumCircuit(4)

    for qbit in range (0, 3):
        qc.x(qbit)

    for qbit in range (0, 3):
        qc.cx(qbit, 3)

    for qbit in range (0, 3):    
        qc.x(qbit)

    return qc


def constant_oracle_definition() -> QuantumCircuit:
    qc = QuantumCircuit(4)

    qc.x(3)

    return qc


def main():

    try:
        backend = AerSimulator()

        constant_oracle = constant_oracle_definition()

        # Balanced example
        balanced_oracle = balanced_oracle_definition()

        for oracle in [balanced_oracle, constant_oracle]:

            qc = deutsch_jozsa_algorithm(oracle)
            qc.draw("mpl")

            qc_compile = transpile(qc, backend=backend)
            job: AerJob = backend.run(qc_compile, shots=SHOTS)
            result: Result = job.result()
            counts: Dict = result.get_counts(qc_compile)

            if counts.get("000"):
                print("This oracle is constant.")
            else:
                print("This oracle is balanced.")

            counts = {key: value / SHOTS for key, value in counts.items()}
            plot_histogram(counts)
            plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
