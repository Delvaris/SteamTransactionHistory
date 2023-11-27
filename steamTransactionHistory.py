import pandas as pd #daatframes are useful
from bs4 import BeautifulSoup #we only need to parse the raw HTML no need to import all of BS4
import os #for paths
import re #it's re....
import sys #it's sys....

def findandSoup():
    '''This finds what should be the only HTML file in the current working directory. 
    It will throw an error if it isn't. It parses that file into a BS4 document, and returns the
    document 
    '''
    path = os.getcwd()
    files = [x for x in os.listdir(path) if x.endswith('.htm') or x.endswith('.html')]
    if len(files) > 1:
        sys.exit('you know you shouldn\'t have more than one htm or html file here. stop trying to make me look bad.')
    file = files[0]
    transHistSoup = BeautifulSoup(open(file, encoding= "utf8"), "html.parser")
    return transHistSoup

def dataScrubber(transHist):
    '''Creates lists of relevent columns, excludes all entries before 1/28/2017, as well as
    removes transactions that are not games, before creating the dictionary which will create
    the dataframe.
    '''
    frameDict = {}
    exclusions = ['in-game purchase', 'wallet credit', "steam promotion", 'gift re']
    #The elimination of non-qualifying purchases could probably be determined via a comparison of type with "Purchase" as an allowed member, however this is more modular.
    #All are lowercase, because I am going to casefold for comparison.

    wht_date = transHist.select(".wht_date")
    wht_date = [each.get_text() for each in wht_date[1:]]
    return frameDict

def createDF(transDict):
    '''Literally just declares a global variable to store the dataframe and creates it from the
    passed dictionary
    '''
    global transactions 
    transactions = pd.DataFrame.from_dict(transDict)

def outputTotal():
    pass

if __name__ == '__main__':
    
    rawHTML = findandSoup()

    if 'document' in rawHTML.name:
        print('Soups Done, Creating something useful')
    else:
        print('Houston, we have a problem.')
    
    transDict = dataScrubber(rawHTML)
    createDF(transDict)
    outputTotal(transactions)


    
