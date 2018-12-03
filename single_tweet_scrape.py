import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
from progress.bar import Bar
from progress.counter import Counter

from perceptron import generate_features, classify, compute_accuracy, standard_perceptron
from process_tweets import preprocess, generate_stop_terms

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

tweet_count = 0
max_tweet_count = 0

class MyListener(StreamListener):
	def on_data(self, data):
		try:
			json_data = json.loads(data)
			if (json_data['user']['lang'] == 'en'):
				new_json_data = prune_data(data)
				return True
			else:
				return True

		except BaseException as e:
			if str(e) == "1":
				exit(0)
			#print("Error on_data: %s" % str(e))
		return True
 
	def on_error(self, status):
		print(status)	
		return True

def read_scrape_words(filename):
	scrape_words = []
	file = open(filename, "r")
	for line in file:
		scrape_words.append(line.rstrip())
	return scrape_words

def prune_data(data):
	# Convert the string into a JSON object
	json_data = json.loads(data)

	# Prepare to store the useful data in a new object
	new_json_data = {}

	# Extract the full text
	if 'retweeted_status' in json_data:
		new_json_data['text'] = json_data['retweeted_status']['extended_tweet']['full_text'].rstrip()
	elif 'text' not in json_data:
		print("test not in json")
		return 0
	elif json_data['truncated'] == True:
		new_json_data['text'] = json_data['extended_tweet']['full_text']
	else: 
		new_json_data['text'] = json_data['text'].rstrip()
	# Extract user stuff
	print(new_json_data['text'])
	exit(1)

def main():
	# Set creds up
	try:
		f = open("creds.txt")
		for line in f:
			word = line.split(":")
			if word[0] == 'consumer_key':
				consumer_key = word[1].rstrip()
			elif word[0] == 'consumer_secret':
				consumer_secret = word[1].rstrip()
			elif word[0] == 'access_token':
				access_token = word[1].rstrip()
			elif word[0] == 'access_secret':
				access_secret = word[1].rstrip()

	except BaseException as e:
		print(str(e))
		print("Error! Please set up a credential file in 'creds.txt' like the example below:")
		print("\tconsumer_key: [consumer_key]")
		print("\tconsumer_secret: [consumer_secret]")
		print("\taccess_token: [access_token]")
		print("\taccess_secret: [access_secret]")
		exit(0)

	# Set up scrape words
	scrape_words = read_scrape_words("config_files/scrape_words.txt")

	# API initial connection and setup
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	twitter_stream = Stream(auth, MyListener())
	
	twitter_stream.filter(track=scrape_words)
	

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)