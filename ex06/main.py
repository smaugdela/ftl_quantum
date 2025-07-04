# Algorithme de recherche

import math
import random
from typing import Dict, List
from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt


SHOTS = 500


def state_init(Y: int) -> QuantumCircuit:
    qc = QuantumCircuit(Y+1, name="States initialization")
    # Data qubits into |+>
    for q in range(Y):
        qc.h(q)
    # Ancilla into |->
    qc.x(Y)
    qc.h(Y)
    return qc


def random_oracle_generator(Y: int) -> QuantumCircuit:
    qc = QuantumCircuit(Y + 1, name="Oracle")

    num_solutions = random.randint(1, 3)

    print(f"Number of solutions: {num_solutions}")
    solutions: List[int] = random.sample(range(2 ** Y), num_solutions)
    solutions: List[str] = [format(solution, f"0{Y}b") for solution in solutions]
    print(f"Solutions: {solutions}")
    for solution in solutions:
        for i, bit in enumerate(reversed(solution)):    # reversed because qiskit use little-endian
            if bit == '0':
                qc.x(i)
        qc.mcx(list(range(Y)), Y)
        for i, bit in enumerate(reversed(solution)):
            if bit == '0':
                qc.x(i)

    return qc


def diffuser(Y: int) -> QuantumCircuit:
    qc = QuantumCircuit(Y + 1, name="Diffuser")

    for i in range(Y + 1):
        qc.h(i)

    for i in range(Y):
        qc.x(i)

    # Multi-controlled Z gate
    # Beacuse Z = H * X * H, we can use a multi-controlled Toffoli gate wrapped in Hadamard gates
    qc.h(Y - 1)
    qc.mcx(list(range(Y - 1)), Y - 1)
    qc.h(Y - 1)

    for i in range(Y):
        qc.x(i)

    for i in range(Y):
        qc.h(i)

    return qc


def main():

    try:
        N = 4

        backend = AerSimulator()

        qc = QuantumCircuit(N + 1, N)

        qc.compose(state_init(N), inplace=True)
        oracle = random_oracle_generator(N)

        # Apply 'iterations' time the oracle and diffuser
        iterations = math.floor((math.pi/4) * math.sqrt(N))
        for _ in range(iterations):
            qc.barrier(range(N + 1))
            qc.compose(oracle, inplace=True)
            qc.barrier(range(N + 1))
            qc.compose(diffuser(N), inplace=True)

        qc.measure(range(N), range(N))

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
