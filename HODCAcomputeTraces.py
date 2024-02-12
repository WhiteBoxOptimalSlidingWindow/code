from sage.all import binomial, ceil, RealField, RR, pi, sqrt, exp, log
from functools import cache
import scipy.stats
import pickle

##############################################################################################
#           From "Higher-Order DCA against Standard Side-Channel Countermeasures"            #

RF = RealField(200)

#@cache
def CDF(k, n, p):
    binom_dist = scipy.stats.binom(n, p)
    return(binom_dist.cdf(k))

def Fxmax(x, N, p, K, d, t):
    return(CDF(x, N, RF(1-p)*(1/K))**binomial(t,d))

def Fstarmax(x, N, p, K, d, t):
    return(CDF(x, N, p + RF(1-p)*(1/K))**binomial(t,d))

def Psucc(N, p, K, d, t):
    sum = 0
    for i in range(1,N+1):
        sum += (Fstarmax(i, N, p, K, d, t)-Fstarmax(i-1, N, p, K, d, t)) * Fxmax(i-1, N, p, K, d, t)
    return(sum**(K-1))

#                                                                                          #
############################################################################################

def DetermineNumOfTracesHODCA(E, K, Degree, beginValue=1, exigedPsucc=0.90, precision=0.001, record=1):
    t = E*Degree
    p = 1/binomial(t,Degree)

    T=beginValue
    psucc=Psucc(T, p, K, Degree, t)
    prev=0
    while psucc < exigedPsucc:
        prev=T
        T*=2
        psucc=Psucc(T, p, K, Degree, t)
        print("T=%d, psucc=%.20f" % (T,psucc))

    print()
    lower=prev
    upper=T
    while (upper-lower>1) and (abs(psucc-exigedPsucc)>precision):
        T=lower+(upper-lower)//2
        psucc=Psucc(T, p, K, Degree, t)

        if psucc > exigedPsucc:
            upper=T
        else:
            lower=T

        print("T=%d, psucc=%.20f" % (T,psucc))
    print("T=%d"%T)
    print()
    return(T)


def ComputeAllNeededTraces(record=1):
    """
    print("___________________DEGREE 2___________________")
    L2=[1]
    try:
        for E in range(93,101):
            print("--------- E=%d ---------"%E)
            L2.append(DetermineNumOfTracesHODCA(E, 4096, 2, beginValue=L2[-1]))

        print(L2)
    except KeyboardInterrupt:
        print()
        print(L2)
        if record:
            fntraces = "TracesDeg2HODCA_unfinished.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L2, file)
        exit()
    if record:
        if record:
            fntraces = "TracesDeg2HODCA.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L2, file)
    """

    #[1, 13, 21, 34, 50, 70, 95, 131, 169, 212, 271, 344, 417, 502, 619, 740, 869, 1037, 1218, 1408, 1650, 1900, 2173, 2503, 2834, 3232, 3648, 4118, 4632, 5192, 5800, 6456, 7174, 7958, 8796, 9705, 10690, 11733, 12877, 14083, 15403, 16785, 18227, 19792, 21492, 23254, 25160, 27223, 29349, 31583, 33925, 36442, 39145, 41896, 44841, 47993, 51273, 54677, 58307, 62178, 66064, 70193, 74580, 78949, 83883, 88797, 93999, 99321, 104946, 110685, 116737, 123121, 129854, 136700, 143641, 151495, 159187, 166959, 175436, 183659, 192984, 202029, 211498, 221411, 231789, 241747, 253078, 263951, 276323, 288195, 300578, 313493, 326656, 340054, 354000, 368518, 382913, 399366, 414966, 431175]

    print("___________________DEGREE 3___________________")
    L3=[1]
    try:
        for E in range(2,51):
            print("--------- E=%d ---------"%E)
            L3.append(DetermineNumOfTracesHODCA(E, 4096, 3, beginValue=L3[-1]))

        print(L3)
    except KeyboardInterrupt:
        print()
        print(L3)
        if record:
            fntraces = "TracesDeg3HODCA_unfinished.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L3, file)
        exit()
    if record:
        if record:
            fntraces = "TracesDeg3HODCA.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L3, file)

    """
    print("___________________DEGREE 4___________________")
    L4=[1]
    try:
        for E in range(2,6):
            print("--------- E=%d ---------"%E)
            L4.append(DetermineNumOfTracesHODCA(E, 4096, 4, beginValue=L3[-1]))

        print(L4)
    except KeyboardInterrupt:
        print()
        print(L4)
        if record:
            fntraces = "TracesDeg4HODCA_unfinished.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L4, file)
        exit()
    if record:
        if record:
            fntraces = "TracesDeg4HODCA.pkl"
            with open(fntraces, "wb") as file:
                pickle.dump(L4, file)
    """
    return

ComputeAllNeededTraces(record=1)
