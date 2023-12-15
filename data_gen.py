import csv
import random


def generate_input_data():
    max_length = int(input("Enter the maximum length: "))
    num_items = int(input("Enter the number of items: "))
    fileName = f"data/input_data_{max_length}_{num_items}.csv"

    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([max_length])
        itemLengths = []
        itemDemands = []
        while len(itemLengths) != num_items:
            length = random.randint(5, max_length-2)
            demand = random.randint(5, 100)
            if length not in itemLengths:
                itemLengths.append(length)
                itemDemands.append(demand)

        for (length,demand) in zip(itemLengths,itemDemands):
            writer.writerow([length, demand])


# Example usage
generate_input_data()
