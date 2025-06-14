# Simon

import random
from typing import Dict
from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt


SHOTS = 500


def random_oracle_generator(Y: int) -> QuantumCircuit:
    qc = QuantumCircuit(Y + 1, name="Oracle")

    ###

    return qc


def main():

    try:

        backend = AerSimulator()

        n = random.randint(1, 8)  # Number of data qubits
        oracle = random_oracle_generator(n)

        qc = QuantumCircuit(n + 1, n)
        # Data qubits into |+>
        for q in range(n):
            qc.h(q)
        # Ancilla into |->
        qc.x(n)
        qc.h(n)

        qc.barrier(range(n + 1))
        qc.compose(oracle, inplace=True)

        qc.barrier(range(n + 1))
        for q in range(n):
            qc.h(q)
        qc.measure(range(n), range(n))
        qc.draw(output='mpl')

        qc_compiled = transpile(qc, backend=backend)
        result: Result = backend.run(qc_compiled, shots=SHOTS).result()
        counts: Dict = result.get_counts(qc_compiled)
        counts = {k: v / SHOTS for k, v in counts.items()}

        plot_histogram(counts)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
