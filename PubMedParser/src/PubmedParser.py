from Bio import Entrez
from Bio import Medline
import urllib

def getArticles(diseaseDictionary):

    """
    Takes a dictionary of the form: {'disease xx': {'terms' : [xx, yy], 'uid' : nnnnnn }, etc}}
    And returns a dictionary containing:
    {'disease a': [pmid1, pmid2, pmid3...], 'disease b' : [pmidx, pmidy,...], ...}

    Duplicate are currently not considered, but should be.
    """

    diseaseArticleIDlist = {}

    for disease in diseaseDictionary:
        diseaseArticleIDlist[disease]=[]

        if (diseaseDictionary[disease]['terms'] != []):
            for searchterm in diseaseDictionary[disease]['terms']:
                diseaseArticleIDlist[disease].extend(getArticleIDlist(searchterm,0))

        if (diseaseDictionary[disease]['uid'] != ''):
            print 'Downloading from uid', diseaseDictionary[disease]['uid']
            diseaseArticleIDlist[disease].extend(getArticleIDsFromLink(diseaseDictionary[disease]['uid']))

    return diseaseArticleIDlist

def removeDuplicates(listOfIDs):

    d = {}

    for x in listOfIDs: d[x] = x

    listOfIDs = d.values()

    return listOfIDs

def getArticlesFromSearchTerm(searchTermList):

    """
    Recieves a list of search term, and returns the list of pubmed
    references containing an abstract.
    """

    Entrez.email = 'michael@diku.dk'

    articleList = []
    
    for searchTerm in searchTermList:
        print 'search term: ', searchTerm
        unquotedURL = urllib.unquote_plus(searchTerm + ' AND hasabstract[text]') # Replace %xx and '+' from search term
        print 'unquoted search term', unquotedURL
        pmids = getArticleIDlist(unquotedURL, 0)
        articleList.extend(getMedlineList(pmids))
        print 'article list size:', len(articleList)

    print 'total number of articles return from search term list:', len(articleList)

    return articleList

def getArticlesFromLink(from_uidList):

    """
    Helper function that is able to handle the special type of links
    that are sometimes returned by rarediseasesdatabase.com, it
    recieves a list of "from_uid" and returns all the pubmed articles
    containing an abtract.
    """

    Entrez.email = 'michael@diku.dk'

    results = []
    ids=[]

    for uid in from_uidList:
        handle=Entrez.elink(db='omim', LinkName='omim_pubmed_calculated', from_uid=uid)
        results.extend(Entrez.read(handle))

    for i in range(len(results)):
       ids.extend([link['Id'] for link in results[i]['LinkSetDb'][0]['Link']])

    articleList = getMedlineList(ids)

    return articleList

def getArticleIDsFromLink(uid):

    """
    Helper function that is able to handle the special type of links
    that are sometimes returned by rarediseasesdatabase.com, it
    recieves a "uid" and returns all the pubmed IDs containing
    an abtract.
    """

    Entrez.email = 'michael@diku.dk'

    handle=Entrez.elink(db='omim', LinkName='omim_pubmed_calculated', from_uid=uid)
    results = Entrez.read(handle)

    ids = [link['Id'] for link in results[0]['LinkSetDb'][0]['Link']]

    return ids


def getArticleCount(search_term):

    """
    This function takes search terms and returns the total number of
    found articles in the PubMed database.
    """

    Entrez.email = 'henrikgjensen@gmail.com'

    handle=Entrez.esearch(db='pubmed',term=search_term,retmax='0')
    record=Entrez.read(handle)
    retmax_length=record['Count']
    print 'Counted a total of',retmax_length,'articles'
    return retmax_length

def getArticleIDlist(search_term,number_of_articles=20):

    """
    This function takes search terms and an integer representing how
    many articles that should be searched for. A list of article-ids
    is returned.  If no number is given, 20 articles will be
    returned. If 0 is given, all articles found will be returned.
    """

    Entrez.email = 'henrikgjensen@gmail.com'

    if number_of_articles==0 : number_of_articles=int(getArticleCount(search_term))

    pmids=[]
    for i in range(0,int(number_of_articles),100000):
        handle=Entrez.esearch(db='pubmed',term=search_term,
            retmax=number_of_articles,retstart=i)
        record=Entrez.read(handle)
        pmids.extend(record['IdList'])
        print 'Downloaded',len(pmids),'PMIDs.',str(number_of_articles-len(pmids)),'remaining...'
    return pmids


def getMedlineList(pmids):

    """
    This function takes a list of article-ids and returns a list of MedLine
    articles that contains an abstract.
    """

    records = []
    cleaned_records = []
    listLength = len(pmids)

    Entrez.email = 'henrikgjensen@gmail.com'

    for i in range(0, listLength, 650):
        tempList = pmids[i:i + 650]
        handle = Entrez.efetch(db='pubmed', id=tempList,rettype='medline', retmode='text')
        records.extend(list(Medline.parse(handle)))
        print 'Downloaded',len(records),'MedLine articles.',str(listLength-len(records)),'remaining...'

    for article in records:
        if 'AB' in article:
            cleaned_records.append(article)
    
    print 'Returned',len(cleaned_records),'MedLine articles containing an abstract.'
    return cleaned_records

def writeOut(list):
    count=0
    out=file('data.txt','w')
    for i in list:
        out.write(str(i)+'\n')
        count+=1
        print 'Wrote out liste element ',str(count)
        
"""
def printRecords(records):

    # Recieves a list of records and prints title, author (if it
    # exists) and source (if it exists)

    for record in records:
        print 'title:', record['TI'].lower()
        if 'AU' in record:
            print 'author:', record['AU']
        if 'SO' in record:
            print 'source:', record['SO']
        print

def print_abstracts(records):

    # Recives a list of records and prints title and abstract (if it
    # exists)

    for record in records:
        print 'title:', record['TI']
        if 'AB' in record:
            print 'abstract:', record['AB']
"""
