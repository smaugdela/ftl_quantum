# Shor's Algorithm

from fractions import Fraction
import random
import math
from typing import Dict, List, Set
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import Permutation, QFT, UnitaryGate
from qiskit_aer import AerSimulator
from matplotlib import pyplot as plt


SHOTS = 500
MAX_PRIME = 5


def generate_N() -> int:
    """Generate a random integer N that is a product of two distinct prime numbers."""

    def is_prime(n: int) -> bool:
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    p = random.randint(2, MAX_PRIME)
    q = random.randint(2, MAX_PRIME)
    while p == q or not is_prime(p) or not is_prime(q):
        p = random.randint(2, MAX_PRIME)
        q = random.randint(2, MAX_PRIME)

    N = p * q
    print(f"p = {p}, q = {q}, N = {N}")
    return N


def c_amod15(a):
    """
    Controlled multiplication by a mod 15.
    This is hard-coded for simplicity.
    """
    U = QuantumCircuit(4)
    if a in [2, 13]:
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
    if a in [7, 8]:
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
    if a in [4, 11]:
        U.swap(1, 3)
        U.swap(0, 2)
    if a in [7, 11, 13]:
        for q in range(4):
            U.x(q)
    U = U.to_gate()
    U.name = f"{a} mod 15"
    c_U = U.control()
    return c_U


def quantum_circuit(N: int, a: int) -> QuantumCircuit:

    n = math.ceil(math.log2(N))  # Number of qubits needed to represent N
    m = 2 * n  # Number of qubits needed for the period finding

    qc = QuantumCircuit(m, n)

    ### Superposition
    qc.h(range(n))
    qc.x(range(n, m))
    qc.barrier(range(m))

    ### Controlled-U operations (U is a modular exponentiation operation)
    cu = c_amod15(a)
    for j in range(n):
        qc.append(cu, [j] + list(range(n, m)))
    qc.barrier(range(m))

    ### Inverse Quantum Fourier Transform (QFT)
    qc.append(QFT(n, inverse=True), range(n))
    qc.barrier(range(m))

    ### Measurement
    qc.measure(range(n), range(n))

    return qc


def get_period_from_counts(counts: Dict[str, int], N: int) -> int:
    """
    Extracts the period 'r' from the measurement results using the continued fraction algorithm.
    """
    n_counting_qubits = math.ceil(math.log2(N))  # Number of counting qubits
    # Get the most frequent measurement result (bitstring)
    most_likely_measurement = max(counts, key=counts.get)
    measured_int = int(most_likely_measurement, 2)
    print(f"Most frequent measurement: {most_likely_measurement} (decimal: {measured_int})")

    # Phase phi = s/r ≈ measured_int / 2^n
    phase = measured_int / (2**n_counting_qubits)

    if phase == 0:
        return 0 # No period information found, try another 'a'

    # Use continued fractions to find s/r
    # We limit the denominator to be less than N
    frac = Fraction(phase).limit_denominator(N)
    s, r = frac.numerator, frac.denominator
    print(f"Continued fraction approximation of phase: {s}/{r}")

    return r


def main():

    try:
        backend = AerSimulator()

        N = 15  # For testing purposes, we use a small N = 15 (3 * 5)

        tested_a: Set[int] = set()
        while True:
            # a = random.randint(2, N - 1)
            a = 2
            k = math.gcd(a, N)
            if k != 1:
                print(f"Found a non-trivial factor: {k}")
                break
            elif a not in tested_a:
                tested_a.add(a)
                print(f"Testing a = {a}")

                qc = quantum_circuit(N, a)
                qc = transpile(qc, backend=backend)
                job = backend.run(qc, shots=SHOTS)
                result: Result = job.result()
                counts = result.get_counts(qc)
                print(f"Counts: {counts}")

                r = get_period_from_counts(counts, N)
                if r == 0:
                    print(f"No period found for a = {a}, trying another 'a'...")
                    continue
                elif r % 2 != 0:
                    print(f"Period r = {r} is odd for a = {a}, trying another 'a'...")
                    continue
                elif pow(a, r // 2, N) == -1 % N:
                    print(f"Found a suitable period r = {r} for a = {a}")
                    # Compute the factors of N
                    factor1 = math.gcd(pow(a, r // 2, N) + 1, N)
                    factor2 = math.gcd(pow(a, r // 2, N) - 1, N)
                    print(f"Factors of N: {factor1}, {factor2}")
                    break
            else:
                print(f"Already tested a = {a}, skipping...")
                continue

            if len(tested_a) >= N:
                print("All possible values of a have been tested.")
                raise ValueError("No suitable 'a' found for Shor's algorithm.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
