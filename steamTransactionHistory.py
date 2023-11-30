import pandas as pd #datatframes are useful
from bs4 import BeautifulSoup #we only need to parse the raw HTML no need to import all of BS4
import os #for paths
import re #it's re....
import sys #it's sys....
import traceback #for printing unexpected execeptions.

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
    
        

def comprehendData(transHist):
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
    wht_items = [each.get_text().replace("\\n", "_").replace("\\t", '') for each in wht_items[1:]]

    #transaction types
    wht_type = transHist.select(".wht_type")
    wht_type = [each.get_text().replace("\\n", "_").replace("\\t", '') for each in wht_type[1:]]

    #Individual transaction totals, this is the major rewrite to the previous found work, I could not make the list comprehension work as hard as I tried.
    wht_total_num = []
    wht_total = transHist.select(".wht_total")
    '''wht_total = [each.get_text().strip().replace("\\n", "").replace(',', '').replace("\\t", '').replace('$', '') for each in wht_total[1:]]
    for index, each in enumerate(wht_total):
        each = each.replace('$', '').replace("\\t", '').replace('\n', '_')
        newEach = ''
        for char in each:
            if char.isnumeric() or char == '.':
                 newEach += char
            wht_total_num.append(float(newEach))
        else:
            wht_total_num.append(0.0)'''
    wht_total=[each.get_text().strip().replace(',', '') for each in wht_total[1:]]
    for index, each in enumerate(wht_total[0:]):
        cleaned_string = each.replace('\t', '').replace('\n', '').replace('Credit', '').replace('$', '').strip()
        if cleaned_string == '':
            wht_total[index] = 0.0
        else:        
            wht_total[index] = cleaned_string

    for index, each in enumerate(wht_total[0:]):
            try:
                wht_total[index] = float(each)
            except:
                print(f"There Was a value error at {index} and {each} ")
    
    #print(sum(wht_total), len(wht_total))

    frameDict = {'Date' : wht_date, "Items" : wht_items, 'Type' : wht_type, 'Total' : wht_total}

    return frameDict

def createDF(transDict):
    '''Literally just declares a global variable to store the dataframe and creates it from the
    passed dictionary
    '''
    global transactions 
    transactions = pd.DataFrame.from_dict(transDict)

    transactions.Date = pd.to_datetime(transactions.Date, infer_datetime_format=True)

    print(transactions.head)
    transactions.to_excel('.\\transactions.xlsx')

def outputTotal():
    print(transactions["Total"].cumsum())

def main ():
    
    try:
        rawHTML = findandSoup()
        if 'document' in rawHTML.name:
            print('Soups Done, Time to Strain')
        else:
            raise TypeError
    except Exception as e:
        if type(e) == "TypeError":
            sys.exit('Houston, we have a problem, the soup was not made. This is most commonly due to the transaction history HTML file not existing in the same directory as the executable, ensure this and try again')
        else:
            traceback.print_exc()
            sys.exit("Post a screenshot of this to @Delvaris on Github, however how you managed this one it's amazing because I specifically raised a certain exception that it should have thrown instead. Enka.")

        
    try:
        transDict = comprehendData(rawHTML)
    except Exception:
        traceback.print_exc()
        sys.exit("Post a screenshot of this to @Devlaris on Github.")
    
    try:
        createDF(transDict)
    except Exception:
        traceback.print_exc()
        sys.exit("Post a screenshot of this to @Delvaris on Github")
    
    try:
        outputTotal()
    except Exception:
        traceback.print_exc()
        sys.exit("Post a screenshot of this to @Devlaris on Github")
    
    ending = input("\n Press any key to exit")


if __name__ == '__main__':
    
    main()


    
