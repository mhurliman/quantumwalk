# import qsharp

# from PHYS575.HelloWorld import SayHello
# from PHYS575.Teleport import RunTeleportationExample
# from PHYS575.Random import UniformSample
# from PHYS575.Entanglement import TestBellState

# def TestHelloWorld():
#     print(SayHello.simulate(name="quantum world"))

# def TestUniformRandomSample():
#     for i in range(5):
#         print("Iteration {0} : {1}".format(i, UniformSample.simulate()))

# def TestEntanglement():
#     a = TestBellState.simulate(count=500, initial=qsharp.Result.One)
#     print(a[0], a[1], a[2], a[3])

# def main():
#     TestEntanglement()
        
    
#main()

import cirq
import matplotlib.pyplot as plt
import sympy
import tkinter as tk

def handle_keypress(event):
    print(event.char)

def handle_click(event):
    print('click')

def gui_test():
    window = tk.Tk()
    window.bind("<Key>", handle_keypress)

    frame = tk.Frame()

    greeting = tk.Label(
        text="Hello, Tkinter",
        master=frame)
    greeting.pack()

    button = tk.Button(
        text="Click me!",
        width=25,
        height=5,
        bg='blue',
        fg='yellow',
        master=frame )
    button.pack()

    frame.pack()

    window.mainloop()

def cirq_helloworld():
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit(cirq.X(qubit) ** 0.5, cirq.measure(qubit, key='m'))
    print('Circuit:')
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=20)
    print('Results:')
    print(result)

def cirq_bellstate():
    bell_circuit = cirq.Circuit()
    q0, q1 = cirq.LineQubit.range(2)

    bell_circuit.append(cirq.H(q0))
    bell_circuit.append(cirq.CNOT(q0, q1))

    s = cirq.Simulator()

    print('Simulate the circuit:')
    results = s.simulate(bell_circuit)
    print(results)

    bell_circuit.append(cirq.measure(q0, q1, key='result'))

    samples = s.run(bell_circuit, repetitions=1000)

    counts = samples.histogram(key='result')

    cirq.plot_state_histogram(counts, plt.subplot())
    plt.show()

def cirq_sweep():
    q = cirq.GridQubit(1, 1)
    circuit = cirq.Circuit(cirq.X(q) **sympy.Symbol('t'), cirq.measure(q, key='m'))

    param_sweep = cirq.Linspace('t', start=0, stop=2, length=200)
    
    s = cirq.Simulator()
    trials = s.run_sweep(circuit, param_sweep, repetitions=1000)

    x_data = [trial.params['t'] for trial in trials]
    y_data = [trial.histogram(key='m')[1] / 1000.0 for trial in trials]

    plt.scatter('t', 'p', data={'t': x_data, 'p': y_data})
    plt.xlabel('trials')
    plt.ylabel('frequency of qubit measured to be one')
    plt.show()

def walk():

    

cirq_sweep()