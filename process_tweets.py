import re
import json
from progress.bar import Bar
import nltk
from nltk.corpus import stopwords
import string
from collections import defaultdict
import operator
import math
import os.path

 

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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def tokenize(s):
	return tokens_re.findall(s)
 
def find_url(string): 
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
	return url 
 
def preprocess(s, stop_terms, lowercase=True):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	new_tokens = []
	for token in tokens:
		if ((token not in stop_terms) and (not token.startswith(('#','@','https://t.co/'))) and (not token == 'amp') and (not is_number(token))):
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
	stop_terms = [token.lower() for token in stop_terms]
	return stop_terms

def compute_com_max(com):
	bar = Bar('Searching for co-occurances...', max = len(com))
	com_max = []
	# For each term, look for the most common co-occurrent terms
	for t1 in com:
		t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
		for t2, t2_count in t1_max_terms:
			com_max.append(((t1, t2), t2_count))
		bar.next()
	bar.finish()
	return com_max

def compute_probability_of_term(single_count, com, file_length):
	bar = Bar('Computing probability of terms...', max = len(single_count))

	# Computer the probability of each term occuring
	# file_length is the total n. of tweets
	# p_t is the probability of the term being in a tweet
	p_t = {}
	p_t_com = defaultdict(lambda : defaultdict(int))
	
	for term, n in single_count.items():
		p_t[term] = n / file_length
		for t2 in com[term]:
			p_t_com[term][t2] = com[term][t2] / file_length
		bar.next()
	bar.finish()
	return (p_t, p_t_com)

def compute_pmi(p_t, p_t_com, com):
	bar = Bar('Compute pointwise mutual information (PMI)...', max = len(p_t))
	pmi = defaultdict(lambda : defaultdict(int))
	for t1 in p_t:
		for t2 in com[t1]:
			denom = p_t[t1] * p_t[t2]
			pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)
		bar.next()
	bar.finish()
	return pmi

def compute_semantic_orientation(pmi, p_t):
	f = open("config_files/positive-words.txt", "r", errors='replace')
	positive_vocab = []
	for line in f:
		if line[0] != ';':
			positive_vocab.append(line.rstrip())
	positive_vocab = [token.lower() for token in positive_vocab]
	f.close()

	f = open("config_files/negative-words.txt", "r", errors='replace')
	negative_vocab = []
	for line in f:
		if line[0] != ';':
			negative_vocab.append(line.rstrip())
	negative_vocab = [token.lower() for token in negative_vocab]
	f.close()
	
	bar = Bar('Computing semantic orientation...', max = len(p_t))
	semantic_orientation = {}
	for term, n in p_t.items():
		positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
		negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
		semantic_orientation[term] = positive_assoc - negative_assoc
		bar.next()
	bar.finish()
	return semantic_orientation

def main():
	# Set filenames...
	input_filename = "data_files/scraped_tweets.json"
	preprocess_stop_terms_filename = "config_files/preprocess_stop_terms.txt"

	nltk.download('stopwords')

	if (os.path.exists(input_filename) == False):
		exit(0)
	# Generate stop terms...
	stop_terms = generate_stop_terms(preprocess_stop_terms_filename)

	# Set up the progress bar...
	file_length = file_len(input_filename)
	if (file_length == 0):
		exit(0)
	bar = Bar('Pre-processing tweets...', max=file_length)

	# Open the file to begin reading...
	file = open(input_filename, "r")

	# Create the co-occurances matrix
	com = defaultdict(lambda : defaultdict(int))
	
	# Create a dictionary to store how often each single term occurs
	single_count = {}

	# Iterate through the tweets and process them
	for tweet in file:
		tweet_data = json.loads(tweet)
		text = tweet_data['text']
		terms_only = preprocess(text, stop_terms)
		for i in range(len(terms_only)):
			if terms_only[i] in single_count:
				single_count[terms_only[i]] += 1
			else:
				single_count[terms_only[i]] = 1
			for j in range(i, len(terms_only)):
				w1, w2 = sorted([terms_only[i], terms_only[j]])				
				if w1 != w2:
					com[w1][w2] += 1
		bar.next()
	bar.finish()

	# Create a list for the most common co-occurances
	com_max = compute_com_max(com)
	
	# Get the most frequent co-occurrences
	terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
	#print(terms_max[:15])

	(p_t, p_t_com) = compute_probability_of_term(single_count, com, file_length)
	pmi = compute_pmi(p_t, p_t_com, com)
	semantic_orientation = compute_semantic_orientation(pmi, p_t)
	semantic_sorted = sorted(semantic_orientation.items(),key=operator.itemgetter(1), reverse=True)
	top_pos = semantic_sorted[:5]
	top_neg = semantic_sorted[-5:]
	top_neg.reverse()
	
	print("\nTop positive terms associated with the search term:")
	for item in top_pos:
		(word, rating) = item
		print(word + ": " + str(rating))

	print("\nTop negative terms associated with the search term:")
	for item in top_neg:
		(word, rating) = item
		print(word + ": " + str(rating))

	f = open("data_files/term_semantic_orientation", "w+")
	for (word,rating) in semantic_sorted:
		f.write(word+" "+str(rating)+"\n")

if __name__ == '__main__':
	main()