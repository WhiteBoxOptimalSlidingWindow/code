from sage.all import Matrix, GF, vector, ceil

from time import time
import sys
import argparse
import pickle

from LDA import LDA, verifyLDAinputs, generateRandomInputsLDA
from HDDA import HDDA, verifyHDDAinputs, generateRandomInputsHDDA
from HODCA import HODCA, verifyHODCAinputs, generateRandomInputsHODCA
from WBLPN import WBLPN, generateRandomInputsWBLPN, prepareProbabilisticParameters

def MeasureTime(ListOfWindowSizes, K, nIterations, AttackName, Degree=2, Noise=1/8, stopAtMaxTime=120, record=0):
    #ListOfWindowSizes: List of window sizes to perform measurments
    #K: Number of elements in the set of all considered selection functions
    #nIterations: Number of iterations per given window size
    #AttackName: List of attacks names to perform computations on. Possible attacks: 'LDA', 'HDDA' and 'HODCA'
    #Degree: The degree corresponding to the degree of HDDA or the order of HODCA
    #stopAtMaxTime: If a mean measurment exceeds stopAtMaxTime seconds, do not compute the next window sizes
    #record: If record equals 0, don't record the outputs in a file, otherwise, a file will be created containing all information

    PossibleAttacks=['LDA','HDDA','HODCA','WBLPN']

    assert AttackName in PossibleAttacks, "The attack %s is not recognized, please choose from \'LDA\', \'HDDA\', \'HODCA\', or \'WNLPN\'" % AttackName
    print("Time measurments for " + str(AttackName))
    if record:
        Results=[AttackName, ListOfWindowSizes, K, nIterations, Degree, Noise]


    if AttackName=='LDA':
        try:
            for E in ListOfWindowSizes:
                print()
                print(" window size = %d" % E)
                times=[]
                for iter in range(nIterations):
                    (Window, E, T, K, SELECTIONVECTORS) = generateRandomInputsLDA(E, K)
                    t1=time()
                    LDA(Window, E, T, K, SELECTIONVECTORS)
                    t2=time()
                    diff=t2-t1
                    if diff >= 1:
                        print("%fs" % (diff))
                    else:
                        print("%fms" % (diff*1000))
                    times.append(diff)
                    average=sum(times)/nIterations
                if average >= 1:
                    print("Average: %fs" % average)
                else:
                    print("Average: %fms" % (average*1000))

                if record:
                    Results.append(times)

                if average>stopAtMaxTime:
                    break

            if record:
                ftime = "timeResults/times_LDA_from%d_to%d_K%d.pkl" % (ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)
        except KeyboardInterrupt:
            if record:
                ftime = "timeResults/times_LDA_from%d_to%d_K%d_Unfinished.pkl" % (ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)

    elif AttackName=='HDDA':
        try:
            for E in ListOfWindowSizes:
                print()
                print(" window size = %d" % E)
                times=[]
                for iter in range(nIterations):
                    (WINDOW, E, ExtWinSize, T, K, SELECTIONVECTORS, Degree) = generateRandomInputsHDDA(E, K, Degree)
                    t1=time()
                    HDDA(WINDOW, E, ExtWinSize, T, K, SELECTIONVECTORS, Degree)
                    t2=time()
                    diff=t2-t1
                    if diff >= 1:
                        print("%fs" % (diff))
                    else:
                        print("%fms" % (diff*1000))
                    times.append(diff)
                    average=sum(times)/nIterations
                if average >= 1:
                    print("Average: %fs" % average)
                else:
                    print("Average: %fms" % (average*1000))

                if record:
                    Results.append(times)

                if average>stopAtMaxTime:
                    break

            if record:
                ftime = "timeResults/times_HDDA_Deg%d_from%d_to%d_K%d.pkl" % (Degree, ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)
        except KeyboardInterrupt:
            if record:
                ftime = "timeResults/times_HDDA_Deg%d_from%d_to%d_K%d.pkl_Unfinished" % (Degree, ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)

    elif AttackName=='HODCA':
        try:
            for E in ListOfWindowSizes:
                Solution = [0 for _ in range(K)]
                print()
                print(" window size = %d" % E)
                times=[]
                for iter in range(nIterations):
                    (WINDOW, E, ExtWinSize, T, K, SELECTIONVECTORS, Degree) = generateRandomInputsHODCA(E, K, Degree, Solution, exigedPsucc=0.90)
                    t1=time()
                    Solution=HODCA(WINDOW, E, ExtWinSize, T, K, SELECTIONVECTORS, Degree, Solution)
                    t2=time()
                    diff=t2-t1
                    if diff >= 1:
                        print("%fs" % (diff))
                    else:
                        print("%fms" % (diff*1000))
                    times.append(diff)
                    average=sum(times)/nIterations
                if average >= 1:
                    print("Average: %fs" % average)
                else:
                    print("Average: %fms" % (average*1000))

                if record:
                    Results.append(times)

                if average>stopAtMaxTime:
                    break

            if record:
                ftime = "timeResults/times_HODCA_Deg%d_from%d_to%d_K%d.pkl" % (Degree, ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)
        except KeyboardInterrupt:
            if record:
                ftime = "timeResults/times_HODCA_Deg%d_from%d_to%d_K%d_Unfinished.pkl" % (Degree, ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)

    elif AttackName=='WBLPN':
        (mARRAY, cARRAY, aARRAY)=prepareProbabilisticParameters(ListOfWindowSizes[-1], K, Noise)
        try:
            for E in ListOfWindowSizes:
                print()
                print(" window size = %d" % E)
                times=[]
                for iter in range(nIterations):
                    (Mpool, Spool, Mv, Sv, Solution, mARRAY, cARRAY, aARRAY) = generateRandomInputsWBLPN(E, K, Noise, mARRAY, cARRAY, aARRAY)
                    t1=time()
                    Solution=WBLPN(Mpool, Spool, Mv, Sv, Solution, mARRAY, cARRAY, aARRAY)
                    t2=time()
                    diff=t2-t1
                    if diff >= 1:
                        print("%fs" % (diff))
                    else:
                        print("%fms" % (diff*1000))
                    times.append(diff)
                    average=sum(times)/nIterations
                if average >= 1:
                    print("Average: %fs" % average)
                else:
                    print("Average: %fms" % (average*1000))

                if record:
                    Results.append(times)

                if average>stopAtMaxTime:
                    break

            if record:
                ftime = "timeResults/times_WBLPN_Noise0-%04d_from%d_to%d_K%d.pkl" % (ceil(Noise*1000), ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)
        except KeyboardInterrupt:
            if record:
                ftime = "timeResults/times_WBLPN_Noise0-%04d_from%d_to%d_K%d_Unfinished.pkl" % (ceil(Noise*1000), ListOfWindowSizes[0], ListOfWindowSizes[-1], K)
                with open(ftime, "wb") as file:
                    pickle.dump(Results, file)


