import matplotlib.pyplot as plt
import numpy as np


SAMPLE_TIME = 20


def get_data(file):
    lines = open(file)
    lines = lines.readlines()
    sample_num = []
    counts = []
    lines = lines[2:]
    for line in lines:
        separated_data = line.split()
        sample_num.append(int(separated_data[0]))
        counts.append(int(separated_data[1]))
    return [sample_num, counts]


def get_average_background(data):
    return sum(data[1])/len(data[1])


def subtract_from_list(data: [list, list], num):
    for x in range(0, len(data[1])):
        data[1][x] -= num
    return data


def remove_first_30(data):
    seconds = 30 * 60
    samples = seconds/SAMPLE_TIME
    data[0] = data[0][int(samples)-1:]
    data[1] = data[1][int(samples) - 1:]
    return data


def only_first_30(data):
    seconds = 30 * 60
    samples = seconds / SAMPLE_TIME
    data[0] = data[0][:int(samples) - 1]
    data[1] = data[1][:int(samples) - 1]
    return data


def remove_last_30(data):
    data[0] = data[0][:len(data[0])-30]
    data[1] = data[1][:len(data[1])-30]
    return data


def remove_slow_decay(data, coefs):
    for x in range(0, len(data[1])):
        data[1][x] -= (coefs[0]*x + coefs[1])
    return data


def get_log_of_data(data):
    data[1] = np.log(data[1])
    return data


def get_exp_of_data(data):
    data[1] = np.exp(data[1])
    return data


def get_fit(data):
    coefs = np.polyfit(data[0], data[1], 1)
    return coefs


def plot_semilog(data):
    plt.semilogy(data[0], data[1])
    plt.show()


def plot(data):
    plt.plot(data[0], data[1])
    plt.show()


sample_data = get_data('sample_correct.txt')
background_data = get_data('background_rad.txt')
background_avg = get_average_background(background_data)
sample_no_bg = subtract_from_list(sample_data, background_avg)
sample_ignore_first_30 = remove_first_30(list(sample_no_bg))
sample_ends_removed = remove_last_30(list(sample_ignore_first_30))
sample_first_30 = only_first_30(list(sample_no_bg))
log_data = get_log_of_data(list(sample_ends_removed))
sample_first_30_log = get_log_of_data(sample_first_30)
coefs = get_fit(log_data)
print(log_data)
print(coefs[0], coefs[1])
corrected_data_log = remove_slow_decay(list(sample_first_30_log), coefs)
print(corrected_data_log)
corrected_data = get_exp_of_data(list(corrected_data_log))
plot(corrected_data)
#plot_semilog(sample_ends_removed)
