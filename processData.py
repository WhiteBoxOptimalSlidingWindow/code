import pickle
import argparse
import pathlib

def readFile(pathToResultFile):
    try:
        with open(pathToResultFile, "rb") as file:
            L=pickle.load(file)
    except IOError as err:
        "The given path to the pickle file is incorrect"
        print(err)
        exit()

    AttackName =                 L[0]
    ListOfEffectiveWindowSizes = L[1]
    K =                          L[2]
    nIterations =                L[3]
    Degree =                     L[4]
    Noise =                      L[5]

    TIMINGS = [i for i in L[6:]]

    PossibleAttacks=['LDA','HDDA','HODCA','WBLPN']
    assert AttackName in PossibleAttacks, "The attack %s is not recognized, possibe attacks: \'LDA\', \'HDDA\', \'HODCA\', or \'WNLPN\'" % AttackName
    assert len(TIMINGS)<=len(ListOfEffectiveWindowSizes)

    return(AttackName, ListOfEffectiveWindowSizes, K, nIterations, Degree, Noise, TIMINGS)

def printAverage(pathToResultFile):
    (AttackName, ListOfEffectiveWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("AVERAGE")
    for timings in TIMINGS:
        if len(timings)==nIterations:
            print(sum(timings)/nIterations)
        else:
            print("Stopped: missing some iterations")
            break
    return(1)

def printMin(pathToResultFile):
    (AttackName, ListOfEffectiveWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("MIN")
    for timings in TIMINGS:
        if len(timings)==nIterations:
            print(min(timings))
        else:
            print("Stopped: missing some iterations")
            break
    return(1)

def printMax(pathToResultFile):
    (AttackName, ListOfEffectiveWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("MAX")
    for timings in TIMINGS:
        if len(timings)==nIterations:
            print(max(timings))
        else:
            print("Stopped: missing some iterations")
            break
    return(1)

def printWindowSizes(pathToResultFile, E=0):
    (AttackName, ListOfEffectiveWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("WINDOW SIZES")
    for i in range(E,len(TIMINGS)):
        if len(TIMINGS[i])==nIterations:
            print(ListOfEffectiveWindowSizes[i])
        else:
            print("Stopped: missing some iterations")
            break
    return(1)

def printPacesForOneEWS(pathToResultFile, E):
    (AttackName, ListOfWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("PACES FOR EFFECTIVE WINDOW SIZE E=%d" % E)
    avg=[]
    for timings in TIMINGS:
        if len(timings)==nIterations:
            avg.append(sum(timings)/nIterations)

    for j in range(E, len(avg)):
        W=ListOfWindowSizes[j]
        print(avg[j]/(W-E+1))
    return(1)


def printOptimalParameter(pathToResultFile, mode='opt'):
    (AttackName, ListOfWindowSizes, K, nIterations, Degree, Noise, TIMINGS)=readFile(pathToResultFile)
    print("OPTIMAL PARAMETERS")
    avg=[]
    for timings in TIMINGS:
        if len(timings)==nIterations:
            avg.append(sum(timings)/nIterations)

    for i in range(len(avg)):
        E = ListOfWindowSizes[i]
        minPace=avg[i]
        stop=False
        for j in range(i+1,len(avg)):
            W=ListOfWindowSizes[j]
            pace=avg[j]/(W-E+1)
            if pace < minPace:
                minPace=pace
            else:
                if j==len(avg)-1:
                    stop=True
                    break
                else:
                    if mode == 'opt':
                        print("E=%d\tW=%d\tpace=%f" % (E, W, minPace))
                    elif mode == 'E':
                        print(E)
                    elif mode == 'W':
                        print(W)
                    elif mode =='pace':
                        print("%.20f" % minPace)
                    break
        if stop:
            break
    return(1)

if __name__ == '__main__' and '__file__' in globals():
    parser = argparse.ArgumentParser(
        description='description to do later',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        'trace_dir', type=pathlib.Path,
        help="path to the pickle file containing time results"
    )

    parser.add_argument(
        '--mode', type=str, default="opt",
        help="What to print ? \n'avg': average timings, \n'min': min timings, \n'max': max timings, \n'win': Window sizes, \n'opt': optimal window and pace for each effective window size, \n'E': effective window size for each optimal parameter, \n'W': optimal window size for each effectve window size, \n'pace': in practice best possible pace"
    )

    parser.add_argument(
        '-E', '--effective-window-size', type=int, default=0,
        help="Effective Window size"
    )

    args = parser.parse_args()

    assert args.mode in ['avg', 'min', 'max', 'win', 'opt', 'E', 'W', 'pace', 'paces'], "--mode should be chosen amongst:\n'avg': average timings, \n'min': min timings, \n'max': max timings, \n'win': Window sizes, \n'opt': optimal window and pace for each effective window size, \n'E': effective window size for each optimal parameter, \n'W': optimal window size for each effectve window size, \n'pace': in practice best possible pace, \n'pace': different possible window sizes for one choosen effective window size"

    if args.mode=='avg':
        printAverage(args.trace_dir)

    elif args.mode=='min':
        printMin(args.trace_dir)

    elif args.mode=='max':
        printMax(args.trace_dir)

    elif args.mode=='win':
        printWindowSizes(args.trace_dir, args.effective_window_size)

    elif args.mode=='paces':
        printPacesForOneEWS(args.trace_dir, args.effective_window_size)

    else:
        printOptimalParameter(args.trace_dir, args.mode)
