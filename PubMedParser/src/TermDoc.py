import RecordHandler
from pysparse import spmatrix
import WordCounter
import RecordHandler

def countWords(dir, filename):
   
   l = []
   records = RecordHandler.loadMedlineRecords(dir,filename)
   interesting_records = RecordHandler.readMedlineFields(records,['AB'])

   for entry in interesting_records.items():
       l.append(WordCounter.wc(entry[0],entry[1]['AB']))

   return l

def populateMatrix(m,n,termDoc):

    M = spmatrix.ll_mat(m,n)

    # row number : m
    # col number : n

    termList=[]
    pmidList=[]
    for item in termDoc:
        pmidIndex=0
        termIndex=0

        if item[0] not in pmidList:
            pmidList.append(item[0])
            pmidIndex=len(pmidList)-1
        else:
            pmidIndex=pmidList.index(item[0])

        for term in item[1]:
            if term[0] not in termList:
                termList.append(term[0])
                termIndex=len(termList)-1
                M[pmidIndex,termIndex]=term[1]
            else:
                termIndex=termList.index(term[0])
                M[pmidIndex,termIndex]+=term[1]

    return M,termList,pmidList




