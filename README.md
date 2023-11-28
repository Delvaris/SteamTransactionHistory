# SteamTransactionHistory

The release is a zip file containing a win64 executable and required dependencies to execute it in an environment that does not have the Python interpreter installed.
It will eventually find a saved steam transaction history in the same directory, parse it, and provide the total transaction amount from January 28, 2017 to present.

BeautifulSoup4 -> Pandas parsing code credit to Alexander Lacson, @max-torch on github. Rewritten not pulled.

Note: ALL successful executions will end with "Press a key to exit" if literally anything else has happened the the program threw an exception and it was caught. If the output is incorrect
then the bug is logical and you should open an issue.

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
