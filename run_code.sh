#!/usr/bin/env bash

if [ `python3 -m virtualenv --version | grep "No module named" | wc -l` -gt 0 ];
then 
	echo "virtualenv not installed, installing it now..."
	python3 -m pip install --user virtualenv
else
	echo "virtualenv already installed"
fi

python3 -m virtualenv env
source env/bin/activate

python3 -m pip install progress
python3 -m pip install tweepy

python3 scrape_tweets.py 1000
python3 preprocess_tweets.py
