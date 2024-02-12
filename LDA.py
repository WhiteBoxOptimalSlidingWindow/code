from sage.all import Matrix, VectorSpace, MatrixSpace, GF, vector

import sage.modules.vector_mod2_dense, sage.matrix.matrix_mod2_dense

def LDA(Window, W, T, K, SELECTIONVECTORS):
    #Window: Matrix in GF(2)
    #W: Window size corresponding to the number of node vectors of Window
    #T: Number of traces. T>=W, ideally T=W+30
    #K: Number of elements in the set of all considered selection functions
    #SELECTIONVECTORS: List of the K T-element vectors corresponding to the selection vectors

    #Computing the Parity Check Matrix
    PCM=Window.right_kernel_matrix()

    #Verifying if one of the selection vectors nullify the product, if so, we found a solution
    Solution=[]
    for SelVecIdx in range(K):
        if not PCM * SELECTIONVECTORS[SelVecIdx]:
            Solution.append(K)

    return(K)

def verifyLDAinputs(Window, W, T, K, SELECTIONVECTORS):
    assert W>0, "W should be greater than zero"
    assert T>=W, "T should be greater or equal than W, ideally T=W+30"
    assert type(Window)==sage.matrix.matrix_mod2_dense.Matrix_mod2_dense, "The input Window should be a matrix in GF(2)"
    assert Window.ncols()==T, "The input Window should have T columns"
    assert Window.nrows()==W, "The input Window should have W rows"
    assert K>0, "K should be greater than zero"
    assert type(SELECTIONVECTORS)==list, "SELECTIONVECTORS should be a LIST of selection vectors"
    assert len(SELECTIONVECTORS)==K, "K should be equal to the length of SELECTIONVECTORS"
    for vect in SELECTIONVECTORS:
        assert type(vect)==sage.modules.vector_mod2_dense.Vector_mod2_dense, "The list of SELECTIONVECTORS should contain matrices representing selection vectors"
        assert len(vect)==T, "A selection vector should contain T elements"

def generateRandomInputsLDA(W, K):
    T=W+30

    Window = MatrixSpace(GF(2), W, T).random_element()

    VS=VectorSpace(GF(2), T)
    SELECTIONVECTORS=[VS.random_element() for _ in range(K)]

    verifyLDAinputs(Window, W, T, K, SELECTIONVECTORS)

    return(Window, W, T, K, SELECTIONVECTORS)
