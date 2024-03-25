from matplotlib import pyplot as plt
import numpy as np

N = [1000000, 10000000, 100000000] #, 1000000000] #, 1000000000]
T = [1, 2, 4, 8, 16, 32, 64, 128]

data = []
filename = 'runtimes.txt'
with open(filename, 'r') as file:
    data = [float(line.strip()) for line in file] #runtimes

for i in range(len(N)):
    runtime = data[i*8: (i+1)*8]
    speedup = [runtime[0]/tp for tp in runtime]
    lb = "N={:.2e}".format(N[i])
    plt.plot(T, speedup, label=lb)

plt.xlabel('Number of threads')
plt.ylabel('Speedup S=T1/Tp')
plt.xscale('log', base=2)
plt.title('Quicksort strong scaling')
plt.legend()
plt.savefig('plot.pdf')