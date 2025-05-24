# Token

from dotenv import find_dotenv, load_dotenv
import os
from qiskit_ibm_runtime import QiskitRuntimeService


def main():

    load_dotenv(find_dotenv())
    token = os.getenv("QISKIT_IBM_TOKEN")

    service = QiskitRuntimeService(channel="ibm_quantum", token=token)


    try:
        backends = service.backends()
        simulators = {backend for backend in backends if backend.configuration().simulator}
        real = set(backends).difference(simulators)

        print("Simulated quantum computers:")
        for backend in simulators:
            name = backend.name
            status = backend.status()
            jobs=status.pending_jobs
            print(f'\t{name} has {jobs} queues')

        print("Real quantum computers")
        for backend in real:
            name = backend.name
            status = backend.status()
            jobs=status.pending_jobs
            config = backend.configuration()
            qbits = config.n_qubits
            print(f'\t{name} has {jobs} queues with {qbits} qubits')


    except Exception as e:
        print(f"An error occured: {e}")
        print("You may want to check if your API key is well set in your .env file, and still valid.")


if __name__ == "__main__":
    main()
