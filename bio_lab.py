import matplotlib.pyplot as plt


def get_data(file):
    lines = open(file)
    lines = lines.readlines()
    time = []
    ufor = []
    lfor = []
    lines = lines[2:]
    n = 0
    for i in range(0, len(lines), 20):
        line = lines[i]
        n+=1
        separated_data = line.split(",")
        time_str = separated_data[0].split(":")
        time.append(float(time_str[1])*60 + float(time_str[2]))
        ufor.append(float(separated_data[1]))
        lfor.append(float(separated_data[2]))
    return [time, ufor, lfor]


time, ufor, lfor = get_data("Artur\\aim_test4.csv")
plt.plot(time, ufor, time, lfor)
plt.legend(["Forearm Flexors", "Wrist Flexors"])
plt.title("Aim Test -- After 3 mins of recovery time")
plt.show()