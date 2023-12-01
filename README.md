# SteamTransactionHistory

The release is a zip file containing a win64 executable and required dependencies to execute it in an environment that does not have the Python interpreter installed.
It searches for a single htm/html file of one's steam purchase history, does the necessary data cleanup and parsing, prints a transactions.xlsx of all transactions from the beginning of your account*
It then uses a series of selection statements to limit the date to after Jan 28, 2017 (pursuit to the class action lawsuit against valve), handle ingame purchases, wallet loads, and refunds. Lastly it 
writes a filteredTransactions.xlsx file, as well as displays the total in the console.


INSTRUCTIONS:
1. Download your steam purchase history as an htm/html file to a new folder.
2. Extract the contents of the zip file to that folder.
3. Run the Exe


BeautifulSoup4 -> Pandas parsing code credit to Alexander Lacson, @max-torch on github. Rewritten not pulled.

Note: ALL successful executions will end with "Press a key to exit" if literally anything else has happened the the program threw an exception and it was caught. If the output is incorrect
then the bug is logical and you should open an issue.

*This is a very dirty file, the only thing that is clean in it are the totals which are suitable floating point numbers. I included the output for comparison purposes to the filtered version.

FAQ:

Will I compile executables or create releases for other platforms?

  Unlikely. I do not currently have easy access to MacOS or Linux installations with a robust implementation of (current Python version). Linux is more likely than MacOS due to the existence of WSL.

Will I add cmdline argument functionality so a path can be specified?
  
  Maybe. I don't intend for this to be used by many people, so unless it blows up and this feature request is made I won't.

Why Python, why not use Java that can compile directly to a binary executable?

  Because I am more familiar with Python than Java. Also I wrote this on the spur of the moment.

Can I use the existing code as a base/redistribute it/redistribute the release?

  You go Coco. Please provide credit to @Delvaris on github otherwise do whatever. With some modifications (IE removing code that cleans the data so it is fit for purpose) it could provide a good basis
  for a wider visualization of steam transaction data.
