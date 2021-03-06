import SearchTermDoc 
import math

def cosineMeasure(M_lil, M_csc, queryString):

    """
    This function calculates the square-root of the cosine score for each
    document containing one or more of the query-terms in the query string
    (thereby the implicit 'or' between each query-term).

    It returns a scored list of all the documents mentioned above.
    """

    # Extract the relevant indices of the row-vectors (pmid-hashes)
    searchIndices,hashedSearchTerms = SearchTermDoc.extractRowIndices(M_csc, queryString)

    # Union the arrays to avoid searching each row more than once
    searchIndices = reduce(set.union,map(set,searchIndices))

    results=[]
    for pmidHash in searchIndices:
        Sum=0
        for termHash in hashedSearchTerms:
            Sum+=M_lil[pmidHash,termHash]
        results.append((Sum,pmidHash))

    return results