if __name__ == '__main__' and '__file__' in globals():
    parser = argparse.ArgumentParser(
        description='description to do later',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-A', '--AttackName', type=str, default='LDA',
        help="The name of the desired attack to perform the measurements amongst \'LDA\', \'HDDA\', \'HODCA\', and \'WNLPN\'"
    )

    parser.add_argument(
        '-F', '--From', type=int, default=5,
        help="The window size value from witch to perform time measurments, the mesurements will be performed on window sizes in range(--from,--to,--by)"
    )

    parser.add_argument(
        '-T', '--To', type=int, default=31,
        help="The window size value up to witch to perform time measurments, the mesurements will be performed on window sizes in range(--from,--to,--by)"
    )

    parser.add_argument(
        '-B', '--By', type=int, default=1,
        help="The step refering to the incrementation for the time measurments for the window sizes, the mesurements will be performed on window sizes in range(--from,--to,--by)"
    )

    parser.add_argument(
        '-K', '--KeySpace', type=int, default=4096,
        help="The size of the key space to perform the time measurments with, corresponds to |K| in the paper\nFor HODCA, the key space should be 4096 or you you have to recompute the number of traces required with the HODAcomputeTraces.py"
    )

    parser.add_argument(
        '-I', '--Iterations', type=int, default=10,
        help="The number of iterations to perform for each window size"
    )

    parser.add_argument(
        '-d', '--Degree', type=int, default=2,
        help="The degree / order of HDDA / HODCA, useless parameter for other attacks"
    )

    parser.add_argument(
        '-n', '--Noise', type=float, default=2,
        help="The noise of the countermeasure for WBLPN: 1/2^n, useless parameter for other attacks"
    )

    parser.add_argument(
        '-m', '--MaxTime', type=float, default=120,
        help="The maximum time (in seconds) authorized to perform measurements. If the average of I Iterations exceeds this value, the measurments stop"
    )

    parser.add_argument(
        '-r', '--Record', type=int, default=1,
        help="if r=1, the measurments will create a pickle file containing all the useful informations to recover information from, that can be processed with processData.py aferwards"
    )

    args = parser.parse_args()

    MeasureTime(range(args.From, args.To, args.By), args.KeySpace, args.Iterations, args.AttackName, args.Degree, 1/(2**args.Noise), args.MaxTime, args.Record)
