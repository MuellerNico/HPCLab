import numpy as np
import matplotlib.pyplot as plt

cpu = [1, 4, 16, 64]
base_res = [64, 128, 256]

data = np.genfromtxt('benchmark_weak.txt', delimiter=',')
column_3 = list(data[:, 2])
print(column_3)

for i in range(3):
    res = base_res[i]
    runtime = column_3[i*4:(i+1)*4]
    plt.plot(cpu, runtime, label='base resolution = %d' % res)

#plt.xscale('log', base=2)
#plt.yscale('log')
plt.xlabel('N_CPU')
plt.ylabel('Time to solution (s)')
plt.legend()
plt.savefig('weak_scaling.pdf')