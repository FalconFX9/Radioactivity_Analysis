import matplotlib.pyplot as plt
import math
import numpy as np

def open_file(file_path):
    file = open(file_path)
    lines = file.readlines()
    counts = []
    for line in lines[2:]:
        elements = line.split()
        counts.append(int(elements[1]))
    return counts

def plot_distribution(counts):
    counts_dict = {}
    for count in counts:
        if count not in counts_dict.keys():
            counts_dict[count] = 1
        else:
            counts_dict[count] += 1
    total = sum(counts_dict.values())
    for key in counts_dict.keys():
        counts_dict[key] /= total
    print(sum(counts_dict.values()))
    new_dict = dict(sorted(counts_dict.items()))
    print(new_dict)
    plt.plot(new_dict.keys(), new_dict.values())
    plt.legend(["Normalized Distribution of recorded counts"])
    plt.show()

def plot_counts_over_time(counts):
    average = sum(counts)/len(counts)
    count_num = []
    for i in range(1, len(counts)+1):
        count_num.append(i)
    line = np.polyfit(count_num, counts, 1)
    func = np.poly1d(line)
    plt.plot(count_num, counts)
    plt.plot(count_num, func(count_num))
    plt.axhline(average, color='r')
    plt.legend(["Recorded Counts", "Trendline of Counts", "Average"])
    plt.show()

counts = open_file('bg.txt')
plot_counts_over_time(counts)
plot_distribution(counts)
