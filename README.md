# UTSL
Unsupervised Twitter Sentiment Learner


This project was built to explore what people are thinking about certain topics, using Twitter to collect the data.

By specifying search terms in config_files/scrape_words.txt and running './run_code', you will be able to see what words people associate with your search terms, sorted by positive and negative association.

Usage:

1. Clone repo
2. open 'config_files/scrape_words.txt' and add the terms you would like to search for, one line per term
3. run one of the following:

		./run_code 
	OR 

		./run_code [tweet_count]
	where [tweet_count] is the number of tweets you wish to collect before analyzing them

TWEEPY CREDENTIALS: When run all at once, this project will attempt to download tweets from Twitter using the Tweepy API. In order to do this, it must read a file called "creds.txt" to get these credentials. You must have your own twitter developer account and app registered in order to use this (sorry but I'm not sharing my keys)

However, if you already have tweets stored in a .json file that you wish to analyze, simply make modifications to process_tweets.py to direct it to your .json file and things might work (unsure, not tested) and you will not need to do any of the following

Create a key file named "creds.txt" that looks like the following in the UTSL directory:

	consumer_key:[consumer key]
	consumer_secret:[consumer secret]
	access_token:[access token]
	access_secret:[access secret]


I was roughly following the instructions in this tutorial to complete the sentiment analysis:

		https://marcobonzanini.com/2015/03/23/mining-twitter-data-with-python-part-4-rugby-and-term-co-occurrences/

Positive and negative word libraries came from the following:

	Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
	Proceedings of the ACM SIGKDD International Conference on Knowledge 
	Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
	Washington, USA, 
	Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
	and Comparing Opinions on the Web." Proceedings of the 14th 
	International World Wide Web conference (WWW-2005), May 10-14, 
	2005, Chiba, Japan.
