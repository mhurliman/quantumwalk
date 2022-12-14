# Introduction

For the final project I decided to piggyback off my term paper and explore quantum walks from an implementation perspective. My career is heavy on programming and I've cultivated a breadth of experience in various programming languages and environments. As a result I'm keen to learn about quantum computing's programming model, exploring the languages and toolkit options available today.

# Samples

The two samples use Google's Cirq library for building and executing the quantum circuit. Here are the full prerequisite steps for running the samples:
 - Install newest version of [Python 3](https://www.python.org)
 - Install git
    - On Debian-based Linux run `sudo apt-get install git` on the command line
    - On Windows download and install from the [git for Windows](https://gitforwindows.org/) site
 - Pull this repo using `git clone https://github.com/mhurliman/quantumwalk` on the command line
 - Navigate to the cloned repo - if immediately following the preceding step "*cd quantumwalk*"
 - On the command line run `pip install -r requirements.txt`
    - The required packages are: absl, numpy, cirq, matplotlib
 - Run the samples:
    - `python src/line.py -mode quantum -iterations 1000 -num_steps 50`
    - `python src/hypercube.py -iterations 1000 -marked_nodes 3,7,14`


## Random Walk on a Line

The walk on the line is arguably the most basic form of random walk. There are no 'goal' states for the walk to find - just a simple random traversal over the Markov process. The value is found in contrasting the classical version of the walk against the quantum version.

The Line sample (line.py) implements both a classical and quantum version of the random walk on a line. In the quantum case steps of the walk are performed by a combination of a Step operator S and a coin flip operator C, combined to form the unitary operator U = S (C x I). The probability of the coin flip is determined by the operator chosen for C. In this sample we use the operator Ry(theta), where theta is determined by the desired probability for the |up> state. For a specified probability p, theta = acos^2(sqrt(p)). Hadamard is also commonly used as it equates to p = 0.5.

One coin qubit is necessary (left and right states) and the number of position qubits is determined by the specified step count, N (n = log2(2N + 1)). The position qubit is initialized halfway between 0 and (2N + 1), 0b100...0, and the coin qubit is initialized in the state |c> = (|up> + i * |down>) / sqrt(2). The walk progresses by applying the unitary U to the initial state N subsequent times. The system is the measured in the computation basis and the final state is tallied.

<img src="images/line_classical.png" alt="drawing" width="30%">
<img src="images/line_quantum.png" alt="drawing" width="30%">

Figure 1: Left - The ending point distribution of the classical quantum walk on a line starting at X=0 evolving over 50 steps for 1000 iterations. Unsurprisingly follows a classic Gaussian distribution with mean 0 and standard deviation . Right - A quantum walk on a line has a vastly different distribution.

## Quantum Walk Search on a 4D Hypercube

The quantum walk search is more complex then the previous with many ideas pulled from Grover's Search algorithm. In this regime each of the 16 vertices (nodes) are identified with an index of 0-15. A number of nodes M are 'marked' and the quantum walk is progressed a number of steps (dependent on the number of marked nodes), happening upon the marked nodes with some probability.

This structure of this algorithm is much the same as Grover's Search. We separate the states into 'Marked' |G> and 'Unmarked' |B> states, correlating to the marked and unmarked nodes. We can then decompose any state into |S> = sin(theta) |G> + cos(theta) |B> for some theta.

 1. Set up an initial superposition of position states, |U> = 1/sqrt(N) * Sum(|x>, x=0, N)
 2. Repeat O(1/sqrt(M/16)) times
    - Reflect through |B>
    - Reflect through |U>
 3. Measure final state in computation basis

Similar to the quantum walk on the line the basis of this algorithm is the unitary operator, U = S (C x I). In this case the coin operator is implemented with the Grover operation. The construction of the problem allows the step operator to be implemented as a trivial single bit flip to reach adjacent states. This algorithm makes use of the phase oracle method to modify the phase of marked vs. unmarked states. The most complex part is a phase estimation operator which I implemented, but don't fully understand all details. At a high-level it is used to estimate the phase of quantum states of the system, and uses that to mark all quantum states with a non-trivial phase (using phase kickback).

Since the 4D hypercube is composed of 16 nodes that merits 4 position qubits. Similarly as each node has 4 neighbors in this case the coin state requires 2 qubits. 4 additional qubits are used to store the estimated phase, with 1 ancillary qubit used to mark states with the non-trivial phase.

<img src="images/hypercube.png" alt="drawing" width="20%">
<img src="images/hypercube_walk.png" alt="drawing" width="30%">

Figure 2: Results from 1000 iterations of a quantum walk search algorithm on the 4D hypercube

# References

https://learn.microsoft.com/en-us/azure/quantum/overview-azure-quantum

https://quantumai.google/cirq/experiments/quantum_walks

https://qiskit.org/textbook/ch-algorithms/quantum-walk-search-algorithm.html