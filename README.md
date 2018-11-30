# UTSL
Unsupervised Twitter Sentiment Learner


This project was built to explore what people are thinking about certain topics, using Twitter to collect the data.

By specifying search terms in config_files/scrape_words.txt and running './run_code', you will be able to see what words people associate with your search terms, sorted by positive and negative association.

Usage:

1. Clone repo
2. open 'config_files/scrape_words.txt' and add the terms you would like to search for, one line per term
3. run './run_code' OR './run_code [# of tweets you want to analyze]'

NOTE: You must have your own twitter developer account and app registered in order to use this (sorry but I'm not sharing my keys)

Create a key file named "creds.txt" that looks like the following in the UTSL directory:

	consumer_key:[consumer key]
	consumer_secret:[consumer secret]
	access_token:[access token]
	access_secret:[access secret]




Positive and negative word libraries came from the following:

	Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
	Proceedings of the ACM SIGKDD International Conference on Knowledge 
	Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
	Washington, USA, 
	Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
	and Comparing Opinions on the Web." Proceedings of the 14th 
	International World Wide Web conference (WWW-2005), May 10-14, 
	2005, Chiba, Japan.
