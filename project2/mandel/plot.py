from matplotlib import pyplot as plt

threads = [1, 2, 4, 8, 16, 32, 64, 128]

data = []
with open("runtime.txt", 'r') as file:
    data = [float(line.strip()) for line in file]

speedup = [data[0] / tp for tp in data]
plt.plot(threads, speedup, marker='o')
plt.xlabel("Number of threads")
plt.ylabel("Speedup S = T(1) / T(p)")
plt.title("Mandelbrot set strong scaling")
plt.xscale('log', base=2)
plt.savefig("mandel_speedup.pdf")
