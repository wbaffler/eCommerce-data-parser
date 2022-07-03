import csv

def write_in_file(filename, data_matrix):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data_matrix)