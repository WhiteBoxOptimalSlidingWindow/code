from sage.all import Matrix, GF, vector, binomial, VectorSpace, MatrixSpace

from itertools import combinations

import sage.modules.vector_mod2_dense, sage.matrix.matrix_mod2_dense

from LDA import LDA

def HDDA(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree):
    #WINDOW: List of all vectors corresponding to the node vectors
    #W: Window size correxponding to the number of node vectors of Window
    #ExtWinSize: Size of the window after extension. ExtWinSize=sum([binomial(W,i) for i in range(Degree)]
    #T: Number of traces. T>=ExtWinSize
    #K: Number of elements in the set of all considered selection functions
    #SELECTIONVECTORS: List of the K 1xW matrix corresponding to the selection vectors
    #Degree: The degree of HDDA. Degree>1

    #Extending the window with the AND combinations of node vectors
    for combSize in range(2,Degree+1):
        for comb in combinations(WINDOW[0:W], combSize):
            sumVect=comb[0]
            for vect in comb[1:]:
                sumVect+=vect
            WINDOW.append(sumVect)

    Window=MatrixSpace(GF(2), ExtWinSize, T)(WINDOW)

    Solution=LDA(Window, W, T, K, SELECTIONVECTORS)

    return(Solution)


def verifyHDDAinputs(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree):
    assert W>0, "W should be greater than zero"
    assert Degree>1, "The Degree should be greater than 1"
    assert ExtWinSize==sum([binomial(W,i) for i in range(1,Degree+1)])
    assert T>=ExtWinSize, "T should be greater or equal than ExtWinSize, ideally T=ExtWinSize+30"
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

def generateRandomInputsHDDA(W, K, Degree):
    ExtWinSize=sum([binomial(W,i) for i in range(1,Degree+1)])
    T=ExtWinSize+30

    VS=VectorSpace(GF(2), T)
    WINDOW = [VS.random_element() for _ in range(W)]

    SELECTIONVECTORS=[VS.random_element() for _ in range(K)]

    verifyHDDAinputs(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree)

    return(WINDOW, W, ExtWinSize, T, K, SELECTIONVECTORS, Degree)
