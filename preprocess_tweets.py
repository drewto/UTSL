import re
import json
from progress.bar import Bar
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from collections import defaultdict
import operator

 

emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""
 
regex_str = [
	emoticons_str,
	r'<[^>]+>', # HTML tags
	r'(?:@[\w_]+)', # @-mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', # other words
	r'(?:\S)' # anything else
]
	
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def tokenize(s):
	return tokens_re.findall(s)
 
def find_url(string): 
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
	return url 

def preprocess(s, stop_terms, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	new_tokens = []
	for token in tokens:
		if ((token not in stop_terms) and (not token.startswith(('#','@')))):
			new_tokens.append(token)
	return new_tokens

def generate_stop_terms(preprocess_stop_terms_filename):
	punctuation = list(string.punctuation)
	stop = stopwords.words('english') + punctuation + ['rt', 'via']
	f = open(preprocess_stop_terms_filename, "r")
	stop_terms = []
	for line in f:
		stop_terms.append(line.rstrip())
	stop_terms += stop
	return stop_terms

def main():
	# Set filenames...
	input_filename = "data_files/scraped_tweets.json"
	output_filename = "data_files/preprocessed_tweets.json"
	preprocess_stop_terms_filename = "config_files/preprocess_stop_terms.txt"

	# Generate stop terms...
	stop_terms = generate_stop_terms(preprocess_stop_terms_filename)

	# Set up the progress bar...
	file_length = file_len(input_filename)
	bar = Bar('Pre-processing tweets...', max=file_length)

	# Open the files to begin reading and writing...
	file = open(input_filename, "r")
	#outfile = open(output_filename, "w")

	# Create the co-occurances matrix
	com = defaultdict(lambda : defaultdict(int))
		

	# Iterate through the tweets and process them
	for tweet in file:
		tweet_data = json.loads(tweet)
		text = tweet_data['text']
		terms_only = preprocess(text, stop_terms)
		for i in range(len(terms_only)-1):
			for j in range(i+1, len(terms_only)):
				w1, w2 = sorted([terms_only[i], terms_only[j]])				
				if w1 != w2:
					com[w1][w2] += 1

		#tweet_data['text'] = " ".join(new_text)
		#outfile.write(json.dumps(tweet_data))
		bar.next()
	bar.finish()

	bar = Bar('Searching for co-occurances...', max = len(com))
	com_max = []
	# For each term, look for the most common co-occurrent terms
	for t1 in com:
		t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
		for t2, t2_count in t1_max_terms:
			com_max.append(((t1, t2), t2_count))
		bar.next()
	bar.finish()
	# Get the most frequent co-occurrences
	terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
	print(terms_max[:15])

if __name__ == '__main__':
	main()