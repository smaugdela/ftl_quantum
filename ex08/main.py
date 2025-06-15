# Simon's Algorithm

import random
from typing import Dict, List, Set
from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt


SHOTS = 500


def random_oracle_generator(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(2 * n, name="Oracle")

    solution = f"{random.randint(0, 2**n - 1):0{n}b}"
    print(f"Solution: {solution}")

    qc.cx(range(n), range(n, 2 * n))

    for i, q in enumerate(reversed(solution)):
        if q == '1':
            qc.cx(i, n + i)

    return qc


def compute_s_from_measurements(measured_states: List[str]) -> str:
    raise NotImplementedError("This algorithm is not implemented yet.")


def main():

    try:

        raise NotImplementedError("This algorithm is not implemented yet.")

        backend = AerSimulator()

        n = random.randint(2, 5)
        oracle = random_oracle_generator(n)

        qc = QuantumCircuit(2 * n, n)
        qc.h(range(n))

        qc.barrier(range(2 * n))
        qc.compose(oracle, inplace=True)

        qc.barrier(range(2 * n))
        qc.measure(range(n, 2 * n), range(n))
        qc.h(range(n))
        qc.measure(range(n), range(n))
        qc.draw(output='mpl')

        qc_compiled = transpile(qc, backend=backend)

        measured_states: Set[str] = set()
        while len(measured_states) < n:
            result: Result = backend.run(qc_compiled, shots=SHOTS).result()
            counts: Dict = result.get_counts(qc_compiled)
            counts = {k: v / SHOTS for k, v in counts.items()}

            measured_states.update(set(counts.keys()))
            print(f"Measured states: {measured_states}")

        s = compute_s_from_measurements(list(measured_states))
        print(f"Computed s: {s}")

        plot_histogram(counts)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
