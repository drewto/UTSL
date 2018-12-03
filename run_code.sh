#!/usr/bin/env bash
clear
if [ `python3 -m virtualenv --version | grep "No module named" | wc -l` -gt 0 ];
then 
	echo "virtualenv not installed, installing it now..."
	python3 -m pip install --user virtualenv
else
	echo "virtualenv already installed"
fi

if [ ! -d "env" ]; then
	echo "creating virtual env"
	python3 -m virtualenv env
else
	echo "env already exists"
fi
source env/bin/activate

python3 -m pip -q install progress
python3 -m pip -q install tweepy
python3 -m pip -q install nltk

#rm data_files/scraped_tweets.json

if [[ $# -eq 0 ]]; then
	echo "Press crtl+c when you think you have enough tweets. It will then go and process them."
	python3 scrape_tweets.py
	echo ""
else
	python3 scrape_tweets.py $1
fi

python3 process_tweets.py
python3 calculate_tweet_sentiment.py
python3 perceptron.py

while true; do
	tweet=`python3 single_tweet_scrape.py`
	echo $tweet
	python3 process_single_tweet.py $tweet
	sleep 3
done
