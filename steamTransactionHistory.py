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
    try:
        if 'document' in transHistSoup.name:
            return transHistSoup
        else:
            raise ValueError
    except ValueError:
        sys.exit('Houston, we have a problem, the Soup was not made.\nChances are the .htm / .html file you saved from your steam transaction history is not in the same directory as this app')

def dataScrubber(transHist):
    '''Creates lists of relevent columns, excludes all entries before 1/28/2017, as well as
    removes transactions that are not games, before creating the dictionary which will create
    the dataframe. Credit to Alexander Lacson's post on Medium from May 21, 2021 for the code that
    creates the precursor lists and does some cleaning.
    '''
    frameDict = {}

    exclusions = ['in-game purchase', 'wallet credit', "steam promotion"]
    #The elimination of non-qualifying purchases could probably be determined via a comparison of type with "Purchase" as an allowed member, however this is more modular.
    #All are lowercase, because I am going to casefold for comparison.

    #Date
    wht_date = transHist.select(".wht_date")
    wht_date = [each.get_text() for each in wht_date[1:]]

    #Items (game name)
    wht_items = transHist.select(".wht_items")
    wht_items = [each.get_text().replace("\n", "_").replace("\t", '') for each in wht_items[1:]]

    print(wht_items)

    return frameDict






    

def createDF(transDict):
    '''Literally just declares a global variable to store the dataframe and creates it from the
    passed dictionary
    '''
    global transactions 
    transactions = pd.DataFrame.from_dict(transDict)

def outputTotal():
    pass

def main ():

    rawHTML = findandSoup()
    if 'document' in rawHTML.name:
        print('Soups Done, Time to Strain')
        
    
    transDict = dataScrubber(rawHTML)
    #createDF(transDict)
    #outputTotal(transactions)


if __name__ == '__main__':
    
    main()


    
