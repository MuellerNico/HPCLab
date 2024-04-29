import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

strong_1_node = pd.read_csv('bench_1_node_strong.csv')
strong_64_node = pd.read_csv('bench_64_nodes_strong.csv')
weak_1_node = pd.read_csv('bench_1_node_weak.csv')
weak_64_node = pd.read_csv('bench_64_nodes_weak.csv')

processes = strong_1_node['p']
speedup_1_node = strong_1_node['time'][0] / strong_1_node['time']
speedup_64_node = strong_64_node['time'][0] / strong_64_node['time']

def amdahl(P, t):
    return 1.0 / (1.0 - P + P / t)

plt.figure()
plt.title('Strong scaling')
plt.plot(processes, speedup_1_node, label='one node', marker='o')
plt.plot(processes, speedup_64_node, label='different nodes', marker='o')
plt.plot(processes, amdahl(1.0, processes), label='Ideal alpha=0', linestyle='--')
plt.plot(processes, amdahl(0.93, processes), label='Amdahl\'s law alpha=0.07', linestyle='--')
plt.xlabel('Number of processes')
plt.ylabel('Speedup S=T1/Tp (seconds)')
plt.xscale('log', base=2)
plt.yscale('log')
plt.legend()
plt.savefig('strong_scaling.pdf')


plt.figure()
plt.title('Weak scaling')
plt.plot(processes, weak_1_node['time'], label='one node')
plt.plot(processes, weak_64_node['time'], label='different nodes')
plt.plot(processes, weak_1_node['time'][0] * np.ones(len(processes)), label='Ideal', linestyle='--')
plt.xlabel('Number of processes')
plt.ylabel('Runtime (seconds)')
plt.xscale('log', base=2)
plt.yscale('log')
plt.legend()
plt.savefig('weak_scaling.pdf')

# check correct scaling
print(weak_1_node['n'] / np.sqrt(weak_1_node['p']))