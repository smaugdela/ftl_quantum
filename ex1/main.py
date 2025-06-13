# Token

from dotenv import find_dotenv, load_dotenv
import os
from qiskit_ibm_runtime import QiskitRuntimeService


def main():

    try:
        load_dotenv(find_dotenv())
        token = os.getenv("QISKIT_IBM_TOKEN")

        service = QiskitRuntimeService(channel="ibm_quantum", token=token)

        backends = service.backends()
        simulators = {backend for backend in backends if backend.configuration().simulator}
        real = set(backends).difference(simulators)

        print("Simulated quantum computers:")
        for backend in simulators:
            name = backend.name
            status = backend.status()
            jobs=status.pending_jobs
            print(f"\t{name:<35s} has {jobs:4} queues")

        print("Real quantum computers:")
        for backend in real:
            name = backend.name
            status = backend.status()
            jobs=status.pending_jobs
            config = backend.configuration()
            qbits = config.n_qubits
            print(f"\t{name:<15s} has {jobs:4} queues with {qbits:3} qubits")

    except Exception as e:
        print(f"Error: {e}")
        print("(You may want to check if your QISKIT_IBM_TOKEN is well set in your .env file, and still valid.)")


if __name__ == "__main__":
    main()
