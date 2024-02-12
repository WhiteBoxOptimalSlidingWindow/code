from sage.all import binomial, ceil, VectorSpace, GF

from itertools import combinations

import sage.modules.vector_mod2_dense, sage.matrix.matrix_mod2_dense

def correlation(v1, v2, T):
    #v1 and v2 are two vector in GF(2)^T
    #T: number of traces

    n00=0
    n01=0
    n10=0
    n11=0

    for i in range(T):
        if v1[i]:
            if v2[i]:
                n11+=1
            else:
                n10+=1
        else:
            if v2[i]:
                n01+=1
            else:
                n00+=1
    denom=((n00+n01)*(n00+n10)*(n11+n01)*(n11+n10))
    if denom==0:
        return(0)
    return(abs( (n11*n00 - n01*n10) / denom ))



def HODCA(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree, Solution):
    #WINDOW: List of all vectors corresponding to the node vectors
    #W: Window size correxponding to the number of node vectors of Window
    #ExtWinSize: Size of the window after extension. ExtWinSize=sum([binomial(W,i) for i in range(Degree)]
    #T: Number of traces. T>=ExtWinSize
    #K: Number of elements in the set of all considered selection functions
    #SELECTIONVECTORS: List of the K 1xW matrix corresponding to the selection vectors
    #Degree: The degree of HODCA. Degree>1
    #Solution: The previously computed correlations between node vectors and selection vectors

    #Extending the window with the AND combinations of node vectors
    for combSize in range(2,Degree+1):
        for comb in combinations(WINDOW[0:W], combSize):
            sumVect=comb[0]
            for vect in comb[1:]:
                sumVect+=vect
            WINDOW.append(sumVect)

    for nodeVect in WINDOW:
        for SelVecIdx in range(K):
            cor=correlation(nodeVect,SELECTIONVECTORS[SelVecIdx],T)
            if cor>Solution[SelVecIdx]:
                Solution[SelVecIdx]=cor

    return(Solution)


def verifyHODCAinputs(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree, Solution):
    assert W>0, "W should be greater than zero"
    assert Degree>1, "The Degree should be greater than 1"
    assert ExtWinSize==sum([binomial(W,i) for i in range(1,Degree+1)])
    assert T>=ExtWinSize, "T should be greater or equal than ExtWinSize"
    assert K>0, "K should be greater than zero"

    assert type(WINDOW)==list, "The input WINDOW should be a LIST of node vectors"
    assert len(WINDOW)==W, "The input WINDOW should contain W node vectors"
    for vect in WINDOW:
        assert type(vect)==sage.modules.vector_mod2_dense.Vector_mod2_dense, "The list of WINDOW should contain vectors in GF(2) representing selection vectors"
        assert len(vect)==T, "A selection vector should contain T elements"

    assert type(SELECTIONVECTORS)==list, "SELECTIONVECTORS should be a LIST of selection vectors"
    assert len(SELECTIONVECTORS)==K, "K should be equal to the length of SELECTIONVECTORS"
    for vect in SELECTIONVECTORS:
        assert type(vect)==sage.modules.vector_mod2_dense.Vector_mod2_dense, "The list of SELECTIONVECTORS should contain matrices representing selection vectors"
        assert len(vect)==T, "A selection vector should contain T elements"

    assert len(Solution)==K, "The length of the list containing the correlations corresponding to the set of all considered selection functions should be equal to K"

ListTracesDeg2=[1, 13, 21, 34, 50, 70, 95, 131, 169, 212, 271, 344, 417, 502, 619, 740, 869, 1037, 1218, 1408, 1650, 1900, 2173, 2503, 2834, 3232, 3648, 4118, 4632, 5192, 5800, 6456, 7174, 7958, 8796, 9705, 10690, 11733, 12877, 14083, 15403, 16785, 18227, 19792, 21492, 23254, 25160, 27223, 29349, 31583, 33925, 36442, 39145, 41896, 44841, 47993, 51273, 54677, 58307, 62178, 66064, 70193, 74580, 78949, 83883, 88797, 93999, 99321, 104946, 110685, 116737, 123121, 129854, 136700, 143641, 151495, 159187, 166959, 175436, 183659, 192984, 202029, 211498, 221411, 231789, 241747, 253078, 263951, 276323, 288195, 300578, 313493, 326656, 340054, 354000, 368518, 382913, 399366, 414966, 431175]

ListTracesDeg3=[1, 26, 88, 253, 659, 1507, 3249, 6510, 12307, 22017, 37755, 62088, 98467, 151546, 226135, 329484, 469771]

def generateRandomInputsHODCA(W, K, Degree, Solution, exigedPsucc=0.90):

    ExtWinSize=sum([binomial(W,i) for i in range(1,Degree+1)])

    assert Degree in [2,3], "The number of required traces are not prepared for Degree=%d" % Degree

    if Degree==2:
        assert W<=len(ListTracesDeg2), "The number of traces required for performing HODCA of degree 2 has been prepared for a maximum window size=%d" % len(ListTracesDeg2)
        T=ListTracesDeg2[W-1]

    if Degree==3:
        assert W<=len(ListTracesDeg3), "The number of traces required for performing HODCA of degree 3 has been prepared for a maximum window size=%d" % len(ListTracesDeg3)
        T=ListTracesDeg3[W-1]

    VS=VectorSpace(GF(2), T)
    WINDOW = [VS.random_element() for _ in range(W)]

    SELECTIONVECTORS=[VS.random_element() for _ in range(K)]

    verifyHODCAinputs(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree, Solution)

    return(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree)
