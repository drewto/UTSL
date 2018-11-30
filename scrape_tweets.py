import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
from progress.bar import Bar
from progress.counter import Counter


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

tweet_count = 0
max_tweet_count = 0

class MyListener(StreamListener):
	
	def __init__(self):
		super().__init__()
		self.counter = 0
		self.run_forever = True
		self.limit = 0
		if len(sys.argv) > 1:
			# No user-provided value, run forever
			self.limit = int(sys.argv[1])
			self.run_forever = False
			self.bar = Bar('Collecting tweets...',max=self.limit)

		else:
			self.bar = Counter('Collecting tweets...')


	def on_data(self, data):
		try:
			json_data = json.loads(data)
			if (json_data['user']['lang'] == 'en'):
				prune_data(data)
				self.counter += 1
				self.bar.next()
			if (self.run_forever == False):
				if self.limit == self.counter:
					self.bar.finish()
					exit(1)
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
	if 'extended_tweet' in json_data:
		new_json_data['text'] = json_data['extended_tweet']['full_text']
	elif 'text' not in json_data:
		return 0
	else: 
		new_json_data['text'] = json_data['text']

	# Extract user stuff
	new_json_data['user_id'] = json_data['user']['id']
	new_json_data['user_name'] = json_data['user']['name']
	new_json_data['user_screen_name'] = json_data['user']['screen_name']
	new_json_data['user_followers_count'] = json_data['user']['followers_count']
	new_json_data['user_friends_count'] = json_data['user']['friends_count']

	# Extract geolocation stuff in case we want to do stuff with it later
	new_json_data['geo'] = json_data['geo']
	new_json_data['coordinates'] = json_data['coordinates']
	new_json_data['place'] = json_data['place']

	# Save the resulting tweet to a file
	with open('data_files/scraped_tweets.json', 'a') as f:
		f.write(json.dumps(new_json_data)+'\n')

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
	# API initial connection and setup
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	twitter_stream = Stream(auth, MyListener())
	scrape_words = read_scrape_words("config_files/scrape_words.txt")
	print("scrape words (search terms):")
	for word in scrape_words:
		print("\t- " + word)
	twitter_stream.filter(track=scrape_words)
	

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)