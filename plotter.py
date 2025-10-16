import numpy as np
import matplotlib.pyplot as plt

# Path to your text file
file_path = "readings/reading1.txt"

# Initialize an empty list
values = []

# Open the file and read each line
with open(file_path, "r") as file:
    for line in file:
        # Strip whitespace/newline and convert to desired type (e.g., int or float)
        value = line.strip()  # Remove \n and spaces
        if value:  # Skip empty lines
            try:
                # Convert to float (change to int() if needed)
                values.append(int(value)/4095.0 * 1.25)
            except ValueError:
                print(f"Warning: could not convert '{value}' to a number.")
                

print(len(values))
print(values)
x = np.arange(len(values))  # x will have the same length as values

# ((int(v)/4095)*1.25)

plt.axis([0, len(values), -0.1, 1.8])
plt.plot(x, values)
plt.show()