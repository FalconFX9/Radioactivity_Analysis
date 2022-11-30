import matplotlib.pyplot as plt
import numpy as np
import whyte_and_tailor
import copy
import math


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
    data = copy.deepcopy(data)
    for x in range(0, len(data[1])):
        data[1][x] -= num
        if data[1][x] < 1.5:
            data[1][x] = 1.5
    return data


def subtract_lists(data, points):
    data = copy.deepcopy(data)
    for x in range(len(points)):
        data[1][x] -= points[x]
    return data


def remove_first_30(data):
    data = copy.deepcopy(data)
    seconds = 30 * 60
    samples = seconds/SAMPLE_TIME
    data[0] = data[0][int(samples)-1:]
    data[1] = data[1][int(samples) - 1:]
    return data


def remove_first_n_min(min, data):
    data = copy.deepcopy(data)
    seconds = min * 60
    samples = seconds/SAMPLE_TIME
    data[0] = data[0][int(samples)-1:]
    data[1] = data[1][int(samples) - 1:]
    return data


def only_first_30(data):
    data = copy.deepcopy(data)
    seconds = 30 * 60
    samples = seconds / SAMPLE_TIME
    data[0] = data[0][:int(samples) - 1]
    data[1] = data[1][:int(samples) - 1]
    return data


def remove_last_30(data):
    data = copy.deepcopy(data)
    data[0] = data[0][:len(data[0])-30]
    data[1] = data[1][:len(data[1])-30]
    return data


def remove_slow_decay(data, coefs):
    data = copy.deepcopy(data)
    for x in range(0, len(data[1])):
        data[1][x] -= (coefs[0]*x + coefs[1])
    return data


def get_log_of_data(data):
    data = copy.deepcopy(data)
    data[1] = np.log(data[1])
    return data


def get_exp_of_data(data):
    data = copy.deepcopy(data)
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
counts_l = []
trendline = []
error_stddev = []
for x in range(len(sample_no_bg[0])):
    counts_l.append(whyte_and_tailor.counts_bi212(20*x))
    error_stddev.append(math.sqrt(sample_no_bg[1][x]))
    trendline.append(whyte_and_tailor.trendline(20*x/60))

sample_no_fast = subtract_lists(sample_no_bg, trendline)
plt.errorbar(sample_no_bg[0], sample_no_bg[1], error_stddev, fmt='.', elinewidth=1)
plt.plot(sample_no_bg[0], counts_l, 'r')
plt.plot(sample_no_bg[0], trendline, 'g')
plt.title("Decay model and experimental data")
plt.legend(["Whyte and Taylor Model + Pb212","Exponential Fit",  "Counts with background Subtracted"])
plt.xlabel("Sample Number (1 sample=20s)")
plt.ylabel("Counts/Sample")
plt.show()
plt.plot(sample_no_bg[1], counts_l)
counts_l = np.array(counts_l)
sample = np.array(sample_no_bg[1])
counts_l_2 = counts_l[:, np.newaxis]
coef, _, _, _ = np.linalg.lstsq(counts_l_2, sample)
print(coef)
chi_squared = 0
print(len(sample_no_bg[1]))
for n in range(len(sample_no_bg[1])):
    term = ((sample[n]-coef*counts_l[n])**2)/sample[n]
   # print(term)
    chi_squared += term
print(chi_squared)
print(chi_squared/341)
plt.plot(counts_l, counts_l*coef)
plt.xlim([0, 60])
plt.ylim([0, 60])
plt.show()

sample_ignore_first_30 = remove_first_30(sample_no_bg)
sample_ignore_first_hour = remove_first_n_min(90, sample_no_bg)
sample_ends_removed = remove_last_30(list(sample_ignore_first_30))
sample_first_30 = only_first_30(list(sample_no_bg))
log_data = get_log_of_data(list(sample_ignore_first_hour))
sample_first_30_log = get_log_of_data(sample_first_30)
full_log_data = get_log_of_data(sample_no_bg)
coefs = get_fit(log_data)
plot(log_data)
print((-1/coefs[0]*20)/60, coefs[1])
plt.plot(full_log_data[0], full_log_data[1])
plt.show()
corrected_data_log = remove_slow_decay(list(sample_first_30_log), coefs)
corrected_data = get_exp_of_data(list(corrected_data_log))
plot(corrected_data)
#plot_semilog(sample_ends_removed)
