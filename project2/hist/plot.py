import numpy as np
from matplotlib import pyplot as plt

T1 = 1.58684
Tp = [2.70225, 
      1.39678, 
      0.759328, 
      0.572412, 
      0.526176, 
      0.270206, 
      0.270623, 
      0.241842]
numCores = [1, 2, 4, 8, 16, 32, 64, 128]

# Plotting
plt.figure()
plt.plot(numCores, [T1 / T for T in Tp], 'o-', label='parallel')
#plt.plot(numCores, numCores, 'o-', label='ideal')
plt.plot(numCores, [1 for _ in numCores], 'o-', label='serial')
plt.xlabel('Number of cores')
plt.ylabel('Speedup (T1/Tp)')
plt.xscale('log', base=2)
plt.title('Speedup vs number of cores')
plt.grid()
plt.legend()
plt.savefig('speedup.pdf')