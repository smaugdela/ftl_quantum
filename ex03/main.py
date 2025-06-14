# Entanglement

from typing import Dict
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.result import Result
from qiskit_aer import AerSimulator, AerJob
from matplotlib import pyplot as plt


SHOTS = 500


def main():

    try:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        qc.draw("mpl")

        backend = AerSimulator()
        qc_compile = transpile(qc, backend=backend)

        job: AerJob = backend.run(qc_compile, shots=SHOTS)
        result: Result = job.result()

        counts: Dict = result.get_counts(qc_compile)
        counts = {key: value / SHOTS for key, value in counts.items()}
        plot_histogram(counts)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
