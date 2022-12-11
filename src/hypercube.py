import cirq
import numpy as np
import matplotlib.pyplot as plt

def hypercube(iterations):

    state_position = cirq.LineQubit.range(0, 4)
    state_coin = cirq.LineQubit.range(4, 6)

    def shift_operator(qubits):
        for i in range(4):
            yield cirq.X(qubits[4])
            if i % 2 == 0:
                yield cirq.X(qubits[5])

            yield cirq.X(qubits[i]).controlled_by(*qubits[4:6])

    def one_step(qubits):
        c = cirq.Circuit()
        c.append(cirq.H.on_each(*qubits))
        c.append(cirq.Z.on_each(*qubits))
        c.append(cirq.Z(qubits[5]).controlled_by(qubits[4]))
        c.append(cirq.H.on_each(*qubits))

        c.append(shift_operator(qubits))

        return c

    def phase_oracle(qubits):
        c = cirq.Circuit()
        c.append(cirq.X(qubits[2]))
        c.append(cirq.H(qubits[3]))
        c.append(cirq.X(qubits[3]).controlled_by(*qubits[0:3]))
        c.append(cirq.H(qubits[3]))
        c.append(cirq.X(qubits[2]))

        c.append(cirq.H(qubits[3]))
        c.append(cirq.X(qubits[3]).controlled_by(*qubits[0:3]))
        c.append(cirq.H(qubits[3]))

        return c

    def mark_auxiliary(qubits):
        c = cirq.Circuit()
        c.append(cirq.X.on_each(*qubits))
        c.append(cirq.X(qubits[4]).controlled_by(*qubits[0:4]))
        c.append(cirq.Z(qubits[4]))
        c.append(cirq.X(qubits[4]).controlled_by(*qubits[0:4]))
        c.append(cirq.X.on_each(*qubits))

        return c

    def phase_estimation(qubits):
        c = cirq.Circuit()
        c.append(cirq.H.on_each(*qubits[0:4])) 
        
        for i in range(0, 4):
            stop = 2**i
            for j in range(0, stop):
                one_step_op = cirq.CircuitOperation(one_step(qubits[4:10]).freeze())
                c.append(one_step_op.controlled_by(qubits[i]))

        c.append(cirq.inverse(cirq.qft(*qubits[0:4])))
        c.append(mark_auxiliary(qubits[0:4] + [qubits[10]]))
        c.append(cirq.qft(*qubits[0:4]))

        for i in range(3, -1, -1):
            stop = 2**i
            for j in range(0, stop):
                one_step_op_inv = cirq.CircuitOperation(cirq.inverse(one_step(qubits[4:10])).freeze())
                c.append(one_step_op_inv.controlled_by(qubits[i]))

        c.append(cirq.H.on_each(*qubits[0:4]), cirq.InsertStrategy.NEW)

        return c

    #simulator = cirq.Simulator()
    #simulator.run(circuit, repetitions=iterations)

    c = cirq.Circuit()
    

    with open('circuit_hypercube.txt', 'wt', encoding='utf-8') as f:
        f.write(str(phase_estimation(cirq.LineQubit.range(0, 11))))


hypercube(5000)