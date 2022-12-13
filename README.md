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

The Line sample (line.py) implements both a classical and quantum version of the random walk on a line. 


<img src="images/line_classical.png" alt="drawing" width="30%">
<img src="images/line_quantum.png" alt="drawing" width="30%">

Figure 1: Left - The ending point distribution of the classical quantum walk on a line starting at X=0 evolving over 50 steps for 1000 iterations. Unsurprisingly follows a classic Gaussian distribution with mean 0 and standard deviation . Right - A quantum walk on a line has a vastly different distribution.

## Quantum Walk Search on a 4D Hypercube


<img src="images/hypercube_walk.png" alt="drawing" width="30%">

Figure 1:

# Impressions

The programming model


# Toolkits



## Q#

## Cirq


# References

https://learn.microsoft.com/en-us/azure/quantum/overview-azure-quantum

https://quantumai.google/cirq/experiments/quantum_walks

https://qiskit.org/textbook/ch-algorithms/quantum-walk-search-algorithm.html