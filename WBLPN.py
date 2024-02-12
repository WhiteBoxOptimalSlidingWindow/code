from sage.all import Matrix, RealField, sqrt, log, ceil, MatrixSpace, GF, Combinations

I=20      #Number of iterations of measuring time per window

pnfm=.999 #Probability of finding Noise-Free Matrix after A attempts
lenK=4096 #Corresponds to |K|, the number of key guesses
Tp=100    #Number of traces for sampling

RF=RealField(10000) #To ensure correct probabilistic parameters computation


##############################################################################################
#                     From "LPN-based Attacks in the White-box Setting"                      #

def WBLPN(Mpool, Spool, Mv, Sv, Solution, mARRAY, cARRAY, aARRAY):
    #Ensuring linearly independent columns, for potential invertible sampled matrices
    linIndColumns = Mpool.pivots()

    #Adapting probabilistic parameters to the potentially reduced LPN dimension
    Wprime=len(linIndColumns)
    m=mARRAY[Wprime-2]
    c=cARRAY[Wprime-1]
    A=aARRAY[Wprime-1]

    numberOfAttempts=0
    while numberOfAttempts < A:
        #Sampling Ms from the pool
        sampledRows=Combinations(range(Tp), Wprime).random_element()
        Ms=Mpool[sampledRows,linIndColumns]

        if Ms.is_invertible():
            MsInv=Ms.inverse()
            numberOfAttempts+=1

            #We transpose W since Sage computes hamming_weight faster for rows than columns
            W=(((Mv[range(m),linIndColumns]*MsInv)*Spool[sampledRows,range(lenK)])+Sv[range(m),range(lenK)]).transpose()

            for i in range(lenK):
                if W.row(i).hamming_weight() < c:
                    if i not in Solution:
                        Solution.append(i)
    return(Solution)

#                                                                                            #
##############################################################################################


RF=RealField(200)
def prepareProbabilisticParameters(maxW, K, Noise):
    ##############################################################################################
    #                     From "LPN-based Attacks in the White-box Setting"                      #
    mARRAY=[]
    cARRAY=[]
    aARRAY=[]
    for e in range(1,maxW+1):
        alpha = RF(1)/(2**e)
        beta = (1/lenK)*(((RF(1)-Noise)/2)**e)

        m = ((sqrt((3/2)*log(1/alpha))+sqrt(log(1/beta)))/((1/2)-Noise))**2
        mARRAY.append(ceil(m))

        c = Noise*m+sqrt(3*((1/2)-Noise)*log(1/alpha)*m)
        cARRAY.append(round(c))

        A=ceil(log(RF(1)-pnfm)/(log(1-(RF(1)-Noise)**e)))
        aARRAY.append(A)

    #                                                                                            #
    ##############################################################################################
    return(mARRAY, cARRAY, aARRAY)


def generateRandomInputsWBLPN(W, K, Noise, mARRAY, cARRAY, aARRAY):

    ##############################################################################################
    #                     From "LPN-based Attacks in the White-box Setting"                      #

    Mpool=MatrixSpace(GF(2), Tp, W).random_element()
    Spool=MatrixSpace(GF(2), Tp, lenK).random_element()

    m=mARRAY[W-1]
    Mv=MatrixSpace(GF(2), m, W).random_element()
    Sv=MatrixSpace(GF(2), m, lenK).random_element()

    #                                                                                            #
    ##############################################################################################

    Solution=[]

    return(Mpool, Spool, Mv, Sv, Solution, mARRAY, cARRAY, aARRAY)
