import numpy as np
import matplotlib.pyplot as plt

cpu = [1, 2, 4, 8, 16]
n = [64, 128, 256, 512, 1024]

data = np.genfromtxt('benchmark_strong.txt', delimiter=',')
column_3 = list(data[:, 2])

print(column_3)
for i in range(5):
    res = n[i]
    runtime = column_3[i*5:(i+1)*5]
    plt.plot(cpu, runtime, label='n = %d' % res)

plt.xscale('log', base=2)
plt.yscale('log')
plt.xlabel('N_CPU')
plt.ylabel('Time to solution (s)')
plt.legend()
plt.savefig('strong_scaling.pdf')