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
    the dataframe. Credit to Alexander Lacson's, aka @Max_Turbo on Github, post on Medium from May 21, 2021 for the code that
    creates the precursor lists and does some cleaning. rewritten not pulled, Total section is a complete rewrite as his list comprehension did not work anymore.
    '''
    frameDict = {}

    #exclusions = ['in-game purchase', 'wallet credit', "steam promotion"]
    '''The elimination of non-qualifying purchases could probably be determined via a comparison of type with "Purchase" as an allowed member, however this is more modular.
        All are lowercase, because I am going to casefold for comparison.

        Note as of Nov 30, 2023 at 0700, release v3.0.1-alpha-:

        Currently considering final clean up with select statements instead of using further work on the lists. This parsing takes care of everything with Total so it can be converted to a float and a usable column. 
        It is TBD if I will apply similiar methods to completely clean the other columns. One advantage to not doing it is as it stands right now it works, all dates have a matching item, have a matching type, have a 
        matching total. The sheer amount of cleanup I had to do to the totals resulted in at least 2 entries on my personal transactions list that ended up completely nulled out. Given this it seems like working with 
        the set as a dataframe is the way forward.''' 

    #Date
    wht_date = transHist.select(".wht_date")
    wht_date = [each.get_text() for each in wht_date[1:]]

    #Items (game name)
    wht_items = transHist.select(".wht_items")
    wht_items = [each.get_text().replace("\n", "_").replace("\t", '') for each in wht_items[1:]]

    #transaction types
    wht_type = transHist.select(".wht_type")
    wht_type = [each.get_text().replace("\n", "_").replace("\t", '') for each in wht_type[1:]]

    #Individual transaction totals, this is the major rewrite to the previous found work, I could not make a single list comprehension work as hard as I tried, so I broke it into 3 steps.
    wht_total_num = []
    wht_total = transHist.select(".wht_total")
    wht_total=[each.get_text().strip().replace(',', '') for each in wht_total[1:]]

    for index, each in enumerate(wht_total[0:]):
        cleaned_string = each.replace('\t', '').replace('\n', '').replace('Credit', '').replace('$', '').strip()
        if cleaned_string == '':
            wht_total[index] = 0.0
        else:        
            wht_total[index] = cleaned_string

    #the above is sometimes too agressive and leave totals as null strings, hence the if-else statement above. This loop is to just to ensure all values convert to floats and it spits out an error specifiying index and value if not.
    #Note I am comfortable with setting them to 0.0 because I checked the parsed HTML and they were simply strings of \t \n and whitespace. Assigning them 0.0 does not effect the total in any way. I do not expect it to trigger.
    for index, each in enumerate(wht_total[0:]):
            try:
                wht_total[index] = float(each)
            except:
                print(f"There Was a value error at {index} and {each} ")
                sys.exit("Send a screenshot of this to @Delvaris on Github")
    
    #print(sum(wht_total), len(wht_total))

    frameDict = {'Date' : wht_date, "Items" : wht_items, 'Type' : wht_type, 'Total' : wht_total}

    return frameDict

def createDF(transDict):
    '''Literally just declares a global variable to store the dataframe and creates it from the
    passed dictionary. Converts the Date column to Datetime, and outputs an xlsx file of the full
    dataframe from account creation to present.
    '''
    global transactions
    transactions = pd.DataFrame.from_dict(transDict)

    transactions.Date = pd.to_datetime(transactions.Date, infer_datetime_format=True)
    transactions.to_excel('.\\transactions.xlsx')

def outputTotal():

    '''This function is a complete rewrite of the original outputTotal function. It is designed to take the dataframe created by createDF and filter it to only include purchases made on or after 
    January 28th, 2017, and to remove in-game purchases, and purchases of wallet credit. It then outputs the dataframe to an xlsx file, and writes the cumulative sum of the Total column to the console.
    Selection Statements made with co-pilot, and double checked by me.
    '''
    
    global transactions
    # Filter transactions to only include those made on or after January 28th, 2017
    transactions = transactions.loc[transactions['Date'] >= '2017-01-28']
    # filter transactions to remove in-game purchases, and purchases of wallet credit
    transactions = transactions.loc[~transactions['Type'].str.contains('in-game purchase|wallet credit|steam promotion', flags=re.IGNORECASE, regex=True)]
    #If the type column includes the phrase Refund make that row's total negative
    transactions.loc[transactions['Type'].str.contains('refund', flags=re.IGNORECASE, regex=True), 'Total'] = transactions['Total'] * -1
    # filter transactions to exclude purchases of wallet credit
    transactions = transactions.loc[~transactions['Items'].str.contains('wallet credit', flags=re.IGNORECASE, regex=True)]
    print(transactions["Total"].cumsum())
    #add a row to the end of the dataframe with today's date, the Item column as TOTAL, the Type column as TOTAL, and the Total column as the sum of the Total column
    transactions = pd.concat([transactions, pd.Series(['TOTAL', 'TOTAL', 'TOTAL', transactions['Total'].sum()], index=transactions.columns)], ignore_index=True)
    #reindex the frame
    transactions.reset_index(drop=True, inplace=True)
    #output the dataframe to an xlsx file called filtered_transactions.xlsx
    transactions.to_excel('.\\filtered_transactions.xlsx')

    

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
        print('Big chunks are out, let\'s comphrehend most of this')
    except Exception:
        traceback.print_exc()
        sys.exit("Post a screenshot of this to @Devlaris on Github.")
    
    try:
        print('Comprehension done, time to build a dataframe')
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


    
