import matplotlib.pyplot as plt
import pandas as pd
import re

# Function to parse the data from the file
def parse_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract data
    data = []
    for line in lines:
        if "php-apache" in line:
            parts = line.split()
            # Extract CPU utilization percentage using regex
            cpu_utilization_match = re.search(r'cpu:\s*(\d+)%', line)
            if cpu_utilization_match:
                cpu_utilization = int(cpu_utilization_match.group(1))
            else:
                continue  # Skip if no match found

            # Extract replicas count, which is the 7th field (zero-indexed 6)
            try:
                replicas = int(parts[6])
            except (IndexError, ValueError):
                continue  # Skip if there's an error parsing the replicas count

            data.append((cpu_utilization, replicas))

    return pd.DataFrame(data, columns=['CPU Utilization', 'Replicas'])

def generate_graph(input, output, title):

    # Read and parse the data
    data = parse_data(input)

    # Add a time column representing 30-second intervals
    data['Time (seconds)'] = data.index * 30

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot CPU Utilization on the primary y-axis
    ax1.plot(data['Time (seconds)'], data['CPU Utilization'], label='CPU Utilization (%)', color='b')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('CPU Utilization (%)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Create a secondary y-axis for Replicas
    ax2 = ax1.twinx()
    ax2.plot(data['Time (seconds)'], data['Replicas'], label='Replicas', linestyle='--', color='g')
    ax2.set_ylabel('Replicas', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    # Title and grid
    plt.title('CPU Utilization and Replicas Over Time - '+ title )
    fig.tight_layout()  # Adjust layout to prevent label overlap
    plt.grid(True)

    # Save the plot as a PNG file
    plt.savefig(output)

    # plt.show()


generate_graph("estudo_do_retorno_1.txt", "estudo_retorno.png", "")
generate_graph("estudo_do_retorno_2.txt", "estudo_retorno2.png", "")

