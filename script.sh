#!/usr/bin/env bash


while true; do
	tweet=`python3 single_tweet_scrape.py`
	echo $tweet
	python3 process_single_tweet.py $tweet
	sleep 3

done