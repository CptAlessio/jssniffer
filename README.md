<h2>JSSniffer</h2>
JSSniffer is a python script aimed at security professionals looking to detect secrets leaked in JavaScript files. The program crawls a website and identifies any JavaScript files containing a set of keywords specified by the user. 

<h3>How it works?</h3>
It downloads the unique JavaScript files locally and searches for specific keywords defined in an array called `keywords`. By default, the program searches for the keyword `token`, but users can add their own keywords to the array if they want. 
If a keyword is found in a JavaScript file, the program prints the name of the keyword and the file name. 
The program also provides an option for the user to delete the js_files folder and its contents.

<h3>Dependencies</h3>

The program uses the following Python libraries:

- `requests`: Used for making HTTP requests to web pages.
- `beautifulsoup4`: Used for parsing HTML and XML documents.
- `urllib`: Used for parsing URLs and joining them together to create absolute URLs.
- `os`: Used for interacting with the file system, including creating and deleting directories and files.
- `shutil`: Used for deleting directories and their contents recursively.

<h3>Example</h3>

```
C:\path\jssniffer>python jssniffer.py
Enter a URL to crawl: http://www.yourwebsite.com
..............................

Found 4 unique JavaScript files on www.yourwebsite.com:
 - /aJavascriptFile1.js
 - /aJavascriptFile2.js
 - /aJavascriptFile3.js
 - /aJavascriptFile4.js
File aJavascriptFile1.js contains keyword 'token'
File aJavascriptFile4.js contains keyword 'token'
Are you sure you want to delete C:\path\jssniffer\jssniffer\js_files? (y/n): N
C:\path\jssniffer was not deleted.
```
