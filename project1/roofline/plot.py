import numpy as np
import matplotlib.pyplot as plt

# Define the x-axis range
x = np.logspace(8, 24, num=100, base=2)

# Define the y-axis values
y = np.minimum(x * 31.4, 3109000) #slope 31.4 GFlops/s
y2 = np.minimum(x * 38.4, 2488000) #slope 38.4 GFlops/s

# Plot the graph
plt.plot(x, y2)
plt.plot(x, y)
plt.xscale('log', base=2)
plt.yscale('log')

# Label the two graphs
plt.plot(x, y, label='EULER VII Phase I')
plt.plot(x, y2, label='EULER VII Phase II')

# Add a legend
plt.legend()
# Set the axis labels
plt.xlabel('Operational intensity I [Flops/Byte]')
plt.ylabel('Performance P [GFlops/s]')

# Save the plot as a PDF file
plt.savefig('/home/uranus/EULER-DIR/HPCLab/project1/roofline/plot.pdf')