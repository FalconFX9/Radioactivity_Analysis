import math

Eb = 0.8
Ec = 0.95
ECB = Ec/Eb
counts_t0 = 46  # technically not true but not sure what else to use
R = 1.43  # need to guess and check
Ab_t0 = counts_t0/(1+ECB*R)


def counts(t):
    gC = math.log(2, math.e)/1194
    gB = math.log(2, math.e)/1620
    l_t = (1+ ECB*(gC/(gC-gB)))*math.exp(-gB*t)
    r_t = (ECB * (R - (gC / (gC - gB)))) * math.exp(-gC * t)
    return Ab_t0 * (l_t+r_t)


def bi212_exp(t):
    Bi212_t0 = 15
    return Bi212_t0 * math.exp(-t/3600)


def pb212_exp(t):
    Pb212_t0 = 4
    return Pb212_t0 * math.exp(-t/(10.6*3600))


def counts_bi212(t):
    return counts(t) + pb212_exp(t)


def trendline(count):
    return 48.6004365*math.exp(-0.0168719*count)
