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

def generate_combined_graph(input1, input2, output, title1, title2):

    # Read and parse the data
    data1 = parse_data(input1)
    data2 = parse_data(input2)

    # Add a time column representing 30-second intervals
    data1['Time (seconds)'] = data1.index * 30
    data2['Time (seconds)'] = data2.index * 30

    # Create a single figure with two subplots, one on top of the other
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

    # Plot the first dataset on the first subplot
    ax1.plot(data1['Time (seconds)'], data1['CPU Utilization'], label='CPU Utilization (%)', color='b')
    ax1.set_ylabel('CPU Utilization (%)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Create a secondary y-axis for Replicas for the first subplot
    ax1_twin = ax1.twinx()
    ax1_twin.plot(data1['Time (seconds)'], data1['Replicas'], label='Replicas', linestyle='--', color='g')
    ax1_twin.set_ylabel('Replicas', color='g')
    ax1_twin.tick_params(axis='y', labelcolor='g')

    ax1.set_title('')
    ax1.grid(True)

    # Plot the second dataset on the second subplot
    ax2.plot(data2['Time (seconds)'], data2['CPU Utilization'], label='CPU Utilization (%)', color='b')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('CPU Utilization (%)', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    # Create a secondary y-axis for Replicas for the second subplot
    ax2_twin = ax2.twinx()
    ax2_twin.plot(data2['Time (seconds)'], data2['Replicas'], label='Replicas', linestyle='--', color='g')
    ax2_twin.set_ylabel('Replicas', color='g')
    ax2_twin.tick_params(axis='y', labelcolor='g')

    ax2.set_title('')
    ax2.grid(True)

    # Adjust layout to prevent label overlap
    fig.tight_layout()

    # Save the combined plot as a PNG file
    plt.savefig(output)

    # plt.show()

generate_combined_graph("estudo_do_retorno_1.txt", "estudo_do_retorno_2.txt", "combined_estudo_retorno.png", "", "")
