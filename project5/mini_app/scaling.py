import pandas as pd
import matplotlib.pyplot as plt
import math

strong = pd.read_csv('bench_strong.csv', sep=', ')
weak = pd.read_csv('bench_weak.csv', sep=', ')

# ignore warmup (10 rows)
strong = strong[10:]
weak = weak[10:]

P = 0.95
def amdahl(t):
    return 1.0 / (1.0 - P + P / t)

resolutions = strong['nx'].unique()
processes = strong['np'].unique()
print(resolutions)

plt.figure()
for res in resolutions:
    subset = strong[strong['nx'] == res]
    runtime_by_procs = subset.groupby('np')['time'].mean()
    min = subset.groupby('np')['time'].min()
    max = subset.groupby('np')['time'].max()
    plt.plot(processes, runtime_by_procs, marker='o', label=f'{res}x{res} resolution')
    plt.fill_between(processes, min, max, alpha=0.2)

plt.yscale('log')
plt.title('Strong scaling')
plt.xlabel('Number of processes')
plt.ylabel('Time to solution (s)')
plt.legend()
plt.grid()
plt.savefig('scaling_strong.pdf')

plt.figure()
processes = weak['np'].unique()
base_res = weak['base_res'].unique()

for res in base_res:
    subset = weak[weak['base_res'] == res]
    runtime_by_procs = subset.groupby('np')['time'].mean()
    min = subset.groupby('np')['time'].min()
    max = subset.groupby('np')['time'].max()
    plt.plot(processes, runtime_by_procs, marker='o', label=f'{res}x{res} base resolution')
    plt.fill_between(processes, min, max, alpha=0.2)

plt.title('Weak scaling')
plt.xlabel('Number of processes')
plt.ylabel('Time to solution (s)')
plt.legend()
plt.grid()
plt.savefig('scaling_weak.pdf')




