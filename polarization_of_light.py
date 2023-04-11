import matplotlib.pyplot as plt
import math
import numpy as np
import scipy


def open_file(file_path):
    file = open(file_path)
    lines = file.readlines()
    split_lines = []
    for line in lines[304:]:
        split_lines.append(line.split(','))
    return split_lines


def get_trial(split_lines, num):
    angle, volts = [], []
    for line in split_lines:
        try:
            angle.append(float(line[num*3]))
            volts.append(float(line[(num*3)+1]))
        except ValueError:
            break
    return angle, volts


def get_exp_fit(angle, volts, p0):
    coefs = scipy.optimize.curve_fit(lambda t, a, b: a*np.exp(b*t), np.array(angle), np.array(volts), p0)
    print(coefs)
    return coefs

def get_linear_fit(angle, volts):
    coefs = scipy.optimize.curve_fit(lambda t, a, b: a*t + b, np.array(angle), np.array(volts), (0.1, -2))
    print(coefs)
    return coefs


def trial_1_trendline(x):
    return 1043.74173*np.exp(-0.0355769422*x)


def trial_2_first_half_trendline(x):
    return 6151.65432*np.exp(-0.0500355344*x)
    #return 11925.1838 * np.exp(-0.050667549 * x)


def trial_2_latter_half_trendline_guess(x):
    return 0.00501711*x - 1.01229046

def trial_2_latter_half_trendline_2nd_iteration(x):
    return 0.00561423*x - 1.13247935


def trial_3_trendline(x):
    return 406.884917*np.exp(-0.032876741*x)


def remove_erroneous_voltages(angle, volts):
    new_angles, new_volts = [], []
    for i in range(500, len(angle)):
        if volts[i] > trial_2_latter_half_trendline_guess(angle[i]):
            new_angles.append(angle[i])
            new_volts.append(volts[i])
    return new_angles, new_volts


lines = open_file("brewster_angle.csv")
angle, volts = get_trial(lines, 1)
ns_angle, ns_volts = [], []
for i in range(len(angle)):
    if not (angle[i] < 185 and volts[i] < 0.35):
        ns_angle.append(angle[i])
        ns_volts.append(volts[i])
#get_exp_fit(angle, volts, (1000, -0.01))
n_angles, n_volts = remove_erroneous_voltages(angle, volts)
get_linear_fit(n_angles, n_volts)
coefs = get_exp_fit(ns_angle[175:450], ns_volts[175:450], (1000, -0.01))
x = np.linspace(200, 320, 200)
y = np.linspace(180, 240, 100)
plt.plot(x, trial_2_latter_half_trendline_2nd_iteration(x), y, coefs[0][0]*np.exp(coefs[0][1]*y))
plt.plot(ns_angle, ns_volts, n_angles, n_volts)
plt.show()
tr = []
for i in range(len(ns_angle[:550])):
    tr.append(ns_volts[i] - (coefs[0][0]*np.exp(coefs[0][1]*ns_angle[i])))

tr2 = []
for i in range(len(n_angles)):
    tr2.append(n_volts[i] - trial_2_latter_half_trendline_2nd_iteration(n_angles[i]))
plt.plot(ns_angle[:550], tr, n_angles, tr2)
plt.show()