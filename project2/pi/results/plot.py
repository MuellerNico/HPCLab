import os
import matplotlib.pyplot as plt

scaling_modes = ['strong', 'weak']
implementations = ['serial', 'critical', 'reduction']

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        values = [line.strip() for line in lines]
        values = [float(value) for value in values]
    return values

for mode in scaling_modes:
    serial = read_file(f'{mode}/serial.txt')
    critical = read_file(f'{mode}/critical.txt')
    reduction = read_file(f'{mode}/reduction.txt')

    # calculate speedup from runtimes
    critical = [t1 / tp for t1, tp in zip(serial, critical)]
    reduction = [t1 / tp for t1, tp in zip(serial, reduction)]

    x_values = [i+1 for i in range(48)]
    ideal_speedup = [x for x in x_values]

    #plt.plot(x_values, serial, label='Serial')
    plt.plot(x_values, critical, label='Critical')
    plt.plot(x_values, reduction, label='Reduction')
    #plt.plot(x_values, ideal_speedup, label='Ideal speedup')
    plt.xlabel('Number of cores')
    plt.ylabel('Speedup (T_1 / T_p)')
    plt.title(f'{mode.capitalize()} scaling')
    plt.legend()
    plt.savefig(f'{mode}_scaling.pdf')
    plt.close()



            

        