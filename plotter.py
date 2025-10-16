import numpy as np
import matplotlib.pyplot as plt

# Path to your text file
file_path = "readings/reading9.txt"

# Initialize an empty list
values = []
filter_values = []
output = 0
a = 0.9

# Open the file and read each line
with open(file_path, "r") as file:
    for line in file:
        # Strip whitespace/newline and convert to desired type (e.g., int or float)
        value = line.strip()  # Remove \n and spaces
        if value:  # Skip empty lines
            try:
                # Convert to float (change to int() if needed)
                values.append(int(value)/4095.0 * 2.5)
            except ValueError:
                print(f"Warning: could not convert '{output}' to a number.")
                

print(len(values))
print(values)
x = np.arange(len(values))  # x will have the same length as values
for v in values:
    output = ((1-a)*v) + (a*output)
    filter_values.append(output)
# ((int(v)/4095)*1.25)

plt.axis([0, len(filter_values), .95, 3])
plt.plot(x, filter_values)
# plt.plot(x, values)
plt.show()