import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
from progress.bar import Bar

consumer_key = '4gzBY6Jmym4x42KIuQo9L4urQ'
consumer_secret = 'pSAhz09Q6OhI4f4XuP0Q87TzQV8aZHR6tgn0zgzTHGuiDIDeut'
access_token = '27372243-fMxHce6RVTID2Ykj02GmxrhGrFpmuTlLAzFr7FS1Y'
access_secret = 'lotydcEqecC9phanNP56P2jtsdgX9fwQLLYeRgVxJjE5n'

tweet_count = 0
max_tweet_count = 0

class MyListener(StreamListener):
	
	def __init__(self):
		super().__init__()
		self.counter = 0
		if len(sys.argv) < 2:
			print("Error: Incorrect usage\nUsage: python3 scrape_tweets.py [# of tweets to scrape]")
			exit(0)
		self.limit = int(sys.argv[1])
		self.bar = Bar('Collecting tweets...',max=self.limit)

	def on_data(self, data):
		try:

			prune_data(data)
			self.counter += 1
			self.bar.next()
			if self.limit > self.counter:
				return True
			else:
				self.bar.finish()
				exit(1)
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
		scrape_words.append(line)
	return scrape_words

def prune_data(data):
	# Convert the string into a JSON object
	json_data = json.loads(data)
	if json_data['user']['lang'] == 'en':

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

	# API initial connection and setup
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	twitter_stream = Stream(auth, MyListener())
	if sys.argv[1] == "":
		sys.argv[1] = 100

	scrape_words = read_scrape_words("config_files/scrape_words.txt")
	twitter_stream.filter(track=scrape_words)
	

if __name__ == '__main__':
	main()