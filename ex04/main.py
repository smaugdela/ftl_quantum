# Entanglement

import os
from typing import Dict
from dotenv import find_dotenv, load_dotenv
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.primitives import PrimitiveResult
from qiskit_ibm_runtime import QiskitRuntimeService, RuntimeJobV2, SamplerV2
from matplotlib import pyplot as plt


SHOTS = 500


def main():

    try:

        load_dotenv(find_dotenv())
        token = os.getenv("QISKIT_IBM_TOKEN")

        service = QiskitRuntimeService(channel="ibm_quantum", token=token)

        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        qc.draw("mpl")

        backend = service.least_busy(min_num_qubits=2, operational=True, simulator=False)
        print(f"Using backend: {backend.name}")
        if backend is None:
            raise Exception("No suitable backend found.")
        qc_compile = transpile(qc, backend=backend)

        sampler: SamplerV2 = SamplerV2(mode=backend)
        job: RuntimeJobV2 = sampler.run([qc_compile], shots=SHOTS)
        result: PrimitiveResult = job.result()

        counts: Dict = result[0].data.meas.get_counts()
        counts = {key: value / SHOTS for key, value in counts.items()}
        plot_histogram(counts)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
