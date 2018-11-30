#!/usr/bin/env bash

if [ `python3 -m virtualenv --version | grep "No module named" | wc -l` -gt 0 ];
then 
	echo "virtualenv not installed, installing it now..."
	python3 -m pip install --user virtualenv
else
	echo "virtualenv already installed"
fi

if [ ! -d "env" ]; then
	python3 -m virtualenv env
fi
source env/bin/activate

python3 -m -q pip install progress
python3 -m -q pip install tweepy
python3 -m -q pip install nltk

echo "Press crtl+c when you think you have enough tweets. It will then go and process them."
python3 scrape_tweets.py
python3 process_tweets.py
