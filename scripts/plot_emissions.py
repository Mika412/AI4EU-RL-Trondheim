import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser("Emissions Plot")
parser.add_argument("--emissions", help="Emissions csv file.", type=str)
args = parser.parse_args()
print(args.emissions)

data = pd.read_csv(args.emissions, sep=',', header=0, encoding='unicode_escape')

nrow = 3
ncol = 2
fig, axes = plt.subplots(nrow, ncol)

# plot counter
data.plot(kind='line', x='Timestep', y='CO', color='red', ax=axes[0, 0])
data.plot(kind='line', x='Timestep', y='CO2', color='red', ax=axes[0, 1])
data.plot(kind='line', x='Timestep', y='NOx', color='red', ax=axes[1, 0])
data.plot(kind='line', x='Timestep', y='HC', color='red', ax=axes[1, 1])
data.plot(kind='line', x='Timestep', y='PMx', color='red', ax=axes[2, 0])

plt.show()
