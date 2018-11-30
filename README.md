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



Output:

The output of this program comes in a few parts, all of which are saved in the 'UTSL/data_files/' directory.


'scrape_tweets.py'

The 'scrape_tweets.py' program scraped Tweets from Twitter using Tweepy and saves them to 'UTSL/data_files/scraped_tweets.json'. These tweets are not the full JSON downloaded from Tweepy, but a stripped-down version containing the following information (if available in the original Tweet): 
	
	1. user_id
	2. user_name
	3. user_screen_name
	4. user_follower_count
	5. user_friends_count
	6. geo
	7. coordinates
	8. place
	9. text
	To learn more about what these fields actually mean, please check here: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html


'process_tweets.py'

'process_tweets.py' takes the tweets that were scraped and processes them. It does this by first getting rid of stop words (words that have very little meaning, like 'a', 'and', 'the') and only saving the words that actually contain information. It then computes the probability of any non-stop word appearing in any given text (# of times word has appeared / total # of tweets). It then uses these probabilities in tandem with a list of positive and negative words (for references see the credits section at the bottom) to compute the semantic orientation of each word. It then saves the list of words and their respective semantic orientation in 'UTSL/data_files/term_semantic_orientation.txt'. 


'calculate_tweet_sentiment.py'

This program loads up the semantic orientation file created in 'process_tweets.py' and then simply iterates through the scraped tweets saved by 'scrape_tweets.py', coming up with a sentiment value by adding all of the sentiment of the words in the text. If this value is higher than 0, the tweet is predicted to be positive. If the sentiment value is lower than 0, it is predicted to have negative sentiment. 


NOTE: While this project does use external libraries like tweepy, progress, and nltk, the run_code script will create a virtualenv to download these libraries so it doesn't add unecessary packages to your computer's python environment. Be warned, however: one thing it does install by default is virtualenv.

TWEEPY CREDENTIALS: When run all at once, this project will attempt to download tweets from Twitter using the Tweepy API. In order to do this, it must read a file called "creds.txt" to get these credentials. You must have your own twitter developer account and app registered in order to use this (sorry but I'm not sharing my keys)

However, if you already have tweets stored in a .json file that you wish to analyze, simply make modifications to process_tweets.py to direct it to your .json file and things might work (unsure, not tested) and you will not need to do any of the following

Create a key file named "creds.txt" that looks like the following in the UTSL directory:

	consumer_key:[consumer key]
	consumer_secret:[consumer secret]
	access_token:[access token]
	access_secret:[access secret]





CREDITS

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
