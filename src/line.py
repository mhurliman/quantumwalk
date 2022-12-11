

import cirq
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy
import scipy.special
import sys


def bit_count(x):
    return (x-1).bit_length()

def line_classical(iterations, N=50, start=0, p=0.5):
    
    def walk(num_steps, start=0, p=0.5):
        position = start

        for _ in range(num_steps):
            step = np.random.choice(2, 1, p=[1-p, p])[0] * 2 - 1
            
            position += step

        return position
    
    positions = range(-N, N+1)
    stats = [0 for _ in range(-N, N+1)]

    for i in range(iterations):
        final = walk(N, start, p)
        stats[N+final] += 1

    plt.bar(positions, [n/iterations for n in stats])
    plt.show()

def line_quantum(iterations, N=30, start=0, p=0.5):
    # Given we walk N steps we need enough states to walk N steps in either direction from x=0 
    # -N to N -> 2N + 1 states -> log2(2N + 1) qubits
    num_qubits = bit_count(N*2 + 1)
    
    # Coin qubit is our last indexable bit
    COIN_BIT = num_qubits

    # Rotation about bloch X-axis by theta
    # Probability is dictated by relative angle to |0>
    theta = math.acos(math.sqrt(p))*2

    def init(bits):
        # Start at state which is halfway between our bit range (0b100...0) (otherwise we'll over/underflow)
        yield cirq.X(cirq.LineQubit(0)) 

        # Begin coin in superposition - (|down> + i|up>)/sqrt(2)
        yield cirq.H(cirq.LineQubit(COIN_BIT))
        yield cirq.S(cirq.LineQubit(COIN_BIT))

    def add_circuit(bits):
        for i in range(bits, 0, -1):
            controls = [cirq.LineQubit(v) for v in range(bits, i - 1, -1)]
            yield cirq.X(cirq.LineQubit(i - 1)).controlled_by(*controls)
            
            if i > 1:
                yield cirq.X(cirq.LineQubit(i - 1))

    def walk_step(bits):
        # Coin Flip
        yield cirq.Ry(rads=theta)(cirq.LineQubit(COIN_BIT))

        # Addition op
        yield cirq.X(cirq.LineQubit(bits))

        addition_op = cirq.Circuit(add_circuit(bits)).freeze()

        yield cirq.CircuitOperation(addition_op)
        yield cirq.X(cirq.LineQubit(bits))
        yield cirq.CircuitOperation(cirq.inverse(addition_op))

    def graph(results):
        # Sort results by x-axis position
        # (Results are by default in order of decreasing frequency of measured states)
        items = [(i, j) for i, j in results.items()]
        items.sort(key=lambda x: x[0])

        # Invariant under translation - shift x-axis to 'start' position
        x_arr = [x - (1 << (num_qubits-1)) + start for x in list(zip(*items))[0]] # X-axis positions
        y_arr = [y / iterations for y in list(zip(*items))[1]] # Probability of positions

        # Plot with matplotlib
        plt.plot(x_arr, y_arr)
        plt.scatter(x_arr, y_arr)
        plt.show()

    # Create the circuit
    circuit = cirq.Circuit()
    circuit.append(init(num_qubits))
    for j in range(N):
       circuit.append(walk_step(num_qubits))

    circuit.append(cirq.measure(*cirq.LineQubit.range(num_qubits), key='x')) # Measure final state
    
    # Run simulation many times and build histogram of data
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=iterations)
    final = result.histogram(key='x')

    # Serialize the network structure to file
    with open('circuit_line.txt', 'wt', encoding='utf-8') as f:
        f.write(str(circuit))

    # Graph the histogram results
    graph(final)

line_quantum(5000)