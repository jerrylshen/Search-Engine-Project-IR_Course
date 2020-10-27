## Search Engine http://shenjl.pythonanywhere.com/
Built after crawling 55,393 HTML documents in developer.zip, with 1,352,851 unique terms in a team of 3.

This Drive folder contains the zipped folder, the outputted txt files that are too large to upload to Github, and some misc code:  
https://drive.google.com/drive/folders/16kRnpAoDPqRqCHf6IUg8JZBwJDjMgLqM?usp=sharing  
  
The code that handles the crawling, simhash, calculating the TF-IDF, etc isn't shown to prevent future CS 121 students to reference. 

## Short Summary on How We Created It
When crawling the zipped folder, each HTML document is assigned a docID number. Each alphanumeric token that's crawled is stemmed before being placed into an index. The frequency of each token is also tracked for each docID that it appears in. SimHash is also used to remove any near duplicate pages, with a threshold set at 0.95.

After crawling, the TF-IDF is calculated for every token in every document. Then the TF-IDF scores are normalized.

At runtime of the Flask app, all the relevant .txt index files are loaded into memory and cosine scoring and pageranking is used to rank the resulting document URLs.  
  
To overcome PythonAnywhere's 100MiB file upload limit and Github's 25MB upload limit, writeToSmallIndex.py is used to separate the larger Token_TFIDF_Normalized.txt into two separate files which then gets recombined when initializing the Flask app.
